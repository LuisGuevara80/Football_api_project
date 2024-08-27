# Football Data Web Application

A Django web application providing up-to-date football information on leagues, teams, players, and fixtures.
![Home](https://github.com/user-attachments/assets/996019c7-ade5-4831-858b-f33f54502770)
![Leagues](https://github.com/user-attachments/assets/e6ea85ad-93ca-48e1-b055-83f9f9e2ab9f)
![Teams](https://github.com/user-attachments/assets/604d2957-e68e-43c8-9cca-49e9076b6e96)
![Players](https://github.com/user-attachments/assets/d83f12fd-1429-4552-bc9c-8c04854ddfb7)
![Fixtures](https://github.com/user-attachments/assets/77edc361-c0f2-4bff-8397-3a931fefeb9b)

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
