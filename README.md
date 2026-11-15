# AutoPostHub – Automated Multi-Platform Posting System

## Project Overview

AutoPostHub is a Python-based application that allows users to submit one message through a single API request and attempt to publish it across five social media platforms.

The application uses FastAPI to receive requests, validates the message, and handles publishing independently for each supported platform.

## Technologies Used

- Python 3
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- HTTPX
- AT Protocol Python SDK
- Pytest

## Supported Platforms

1. Mastodon
2. Bluesky
3. Reddit
4. Telegram
5. Discord

## Features

- Single API endpoint for multi-platform posting.
- Maximum message length of 200 characters.
- Exactly one valid CTA URL is required.
- Independent publishing attempts across all five platforms.
- Platform-specific success and failure responses.
- Error handling to prevent one platform failure from stopping other publishing attempts.
- Environment-based credential configuration.

## Project Structure
automated-posting/
|-- app/
|   |-- platforms/
|   |   |-- base.py
|   |   |-- mastodon.py
|   |   |-- bluesky.py
|   |   |-- reddit.py
|   |   |-- telegram.py
|   |   |-- discord.py
|   |-- services/
|   |   |-- posting_service.py
|   |-- config.py
|   |-- main.py
|   |-- schemas.py
|-- tests/
|   |-- test_api.py
|-- .env.example
|-- .gitignore
|-- pytest.ini
|-- requirements.txt
|-- README.md
## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Nisarga555/automated-multi-platform-posting.git
cd automated-multi-platform-posting
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a template.

On Windows:

```powershell
Copy-Item .env.example .env
```

Add the required API credentials for each platform to the `.env` file.

**Important:** Never upload your `.env` file or expose your API credentials publicly.

## Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --port 4000
```

The application will run at:

`http://127.0.0.1:4000`

## API Documentation

Open the interactive Swagger documentation:

`http://127.0.0.1:4000/docs`

## API Endpoint

**POST** `/postingRequest`

### Sample Request

```json
{
  "message": "Check this out: https://example.com"
}
```

### Response Format

The API returns an overall success value and individual results for each platform.

Each platform result includes:

- `platform`
- `status`
- `posted_url`
- `public_access`
- `date`
- `time`
- `error`

If a platform is not configured or publishing fails, its individual result reports the failure.

The overall `success` value is `true` if at least one platform publishes successfully; otherwise, it is `false`.

## Validation Rules

- Message must not be empty.
- Message must not exceed 200 characters.
- Exactly one valid HTTP or HTTPS URL must be included.

Invalid requests return HTTP `422 Unprocessable Entity`.

## Run Tests

Execute the automated test suite:

```bash
python -m pytest -v
```

## Security

- Platform credentials are managed through environment variables.
- The `.env` file is excluded from Git tracking.
- Never commit access tokens, passwords, or webhook URLs to a public repository.

## Current Testing Status

- Home endpoint: Passed.
- Valid posting request: Passed.
- Invalid posting request: Passed.
- Manual API validation checks: Passed.
- Live publishing requires valid credentials for the respective platforms.

## Author

Developed as a Python practical assessment project.

**GitHub:** https://github.com/Nisarga555/automated-multi-platform-posting
