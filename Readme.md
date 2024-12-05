# inventory-management

Inventory Management is a Django application. It is designed to store and manage property information efficiently. It utilizes Django's powerful admin interface for CRUD operations and includes custom models to handle various aspects of property data, such as images, locations, and amenities.


## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Prerequisites](#prerequisites)
4. [Project Structure](#project-structure)
5. [Getting Started](#getting-started)
   - [Installation](#installation)
   - [Database Schema](#database-schema)
   - [Running the Application](#running-the-application)
   - [Access Point](#access-point)
   - [Command Line Utility for Sitemap Generation](#comand-line-utility-for-sitemap-generation)
6. [Testing Instructions](#testing-instructions)
   - [Test](#test)
   - [Test Coverage](#test-coverage)
7. [Contributing](#Contributing)                                  


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
└── requirements.txt
```



## Getting Started

### Installation

1. Clone the repository:
   ```bash
   - git clone https://github.com/Khairun-Nahar-Munne/w3-assignment5.git
   - cd w3-assignment5
   ```

2. Set up a virtual environment:
   ```bash
   - python3 -m venv env 
   - source env/bin/activate   # On Windows use `source .env/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Docker Set Up:
   ```bash
   - cd InventoryManagement 
   - docker build
   - docker up
   ```
5. PgAdmin Set Up:

   ```
   - Launch pgAdmin on http://localhost:5050 in your browser.

   - Provide Admin Email: admin@admin.com and Password: admin

   - Right-click on "Servers" > Click on "Register" > "Server".

   - Fill in the details:

      General Tab:
      Name your connection: InventoryDB

      Connection Tab:
      Host: db
      Port: 5432 
      Maintenance Database: postgres.
      Username: knm
      Password: knm123

   ```
### Database Schema

The project includes the following models:

1. Location Model
2. Accomodation Model
3. Localise Accomodation Model

### Running the Application


1. Apply migrations:
   ```bash
   docker exec -it inventory_management_app python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   docker exec -it inventory_management_app python manage.py createsuperuser

   username: your admin username
   email: your email
   password: your admin password
   ```

3. Start the development server:
   ```
   Access Admin Panel on `http://localhost:8000/admin/`
   ```
4. Login as an Admin:

    ```bash
   username: your admin username
   password: your admin password
   ```

5. Make a csv file:
   ```
   - Open a text editor > put the below data into the file> save it with extention .csv
   

   - Data:

   title,center,parent_id,location_type,country_code,state_abbr,city
   1,India,POINT(78.9629 20.5937),,country,IN,, 
   2,Karnataka,POINT(75.7139 15.3173),1,state,IN,KA, 
   3,Maharashtra,POINT(75.7139 19.7515),1,state,IN,MH, 
   4,Bangalore,POINT(12.9716 77.5946),2,city,IN,KA,Bangalore
   5,Mumbai,POINT(19.0760 72.8777),3,city,IN,MH,Mumbai
   6,Pune,POINT(18.5204 73.8567),3,city,IN,MH,Pune

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

   Access Signup Page on http://localhost:8000/app/signup/ 

   username: your username
   email: your email
   first name: your first name
   last name: your last name
   password: your password
   ```

7. Active Status:

    ```bash
   Log in as admin > Click on User > Click on Status > Save > Log Out
   ```

4. Login as a Property Owner:

    ```bash
   username: your username
   password: your password
   ```
6. Accomodation Model:
   ```
   - Click Accomodation > Put Necessary Data> Save

   - Amenities Field Data:

   [
    "Free Wi-Fi",
    "Air Conditioning",
    "Swimming Pool",
    "Pet-Friendly",
    "Room Service",
    "Gym Access"
   ]

   - Image Field Data: 

   https://example.com/image.jpg,https://example.com/image2.png

   - Other users can not view your property except admin 
   ```
6. Localise Accomodation Model:
   ```
   - Click Localise Accomodation > Put Necessary Data> Save

   - Policy Feild Data: 

   [  {"pet_policy": "Pets are not allowed."},
      {"smoking_policy": "Smoking is prohibited indoors."}
   ]

   - You have to put Correct language code in which you write the desciption
   ```

### Access Point 

   1. Access Homepage `http://localhost:8000/app`

   2. Access Signup Page `http://localhost:8000/app/signup/`

   3. Access the admin panel at `http://localhost:8000/admin/` and log in with your superuser credentials.


### Command Line Utility for Sitemap Generation

To generate a sitemap.json file for all country locations. Sitemap will be generate for basic regions: Country, State and City.

```bash
docker exec -it inventory_management_app  python manage.py generate_sitemap
```

## Testing Instructions

### Test

   ```
   docker exec -it inventory_management_app  python manage.py test
   ```

### Test Coverage
   ```
   docker exec -it inventory_management_app coverage run manage.py test
   docker exec -it inventory_management_app coverage report
   docker exec -it inventory_management_app coverage html
   ```

   Open the `htmlcov/index.html` file in a web browser to view the detailed coverage report.

## Contributing
Contributions are welcome! Here's how you can contribute:

### Fork the Repository
```bash
- git clone https://github.com/Khairun-Nahar-Munne/hotel-management-system.git
- cd hotel-management-system
```
### Create a New Branch

```bash
- git checkout -b feature/add-new-feature
```
### Make Modifications and Commit Changes
```bash
- git commit -m 'Add new feature: [brief description of the feature]'

```
### Push Changes to the Branch

```bash
- git push origin feature/add-new-feature

```
### Create a New Pull Request
- Navigate to the repository on GitHub.
- Click on the "Compare & pull request" button.
- Fill in the pull request details and submit it for review.