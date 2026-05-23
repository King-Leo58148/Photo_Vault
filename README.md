# Photo Vault

A Django REST API for managing and sharing photos securely. Users can upload, organize photos into albums, and control privacy settings with token-based authentication.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)

---

## Features

**User Authentication**
- User registration and login with token-based authentication
- Session and token-based authentication support
- Rate limiting on login endpoint (3 requests/minute)
- User logout functionality

**Photo Management**
- Upload photos with title, description, and privacy settings
- Organize photos into albums
- View personal and public photos
- Delete photos
- Cache photos for improved performance

**Privacy & Security**
- Private/Public photo visibility control
- User-specific photo access
- Token authentication for API requests
- Cloudinary integration for secure cloud storage

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Django 6.0 |
| API | Django REST Framework |
| Database | MySQL |
| Authentication | Token Authentication |
| Cache | Redis |
| Cloud Storage | Cloudinary |
| Environment | Python 3.x |

---

## Project Structure

```
Instagram/
├── manage.py
├── Pipfile
├── README.md
├── .env                     # Not committed — create locally
│
├── Instagram/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── photo_vault/
    ├── models.py
    ├── views.py
    ├── serializers.py
    ├── urls.py
    ├── admin.py
    ├── throttle.py
    ├── migrations/
    └── tests.py
```

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Redis Server

### Installation Steps

1. Clone the repository
```bash
git clone https://github.com/King-Leo58148/Photo_Vault.git
cd Photo_Vault
```

2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following values
```
SECRET_KEY=your-secret-key
DB_NAME=photo_vault
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=3306
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

5. Create the MySQL database
```sql
CREATE DATABASE photo_vault;
```

6. Run migrations
```bash
python manage.py migrate
```

7. Start Redis
```bash
redis-server
```

8. Run the development server
```bash
python manage.py runserver
```

Server runs on `http://localhost:8000/`

---

## API Endpoints

### Authentication

#### POST `/signup/`
Register a new user account.

Request body:
```json
{
  "username": "john_doe",
  "password": "securepass123",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

Response (201 Created):
```json
{
  "token": "abc123xyz789",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

---

#### POST `/login/`
Authenticate and get a token. Rate limited to 3 requests per minute.

Request body:
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```

Response (200 OK):
```json
{
  "token": "abc123xyz789",
  "message": "Login Successful"
}
```

---

#### POST `/logout/`
Logout and revoke token.

Headers:
```
Authorization: Token abc123xyz789
```

Response (200 OK):
```json
{
  "message": "Logged out Successfully"
}
```

---

### Photo Management

#### POST `/upload_photo/`
Upload a new photo.

Headers:
```
Authorization: Token abc123xyz789
```

Request body (multipart/form-data):
```
title: "My vacation"
description: "Beach photos from summer"
photo: <image_file>
private: true
album: null
```

Response (201 Created):
```json
{
  "id": 5,
  "user": 1,
  "title": "My vacation",
  "description": "Beach photos from summer",
  "photo": "https://cloudinary-url.com/...",
  "private": true,
  "album": null
}
```

---

#### GET `/list_photos/`
Get all photos for the authenticated user. Cached for 15 minutes.

Headers:
```
Authorization: Token abc123xyz789
```

Response (200 OK):
```json
[
  {
    "id": 1,
    "title": "Photo 1",
    "description": "Description",
    "photo": "https://cloudinary-url.com/...",
    "private": true,
    "album": null
  }
]
```

---

#### GET `/view_photo/<photo_id>/`
Get a specific photo. Cached for 15 minutes.

Headers:
```
Authorization: Token abc123xyz789
```

Response (200 OK):
```json
{
  "id": 1,
  "title": "My Photo",
  "description": "Description",
  "photo": "https://cloudinary-url.com/...",
  "private": true,
  "album": 2
}
```

---

#### GET `/public_photo/<photo_id>/`
View a public photo. No authentication required. Cached for 15 minutes.

Response (200 OK):
```json
{
  "id": 3,
  "title": "Public Photo",
  "private": false,
  "photo": "https://cloudinary-url.com/..."
}
```

---

#### GET `/all_public_photos/`
Get all public photos. No authentication required. Cached for 15 minutes.

Response (200 OK):
```json
[
  {
    "id": 3,
    "title": "Public Photo 1",
    "private": false
  }
]
```

---

#### DELETE `/delete_photo/<photo_id>/`
Delete a photo.

Headers:
```
Authorization: Token abc123xyz789
```

Response (202 Accepted):
```json
{
  "message": "photo deleted"
}
```

---

#### GET `/get_album/<album_name>/`
Get all photos in an album. Cached for 15 minutes.

Headers:
```
Authorization: Token abc123xyz789
```

Response (200 OK):
```json
[
  {
    "id": 1,
    "title": "Album Photo 1",
    "album": 2
  }
]
```

---

## Database Models

### CustomUser
Extends Django's AbstractUser with a unique email field.

- username: CharField
- password: CharField
- email: EmailField (unique)
- first_name: CharField
- last_name: CharField

### Album
Groups photos together.

- album_name: CharField (max 25 chars)

### Photo
Main model for storing photo metadata.

- user: ForeignKey(CustomUser, CASCADE)
- title: CharField (max 25 chars)
- description: TextField
- photo: ImageField (stored in Cloudinary)
- private: BooleanField (default: True)
- album: ForeignKey(Album, DO_NOTHING, nullable)

---

## Configuration

All sensitive values are stored in a `.env` file and loaded via `python-dotenv`. Never commit your `.env` file — it is included in `.gitignore`.

### Database
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

### Authentication
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}
```

### Caching (Redis)
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```

### Cloudinary Storage
```python
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
```

### Rate Limiting
- Login: 3 requests per minute
- Signup: 2 requests per minute

---

## Usage Examples

### Register and Login
```bash
# Signup
curl -X POST http://localhost:8000/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123","email":"john@example.com"}'

# Login
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass123"}'
```

### Upload and View Photos
```bash
# Upload photo
curl -X POST http://localhost:8000/upload_photo/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "photo=@/path/to/photo.jpg" \
  -F "title=My Photo" \
  -F "description=Beautiful sunset" \
  -F "private=true"

# List photos
curl -X GET http://localhost:8000/list_photos/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### View Public Photos
```bash
# All public photos
curl http://localhost:8000/all_public_photos/

# Specific public photo
curl http://localhost:8000/public_photo/3/
```

---

## Error Handling

| Status Code | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 202 | Accepted |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Server Error |

---

## License

This project is open source and available under the MIT License.
