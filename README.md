# SSL_FINAL_QUEUE_SYSTEM
NITC
# SmartQueue

SmartQueue is a web-based queue management system built with Flask and MongoDB. It allows visitors to register for a numbered token, estimate an end time, and check token status while staff manage active queues through a protected dashboard.

## Features

- User registration with name, phone number, address, and date
- Automatic token-number assignment
- Five-minute estimated service slots
- Public token-status lookup
- Staff login and logout
- Staff dashboard with active, completed, and cancelled tokens
- Queue summary with average wait and fastest service times
- Done and cancel actions that reschedule remaining active tokens

## Technology

- Python 3.12
- Flask 3
- Flask-Login
- MongoDB and PyMongo
- HTML, CSS, JavaScript, and Bootstrap

## Project Structure

```text
SmartQueue-main/
├── app.py              # Flask application and routes
├── requirements.txt    # Python dependencies
├── README.md           # Project overview
├── INSTALL.md          # Installation and configuration guide
├── templates/
│   ├── index.html      # User, staff login, and status interface
│   ├── staff.html      # Staff dashboard
│   └── token.html      # Generated token page
└── static/
    ├── background.jpg
    ├── script.js
    └── style.css
```

## Quick Start

```bash
cd SmartQueue-main
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start MongoDB locally, create a staff account, and run the application:

```bash
python app.py
```

Open <http://127.0.0.1:5000>.

See [INSTALL.md](INSTALL.md) for MongoDB setup, staff-account creation, configuration, and troubleshooting.

## Staff Account

The staff collection is empty in a fresh database. Add an account with:

```bash
mongosh "mongodb://localhost:27017/smartqueue" --eval \
'db.staff.insertOne({username:"admin", password:"change-this-password"})'
```

The application compares passwords as plain text in the current implementation. Change the example password and do not use this application in production with real credentials unless passwords are hashed and application secrets are secured.

## API

### `GET /api/token_status/<token_number>`

Returns the token status for the current day.

Example response:

```json
{
  "token_number": 1,
  "status": "Active",
  "end_datetime": "2026-11-27 12:05:00",
  "end_time": "12:05:00"
}
```

## Security and Development Notes

- The Flask secret key and MongoDB connection settings are currently configured directly in `app.py`.
- Staff passwords are stored and compared as plain text.
- Flask debug mode is enabled only by the direct `python app.py` development entry point.
- This project is intended as a local demonstration; harden authentication and configuration before deployment.
