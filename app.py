"""SQLite-backed JWKS server for CSCE 3550 Project 2."""
import base64
import os
import sqlite3
import time

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['DATABASE'] = os.environ.get('JWKS_DB_PATH', 'totally_not_my_privateKeys.db')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def generate_key(exp):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with connect_db() as connection:
        cursor = connection.execute(
            'INSERT INTO keys (key, exp) VALUES (?, ?)', (pem, exp)
        )
        return cursor.lastrowid


def initialize_db():
    with connect_db() as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS keys (
            kid INTEGER PRIMARY KEY AUTOINCREMENT,
            key BLOB NOT NULL,
            exp INTEGER NOT NULL
        )''')
        now = int(time.time())
        valid = connection.execute('SELECT COUNT(*) FROM keys WHERE exp > ?', (now,)).fetchone()[0]
        expired = connection.execute('SELECT COUNT(*) FROM keys WHERE exp <= ?', (now,)).fetchone()[0]
    if not valid:
        generate_key(now + 7200)
    if not expired:
        generate_key(now - 3600)


def read_key(expired=False):
    now = int(time.time())
    operator = '<=' if expired else '>'
    ordering = 'DESC' if expired else 'DESC'
    with connect_db() as connection:
        row = connection.execute(
            f'SELECT kid, key, exp FROM keys WHERE exp {operator} ? ORDER BY exp {ordering} LIMIT 1',
            (now,),
        ).fetchone()
    if row is None:
        return None
    return {'kid': str(row[0]), 'private_key': serialization.load_pem_private_key(row[1], password=None), 'exp': row[2]}


def to_base64(number):
    data = number.to_bytes((number.bit_length() + 7) // 8, 'big')
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def make_jwk(key):
    numbers = key['private_key'].public_key().public_numbers()
    return {
        'kty': 'RSA', 'kid': key['kid'], 'use': 'sig', 'alg': 'RS256',
        'n': to_base64(numbers.n), 'e': to_base64(numbers.e),
    }


@app.get('/.well-known/jwks.json')
def get_jwks():
    now = int(time.time())
    with connect_db() as connection:
        rows = connection.execute('SELECT kid, key, exp FROM keys WHERE exp > ?', (now,)).fetchall()
    keys = [make_jwk({'kid': str(kid), 'private_key': serialization.load_pem_private_key(pem, password=None)})
            for kid, pem, _ in rows]
    return jsonify({'keys': keys})


@app.post('/auth')
def auth():
    expired = 'expired' in request.args
    key = read_key(expired=expired)
    if key is None:
        return jsonify({'error': 'No matching signing key available'}), 503
    now = int(time.time())
    expiration = min(key['exp'], now - 1) if expired else min(key['exp'], now + 3600)
    token = jwt.encode(
        {'sub': 'user', 'iat': now, 'exp': expiration},
        key['private_key'], algorithm='RS256', headers={'kid': key['kid']},
    )
    return token, 200


initialize_db()

if __name__ == '__main__':
    app.run(port=8080)
