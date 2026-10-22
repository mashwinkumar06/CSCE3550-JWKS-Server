"""Tests for SQLite-backed JWKS authentication."""
import sqlite3
import time

import jwt
import pytest
import app as server


@pytest.fixture(autouse=True)
def temporary_database(tmp_path, monkeypatch):
    monkeypatch.setitem(server.app.config, 'DATABASE', str(tmp_path / 'test.db'))
    server.initialize_db()


def test_database_schema_and_key_persistence():
    with server.connect_db() as connection:
        rows = connection.execute('SELECT kid, key, exp FROM keys').fetchall()
    assert len(rows) == 2
    assert all(isinstance(row[0], int) and b'PRIVATE KEY' in row[1] for row in rows)
    server.initialize_db()
    with server.connect_db() as connection:
        assert connection.execute('SELECT COUNT(*) FROM keys').fetchone()[0] == 2


def test_jwks_only_valid_keys():
    response = server.app.test_client().get('/.well-known/jwks.json')
    assert response.status_code == 200
    keys = response.get_json()['keys']
    assert len(keys) == 1
    assert keys[0]['kty'] == 'RSA'
    assert keys[0]['alg'] == 'RS256'
    assert keys[0]['use'] == 'sig'
    assert keys[0]['n'] and keys[0]['e']
    assert keys[0]['kid'] == server.read_key()['kid']


@pytest.mark.parametrize('endpoint,expired', [('/auth', False), ('/auth?expired=true', True), ('/auth?expired', True)])
def test_auth_tokens(endpoint, expired):
    response = server.app.test_client().post(endpoint, json={'username': 'userABC', 'password': 'password123'})
    assert response.status_code == 200
    token = response.get_data(as_text=True)
    key = server.read_key(expired=expired)
    assert jwt.get_unverified_header(token)['kid'] == key['kid']
    payload = jwt.decode(token, key['private_key'].public_key(), algorithms=['RS256'], options={'verify_exp': False})
    assert payload['sub'] == 'user'
    assert (payload['exp'] <= int(time.time())) == expired


def test_missing_key_returns_503():
    with server.connect_db() as connection:
        connection.execute('DELETE FROM keys')
    response = server.app.test_client().post('/auth')
    assert response.status_code == 503


def test_http_methods():
    client = server.app.test_client()
    assert client.get('/auth').status_code == 405
    assert client.post('/.well-known/jwks.json').status_code == 405


def test_generate_key():
    kid = server.generate_key(int(time.time()) + 7200)
    assert isinstance(kid, int)
    with server.connect_db() as connection:
        assert connection.execute('SELECT COUNT(*) FROM keys WHERE kid = ?', (kid,)).fetchone()[0] == 1


def test_expired_key_is_not_published():
    with server.connect_db() as connection:
        connection.execute('UPDATE keys SET exp = ?', (int(time.time()) - 5,))
    assert server.app.test_client().get('/.well-known/jwks.json').get_json() == {'keys': []}
