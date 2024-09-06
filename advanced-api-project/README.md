## Step 1: Install Django and Django REST Framework

# Install Django and DRF:
pip install django djangorestframework

# Create a Django Project:
django-admin startproject advanced_api_project

# Create a Django App:
cd advanced_api_project
python manage.py startapp api

# API Endpoints

- `GET /books/`: Retrieve all books.
- `GET /books/<id>/`: Retrieve a single book.
- `POST /books/create/`: Create a new book (authenticated users only).
- `PUT /books/<id>/update/`: Update a book (authenticated users only).
- `DELETE /books/<id>/delete/`: Delete a book (authenticated users only).

# Permissions

- Unauthenticated users can view book data.
- Authenticated users can create, update, and delete books.

## Testing Approach for API Endpoints

### Key Areas Covered:
- **CRUD Operations**: Tests verify that creating, retrieving, updating, and deleting books works as expected.
- **Filtering, Searching, and Ordering**: Ensures users can filter by title, search by author, and order by publication year.
- **Permissions**: Tests enforce that only authenticated users can modify book data, while unauthenticated users are restricted to read-only operations.

### Running Tests:
Execute the following command to run the tests:
```bash
python manage.py test api