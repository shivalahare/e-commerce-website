# e-commerce-website

This is a Django-based e-commerce-website.

## Installation

1. Create a Virtual Environment:
   For Ubuntu/Linux:
   ```bash
   sudo apt install python3-venv

   For Windows:
   ```bash
   python -m pip install --user virtualenv

2. Set up the Virtual Environment:
   For Ubuntu/Linux:
   ```bash
   python3 -m venv venv
   
   For Windows:
   ```bash
   python -m venv venv

3. Activate the Virtual Environment:
   For Ubuntu/Linux:
   ```bash
   source venv/bin/activate
   
   For Windows:
   ```bash
   venv\Scripts\activate
   
4. Clone the repository:
   ```bash
   git clone https://github.com/shivalahare/e-commerce-website.git
    
5. Navigate to the project directory:
    ```bash
    cd shop_platform
6. Install dependencies:
    ```bash
    pip install -r requirements.txt
    
7. Migrate Database:
    ```bash
    python manage.py makemigrations
8. Apply migrations:
    ```bash
    python manage.py migrate
9. Run the development server:
    ```bash
    python manage.py runserver    
## Usage
    Access the application at http://127.0.0.1:8000/.

## License
    This project is licensed under the MIT License.
