virtual environment
python3 -m venv env
source env/bin/activate

django installation
pip install django


inventory_management/
│
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
├── README.md
│
├── inventory_management/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   ├── __init__.py
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands
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
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   └──forms.py
├── .gitignore
└── sitemap.json
