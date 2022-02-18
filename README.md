# Interview evaluation

This is a test project for developer interviews.

## The structure:

The project consists of a test suite and a basic application skeleton.

Just open the router file and start implementing the API until all tests passes.

## Required code:

The application must implement a persistent storage and authentication with basic auth, including a persistent user storage.

Password verification must be included.

For passwords, I recommend you to use [PassLIB](https://passlib.readthedocs.io/en/stable/)

## Additional requirements:

For completeness, I left space to you to write some unit tests for your own implemented code. This will be also considered in the interview.

You'll gain bonus points if you reach 95% code coverage when testing the code. However, this is a minor requirement.

## If you cannot start the project:

Create a file called ".env" with this content:

```bash
PROJECT_NAME=testproject
BACKEND_CORS_ORIGINS=["http://localhost:8000", "https://localhost:8000", "http://localhost", "https://localhost"]


# These are not used, but you can use for the database connection:
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=database
POSTGRES_DB=app
```

## License

This project is licensed under the terms of the Apache license.
"# interview-evaluation" 
