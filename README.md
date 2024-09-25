# e-commerce-website

This is a Django-based e-commerce website.

## Installation

### Create a Virtual Environment

For Ubuntu/Linux:
1. Install the virtual environment package:
   `sudo apt install python3-venv`
   
2. Create a virtual environment:
   `python3 -m venv venv`

For Windows:
1. Install `virtualenv`:
   `python -m pip install --user virtualenv`
   
2. Create a virtual environment:
   `python -m venv venv`

### Activate the Virtual Environment

For Ubuntu/Linux:
   `source venv/bin/activate`

For Windows:
   `venv\Scripts\activate`

### Clone the Repository
   `git clone https://github.com/shivalahare/e-commerce-website.git`

### Navigate to the project directory
   `cd e-commerce-website`

### Install dependencies
   `pip install -r requirements.txt`

### Migrate the Database

1. Create migrations:
   `python manage.py makemigrations`
   
2. Apply migrations:
   `python manage.py migrate`

### Run the Development Server
   `python manage.py runserver`

## Usage
   Access the application at `http://127.0.0.1:8000/`.

## License
   This project is licensed under the MIT License.
