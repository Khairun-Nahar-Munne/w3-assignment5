# inventory-management

Inventory Management is a Django application. It is designed to store and manage property information efficiently. It utilizes Django's powerful admin interface for CRUD operations and includes custom models to handle various aspects of property data, such as images, locations, and amenities.


## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Prerequisites](#prerequisites)
4. [Project Structure](#project-structure)
5. [Getting Started](#getting-started)
   - [Installation](#installation)
   - [Database Configuration](#database-configuration)
   - [Running the Application](#running-the-application)
6. [Usage](#usage)
7. [Database Schema](#database-schema)


## Features

- **Property Management**: Store and manage detailed property information.
- **Image Handling**: 
- **Location Management**: 
- **Amenity Tracking**: 
- **Django Admin Interface**: 

## Technologies Used

- Backend: Python, Django
- Database: PostgreSQL
- ORM: Django ORM


## Prerequisites

Ensure you have the following installed:
- Python 3.x
- PostgreSQL
- Git
- Docker

## Project Structure

```plaintext
inventory_management/
│
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
├── README.md
├── sitemap.json
├── .coverage
│
├── inventory_management/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_partition_accommodation.py
│   │   └── _003_partition_localize_accommodation.py
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands
|   |       ├── __init__.py
│   │       ├── create_property_owner_group.py
│   │       └── generate_sitemap.py
│   ├── templates/
│   │   ├── signup.html
│   │   └── admin
│   │       ├── csv_import_form.html
│   │       └── app
│   │           └──location
│   │               └──change_list.html
│   │
│   ├── models.py
│   ├── test_forms.py
│   ├── test_localizedacco.py
│   ├── test_validators.py
│   ├── tests_views.py
│   ├── tests.py
│   ├── views.py
│   ├── validators.py
│   ├── urls.py
│   └──forms.py
├── .gitignore
└── sitemap.json
```
## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Khairun-Nahar-Munne/w3-assignment5.git
   cd w3-assignment5
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv env 
   source env/bin/activate   # On Windows use `source .env/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Docker Set Up:
   ```bash
   npm InventoryManagement 
   docker build
   docker up
   ```
### Database Configuration

1. Create a `config.py` file in the DjangoAssignment root directory and add your PostgreSQL credentials:

   ```python
   # config.py
   DB_USERNAME = 'your_username'
   DB_PASSWORD = 'your_password'
   DB_HOST = 'localhost'
   DB_PORT = 'port'
   DJANGO_DBNAME = 'django_project_database_name'
   SECRET_KEY = 'your SECRET_KEY'
   ```

2. Create a `.env` file in the DjangoAssignment root directory and add your PostgreSQL credentials:

   ```
      DB_USERNAME=your_username
      DB_PASSWORD=your_password
      DB_HOST=localhost
      DB_PORT=port
      DJANGO_DBNAME=django_project_database_name
      SECRET_KEY=your_SECRET_KEY
   ```

3. Ensure PostgreSQL is running and create the necessary databases:

```bash
   psql -U your_username
   CREATE DATABASE django_project_database_name;
```

### Running the Application

```bash
      docker-compose up --build -d
```
1. Apply migrations:
   ```bash
   docker exec -it InventoryManagement python manage.py makemigrations
   docker exec -it InventoryManagement python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   docker exec -it InventoryManagement python manage.py createsuperuser
   ```

3. Start the development server:
   ```bash
   docker exec -it inventoryManagement python manage.py runserver 0.0.0.0:8000
   ```


## Usage

1. `http://localhost:8000`

2. `http://localhost:8000/app/signup/`

3. Access the admin panel at `http://localhost:8000/admin/` and log in with your superuser credentials.


### Database Schema

The project includes the following models:

### Command-Line Utility for Sitemap Generation

To generate a sitemap.json file for all country locations.
```bash
      docker exec -it InventoryManagement python manage.py generate_sitemap
```

#### amenities field 
```
[
    "Free Wi-Fi",
    "Air Conditioning",
    "Swimming Pool",
    "Pet-Friendly",
    "Room Service",
    "Gym Access"
]
```
#### policy field
```
{
    "pet_policy": {
        "en": "Pets are not allowed.",
        "ar": "لا يُسمح بالحيوانات الأليفة."
    },
    "smoking_policy": {
        "en": "Smoking is prohibited indoors.",
        "ar": "التدخين ممنوع داخل المبنى."
    }
}
```


## Testing Instructions

   ```
   docker exec -it InventoryManagement pip install coverage
   docker exec -it InventoryManagement python manage.py test
   docker exec -it InventoryManagement coverage run manage.py test
   docker exec -it InventoryManagement coverage report

   docker exec -it inventoryManagement coverage html
   ```

   Open the `htmlcov/index.html` file in a web browser to view the detailed coverage report.







docker exec -it inventory_management_app python manage.py create_property_owner_group
    docker exec -it inventory_management_app python manage.py createsuperuser
docker exec -it inventory_management_app python manage.py generate_sitemap