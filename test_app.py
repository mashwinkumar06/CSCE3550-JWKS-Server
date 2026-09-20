import time
import jwt

from app import app, normal_key, old_key


def test_jwks():
    client = app.test_client()

    response = client.get("/.well-known/jwks.json")

    assert response.status_code == 200

    data = response.get_json()

    assert "keys" in data
    assert len(data["keys"]) == 1

    key = data["keys"][0]

    assert key["kid"] == normal_key["kid"]
    assert key["kty"] == "RSA"
    assert key["alg"] == "RS256"

    # The expired key should not be in JWKS
    assert key["kid"] != old_key["kid"]


def test_normal_auth():
    client = app.test_client()

    response = client.post("/auth")

    assert response.status_code == 200

    token = response.get_data(as_text=True)

    header = jwt.get_unverified_header(token)

    assert header["kid"] == normal_key["kid"]

    payload = jwt.decode(
        token,
        normal_key["private_key"].public_key(),
        algorithms=["RS256"]
    )

    assert payload["sub"] == "user"
    assert payload["exp"] > int(time.time())


def test_expired_auth():
    client = app.test_client()

    response = client.post("/auth?expired=true")

    assert response.status_code == 200

    token = response.get_data(as_text=True)

    header = jwt.get_unverified_header(token)

    assert header["kid"] == old_key["kid"]

    payload = jwt.decode(
        token,
        old_key["private_key"].public_key(),
        algorithms=["RS256"],
        options={"verify_exp": False}
    )

    assert payload["exp"] < int(time.time())


def test_auth_get_not_allowed():
    client = app.test_client()

    response = client.get("/auth")

    assert response.status_code == 405


def test_jwks_post_not_allowed():
    client = app.test_client()

    response = client.post("/.well-known/jwks.json")

    assert response.status_code == 405