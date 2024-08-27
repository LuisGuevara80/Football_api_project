# Football Data Web Application

A Django web application providing up-to-date football information on leagues, teams, players, and fixtures.

## Features
- Browse leagues, teams, and players
- View fixtures and results
- Responsive design
- Regular data updates via API

## Setup
1. Clone the repo
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up `.env` file with your API key
5. Run migrations: `python manage.py migrate`
6. Start server: `python manage.py runserver`

## Usage
Visit `http://localhost:8000` to use the application.

Update data: `python manage.py update_football_data`
