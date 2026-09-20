\# CSCE 3550 Project 1 - JWKS Server



Name: Ashwin Kumar Mandaloju



\## About



This project is a basic JWKS server created for CSCE 3550.



The server generates RSA keys and uses them to sign JWTs. It has a valid key and an expired key. The JWKS endpoint only returns keys that have not expired.



\## Endpoints



\### GET /.well-known/jwks.json



Returns the valid public key in JWKS format.



\### POST /auth



Returns a JWT signed using the valid RSA key.



\### POST /auth?expired=true



Returns an expired JWT signed using the expired RSA key.



\## Run the Server



Install the required packages:



```bash

pip install -r requirements.txt

