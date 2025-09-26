# Alerting & Notification Platform

A lightweight alerting and notification system that balances admin configurability with user control. This platform allows organizations to manage alerts effectively while ensuring users have control over their notification preferences.

## Features

### For Administrators
- **Alert Management**
  - Create unlimited alerts with customizable settings
  - Set severity levels (Info, Warning, Critical)
  - Configure visibility (Organization, Team, or User-specific)
  - Set start and expiry times
  - Archive outdated alerts
  
- **Analytics Dashboard**
  - Track total alerts created
  - Monitor alert delivery and read rates
  - View severity distribution
  - Track snooze patterns

### For End Users
- **Alert Reception**
  - Receive relevant alerts based on organization, team, and individual assignments
  - Automatic 2-hour reminders for unaddressed alerts
  - Clear alert status indicators (read/unread)

- **Alert Control**
  - Snooze alerts for the current day
  - Mark alerts as read/unread
  - View alert history

## Technical Features
- FastAPI-based REST API
- SQLAlchemy ORM with SQLite database
- Automated reminder system using APScheduler
- Comprehensive test suite
- Clean, modular architecture following OOP principles

## Setup & Installation

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn src.main:app --reload
```

## API Documentation

### Admin Endpoints
- `POST /admin/alerts` - Create a new alert
- `GET /admin/alerts` - List all alerts
- `PUT /admin/alerts/{alert_id}/archive` - Archive an alert

### User Endpoints
- `GET /user/alerts` - Get alerts visible to the user
- `GET /user/notifications` - Get user's notification history
- `POST /user/alerts/{alert_id}/read` - Mark alert as read
- `POST /user/alerts/{alert_id}/unread` - Mark alert as unread
- `POST /user/alerts/{alert_id}/snooze` - Snooze alert for the day

### Analytics Endpoints
- `GET /analytics/metrics` - Get system-wide metrics

For detailed API documentation, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
src/
├── api/                    # API routes and endpoints
│   ├── admin.py           # Admin endpoints
│   ├── user.py            # User endpoints
│   └── analytics.py       # Analytics endpoints
├── models/                # SQLAlchemy models
│   ├── enums.py          # Enumerations
│   └── models.py         # Data models
├── services/             # Business logic
│   ├── alert_service.py
│   ├── notification_service.py
│   └── user_preference_service.py
└── utils/               # Helper functions
    └── scheduler.py    # Reminder scheduler
tests/                  # Test files
```

## Testing

Run the test suite:
```bash
pytest
```

The test suite includes:
- Service layer tests
- API endpoint tests
- Integration tests

## Design Patterns Used

- **Strategy Pattern** - For notification delivery channels
- **Observer Pattern** - For alert subscription system
- **State Pattern** - For alert status management
- **Repository Pattern** - For data access abstraction

## Future Extensions

The system is designed to be extensible for:
- Additional notification channels (Email, SMS)
- Custom reminder frequencies
- Role-based access control
- Push notification integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT