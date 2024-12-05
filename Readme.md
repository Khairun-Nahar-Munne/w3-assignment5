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
- **Localise Accomodation**: Handle language detection in property description
- **Location Management**: Store and manage location Information
- **Database Partition**: Provide partitioned database of accomodation and localise accomodation.

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
   cd InventoryManagement 
   docker build
   docker up
   ```
5. PgAdmin Set Up:

   ```
   - Launch pgAdmin on http://localhost:5050 in your browser.

   - Provide Admin Email: admin@admin.com and Password: admin

   - Right-click on "Servers" > Click on "Register" > "Server".

   -Fill in the details:

      General Tab:
      Name your connection: InventoryDB

      Connection Tab:
      Host: db
      Port: 5432 
      Maintenance Database: postgres.
      Username: knm
      Password: knm123

   ```
### Running the Application


1. Apply migrations:
   ```bash
   docker exec -it InventoryManagement python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   docker exec -it InventoryManagement python manage.py createsuperuser

   username: admin
   email: admin@gmail.com
   password: admin123
   ```

3. Start the development server:
   ```
   - Put `http://localhost:8000/admin/` in your browser
   ```
4. Login as an Admin:

    ```bash
   username: admin
   password: admin123
   ```

5. Make a csv file:
   ```
   ```

6. Location Model:
   ```
   - Location> Click On Impost CSV file> Import CSV file > Submit

   - You can also add location manually by clicking on add option.
   ```
7. Create Property Owner Group:
    ```bash
   docker exec -it inventory_management_app python manage.py create_property_owner_group

   ```
7. Signup as a Property Owner:

    ```bash
   username: your username
   email: your email
   first name: your first name
   last name: your last name
   password: your password
   ```

4. Login as an Admin:

    ```bash
   - 
   ```
6. Accomodation Model:
   ```
   - Location> Click On Impost CSV file> Import CSV file > Submit

   - You can also add location manually by clicking on add option.
   ```
6. Localise Model:
   ```
   - Location> Click On Impost CSV file> Import CSV file > Submit

   - You can also add location manually by clicking on add option.
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