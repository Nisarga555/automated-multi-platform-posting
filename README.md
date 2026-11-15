
# AutoPostHub – Automated Multi-Platform Posting System

## Project Overview
AutoPostHub is a Python-based application that allows users to publish a single message across multiple social media platforms through one API request.

## Technologies Used
- Python 3
- FastAPI
- Uvicorn
- Pydantic
- HTTPX
- Pytest

## Supported Platforms
1. Mastodon
2. Bluesky
3. Reddit
4. Telegram
5. Discord

## Features
- Single API endpoint for posting messages.
- Message validation with a 200-character limit.
- Exactly one CTA URL required.
- Independent publishing across platforms.
- Platform-specific success and failure responses.
- Error handling for failed publishing attempts.

## Project Structure
```text
automated-posting/
├── app/
│   ├── platforms/
│   ├── services/
│   ├── config.py
│   ├── main.py
│   └── schemas.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file using `.env.example` as a template.
5. Add your platform credentials to `.env`.

## Run the Application

```bash
uvicorn app.main:app --reload --port 4000
```

## API Documentation

Open:

http://127.0.0.1:4000/docs

## Run Tests

```bash
python -m pytest -v
```

## Security
API credentials are stored in environment variables and must never be committed to GitHub.

## Author
Developed as a Python practical assessment project.
