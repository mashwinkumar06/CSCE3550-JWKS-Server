**CSCE 3550 Project 2 – JWKS Server with SQLite
Student: Ashwin Kumar Mandaloju
Course: CSCE 3550 – Foundations of Cybersecurity**
**About This Project**
For Project 2, I updated my JWKS server from Project 1 by adding a SQLite database.
In Project 1, the RSA keys were stored in memory, so they would be lost when the server stopped. In this project, I changed the server to save the private keys in a database so they can still be used after restarting the server.
The server uses Python and Flask to generate RSA keys, create JWT tokens, and provide public keys that can be used to verify those tokens.
**What I Added**
•	Added a SQLite database to store RSA private keys.
•	Updated the authentication endpoint to read private keys from the database.
•	Updated the JWKS endpoint to return public keys that have not expired.
•	Added support for generating JWTs using expired keys.
•	Used parameterized SQL queries to help prevent SQL injection.
•	Added automated tests to check that the server works correctly.
**Tools Used**
•	Python
•	Flask
•	SQLite
•	PyJWT
•	Cryptography
•	Pytest
•	Pytest-cov
**How to Run the Project**
First, download the repository and open the project folder in VS Code.
**Step 1:** Install the required packages
python -m pip install -r requirements.txt
**Step 2:** Start the server
python app.py
The server runs at:
http://127.0.0.1:8080
The SQLite database is created in the project folder when the application starts.

**API Endpoints**
GET /.well-known/jwks.json
This endpoint returns the public keys that are still valid. Expired keys are not included in the response.
POST /auth
This endpoint generates a JWT token using a valid RSA private key stored in the database.
POST /auth?expired=true
This endpoint generates a JWT token using an expired RSA private key.
Authentication is simulated for this assignment, so the server does not verify actual usernames or passwords.
**Database**
This project uses a SQLite database named totally_not_my_privateKeys.db.
The database contains a table called keys with three columns:
•	kid - A unique ID for each key.
•	key - The RSA private key stored as PEM data.
•	exp -The expiration time of the key.
The private keys are saved in PEM format so they can be stored and retrieved from SQLite.
I also used parameterized SQL queries when working with the database to help prevent SQL injection.
The database file is not uploaded to GitHub because it contains private keys.
Testing
I tested the server using Pytest and the Gradebot provided for this course.
Pytest Results
I ran the following command to test the application and check code coverage:
python -m pytest --cov=app --cov-report=term-missing
**Results:**
•	9 tests passed.
•	98% code coverage.
•	No failed tests.
**Gradebot Result**s
I also tested the server using the official Gradebot client.
On Windows, I ran:
.\gradebot.exe project-2 --run="python app.py"
The Gradebot results were:
**Test	Score**
Valid JWT authentication	15/15
Valid JWK in JWKS	20/20
SQLite database storage	15/15
Database queries	15/15
Code quality	4.25/5
Overall Gradebot score: 98.93%
The Gradebot results were successfully uploaded to the grading server.
**Screenshots**
I included screenshots of the Gradebot results and test coverage in the screenshots folder.
•	screenshots/gradebot-result.png – Gradebot results showing 98.93%.
•	screenshots/test-coverage.png – Pytest results showing 9 passed and 98% coverage.
**Conclusion**
In this project, I learned how to connect a Python Flask application to a SQLite database and store RSA private keys.
I also learned how to use parameterized SQL queries to help prevent SQL injection, generate JWT tokens using database-stored keys, and test a server using automated tests.
This project helped me understand how using a database makes a server more reliable by keeping important data available even after the application restarts.

