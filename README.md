CSCE 3550 Project 2 – JWKS Server with SQLite
Student: Ashwin Kumar Mandaloju  
Course: CSCE 3550 – Foundations of Cybersecurity

About This Project
For Project 2, I updated my JWKS server from Project 1 by adding a SQLite database.
In Project 1, the RSA keys were stored in memory, so they would be lost when the server stopped. In this project, I changed the server to save the private keys in a database so they can still be used after restarting the server.
The server uses Flask and Python to generate RSA keys, create JWT tokens, and provide public keys for verifying those tokens.
What I Added
•	Added a SQLite database to store RSA private keys.
•	Updated the authentication endpoint to read keys from the database.
•	Updated the JWKS endpoint to return public keys that have not expired.
•	Added support for generating JWTs using expired keys.
•	Used parameterized SQL queries to help prevent SQL injection.
•	Added automated tests to check that everything works correctly.
Tools Used
•	Python
•	Flask
•	SQLite
•	PyJWT
•	Cryptography
•	Pytest
How to Run the Project
First, download the repository and open the project folder in VS Code.
Install the required packages:
bash
python -m pip install -r requirements.txt
Start the server:
bash
python app.py
The server runs at: “http://127.0.0.1:8080”
The SQLite database is created in the project folder.
API Endpoints
1. GET /.well-known/jwks.json
Returns the public keys that are still valid. Expired keys are not included.
2. POST /auth
Generates a JWT token using a valid RSA private key stored in the database.
3. POST /auth?expired=true
Generates a JWT token using an expired RSA private key.
The authentication is simulated for this assignment, so actual usernames and passwords are not verified.
Database
The project uses a SQLite database named `totally_not_my_privateKeys.db`.
The database stores the key ID, private key, and expiration time.
Private keys are saved in PEM format. I used parameterized queries when working with the database to help prevent SQL injection.
The database file is not uploaded to GitHub because it contains private keys.
Testing
I tested the server using Pytest and the Gradebot provided for this course.
Pytest Results
•	9 tests passed
•	98% code coverage
Gradebot Results
•	Valid JWT authentication: 15/15
•	Valid JWK in JWKS: 20/20
•	SQLite database: 15/15
•	Database queries: 15/15
•	Code quality: 4.25/5
Overall Gradebot score: 98.93%**
The screenshots of the Gradebot results and test coverage are available in the `screenshots` folder.
Conclusion
In this project, I learned how to connect a Python Flask application to a SQLite database and securely store RSA private keys.
I also learned how to use parameterized SQL queries, work with JWT authentication, and test a server using automated tests. This project helped me understand how databases can improve a server by keeping important data available even after restarting the application.
