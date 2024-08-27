# Football Data Web Application

A Django web application providing up-to-date football information on leagues, teams, players, and fixtures.

## Screenshots

<p align="center">
  <img src="https://github.com/user-attachments/assets/996019c7-ade5-4831-858b-f33f54502770" width="600" alt="Home">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/e6ea85ad-93ca-48e1-b055-83f9f9e2ab9f" width="45%" alt="Leagues">
  <img src="https://github.com/user-attachments/assets/604d2957-e68e-43c8-9cca-49e9076b6e96" width="45%" alt="Teams">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/d83f12fd-1429-4552-bc9c-8c04854ddfb7" width="45%" alt="Players">
  <img src="https://github.com/user-attachments/assets/77edc361-c0f2-4bff-8397-3a931fefeb9b" width="45%" alt="Fixtures">
</p>

## Features
- Browse leagues, teams, and players
- View fixtures and results
- Responsive design
- Regular data updates via API

## Setup
1. Clone the repo: `git clone [repository-url]`
2. Navigate to the project directory: `cd [project-name]`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create a `.env` file in the project root and add necessary environment variables
7. Create migrations: `python manage.py makemigrations`
8. Apply migrations: `python manage.py migrate`
9. Create a superuser: `python manage.py createsuperuser`
10. [Optional for development] Collect static files: `python manage.py collectstatic`
11. Start the development server: `python manage.py runserver`

## Usage
Visit `http://localhost:8000` to use the application.
Update data: `python manage.py update_football_data`
