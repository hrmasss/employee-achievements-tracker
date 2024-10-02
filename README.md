# Employee Achievement Tracker

Employee Achievement Tracker is a Django-based API that helps organizations manage and track employee achievements. It provides CRUD functionality for employees, departments, and achievements, along with user authentication and detailed API documentation.

## Features

-   **User Authentication**: Register and log in users.
-   **CRUD Operations**: Manage employees, departments, and achievements.
-   **Filtering and Pagination**: Easily filter and paginate employee lists.
-   **API Documentation**: Automatically generated API docs via Swagger and ReDoc.

---

## Project Setup

### Prerequisites

-   Python 3.x
-   [Poetry](https://python-poetry.org/docs/#installation)

### Installation

#### Step 1: Clone the Repository

```bash
git clone https://github.com/hrmasss/employee-achievements-tracker.git
cd employee-achievements-tracker
```

#### Step 2: Set Up the Environment

1. **Using Poetry** (Default):

    - Install dependencies:

        ```bash
        poetry install
        ```

    - Create and activate a virtual environment:

        ```bash
        poetry shell
        ```

2. **Using pip** (Alternative):

    - Install dependencies from `requirements.txt`:

        ```bash
        pip install -r requirements.txt
        ```

#### Step 3: Set Up Environment Variables

-   Copy the `.env.example` to `.env`:

    ```bash
    cp .env.example .env
    ```

-   Update the `.env` file with your environment variables.

#### Step 4: Set Up the Database

Run the following commands to apply migrations:

```bash
python manage.py migrate
```

#### Step 5: Run the Server

```bash
python manage.py runserver
```

---

## Project Structure

```
employee-achievements-tracker/
│
├── core/                     # Django project settings
│   └── ...
├── employee_tracker/          # Main app handling the API
│   ├── models.py              # Database models
│   ├── views.py               # API view logic
│   ├── serializers.py         # DRF serializers for data validation
│   └── ...
├── .env                       # Environment variables
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
├── README.md                  # Project README
├── pyproject.toml             # Poetry configuration file
├── requirements.txt           # Dependency list for pip
└── manage.py                  # Django management commands
```

---

## API Endpoints

-   **`/api/employees/`**: CRUD operations for employees
-   **`/api/departments/`**: CRUD operations for departments
-   **`/api/achievements/`**: CRUD operations for achievements
-   **`/api/register/`**: Register a new user
-   **`/api/login/`**: Log in a user
-   **`/api/logout/`**: Log out a user

### API Documentation

-   **Swagger UI**: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
-   **ReDoc**: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

---

## Testing

This project uses `coverage` to run tests and measure code coverage.

#### Run Tests

```bash
coverage run manage.py test
```

#### View Coverage Report

```bash
coverage report
```

To generate an HTML report:

```bash
coverage html
```

The report will be available in the `htmlcov/` directory.

---

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
