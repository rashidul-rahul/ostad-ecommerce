# Ostad Ecommerce
Django Testing Application for OSTAD Pro Batch

## Prerequisites

- **Python 3.8+** installed on your system.
- **Git** (if you need to clone the repository).

## Setup Instructions

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Create a Python Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

#### On Linux/macOS:
```bash
python3 -m venv env
source env/bin/activate
```

#### On Windows:

```bash
py -3 -m venv env
env\Scripts\activate
```
### 3. Install Dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

Your requirements.txt contains:

```bash
django==4.2
django-restframework
djangorestframework-simplejwt
```

### 4. Apply Migrations

Set up your database by applying migrations:
```bash
python manage.py migrate
```

### 5. Run the Development Server

Start the Django development server:
```bash
python manage.py runserver
```

Now, you can access the application by navigating to http://127.0.0.1:8000/ in your web browser.

### Additional Information

#### Debug Mode: This project is configured with DEBUG=True for development purposes. Remember to disable debug mode and use environment variables for sensitive information (like the secret key) in production.
#### Custom User Model: The project uses a custom user model defined in users.User. Ensure that this is correctly set up in your app configuration.
#### Static & Media Files: Static files are served from the static/ directory and collected in staticfiles/. Media files are served from the media/ directory.

**Note:** Feel free to customize these instructions according to your project’s specific needs.
