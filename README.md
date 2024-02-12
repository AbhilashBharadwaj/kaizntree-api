# Kaizntree Inventory Dashboard API

This repository contains the Django RESTful API for the Kaizntree Inventory Dashboard, designed to manage and display inventory items in a dashboard as outlined in the provided Figma design.

## Features

- RESTful API endpoints to serve inventory data.
- Secure authentication for API access.
- Query parameters for advanced filtering.
- Unit tests for API validation.
- API documentation for easy consumption.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8+
- Django 3.2+
- Django REST Framework
- Uses SQLite for dev and PostgreSQL for PROD

## Setup and Installation

To set up the Kaizntree Inventory Dashboard API, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/AbhilashBharadwaj/kaizntree-api.git
```
2. Install requirements:
```bash
pip install -r requirements.txt
```
3. Apply Migrations:
```bash
python manage.py migrate
```

4. Create super-user:
```bash
python manage.py createsuperuser
```
7. Run server:
```bash
python manage.py runserver
```

## API Documentation
API documentation can be found at http://localhost:8000/swagger when the server is running. It provides detailed information on endpoint usage, query parameters, and response formats.


