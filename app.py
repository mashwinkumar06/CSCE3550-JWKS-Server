import base64
import time
import uuid

import jwt
from flask import Flask, jsonify, request
from cryptography.hazmat.primitives.asymmetric import rsa

app = Flask(__name__)


# Makes a new RSA key
def make_key(expired=False):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Give every key its own ID
    kid = str(uuid.uuid4())

    # One key will already be expired
    if expired:
        expires = int(time.time()) - 3600
    else:
        expires = int(time.time()) + 3600

    return {
        "private_key": private_key,
        "kid": kid,
        "expires": expires
    }


# We need one normal key and one expired key
normal_key = make_key()
old_key = make_key(expired=True)


# Converts a number to the format needed by JWK
def to_base64(number):
    size = (number.bit_length() + 7) // 8
    data = number.to_bytes(size, "big")

    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


# Changes our RSA public key into JWK format
def make_jwk(key):
    public_key = key["private_key"].public_key()
    numbers = public_key.public_numbers()

    return {
        "kty": "RSA",
        "kid": key["kid"],
        "use": "sig",
        "alg": "RS256",
        "n": to_base64(numbers.n),
        "e": to_base64(numbers.e)
    }


# JWKS endpoint
@app.route("/.well-known/jwks.json", methods=["GET"])
def get_jwks():
    keys = []
    now = int(time.time())

    # Only add keys that are still valid
    if normal_key["expires"] > now:
        keys.append(make_jwk(normal_key))

    if old_key["expires"] > now:
        keys.append(make_jwk(old_key))

    return jsonify({"keys": keys})


# Authentication endpoint
@app.route("/auth", methods=["POST"])
def auth():
    now = int(time.time())

    # Use the expired key when ?expired is in the URL
    if "expired" in request.args:
        key = old_key
        expiration = now - 3600
    else:
        key = normal_key
        expiration = now + 3600

    payload = {
        "sub": "user",
        "iat": now,
        "exp": expiration
    }

    token = jwt.encode(
        payload,
        key["private_key"],
        algorithm="RS256",
        headers={"kid": key["kid"]}
    )

    return token, 200


if __name__ == "__main__":
    app.run(port=8080)