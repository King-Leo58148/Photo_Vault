# Photo Vault ??

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

? **User Authentication**
- User registration and login with token-based authentication
- Session and token-based authentication support
- Rate limiting on login endpoint (5 requests/minute)
- User logout functionality

?? **Photo Management**
- Upload photos with title, description, and privacy settings
- Organize photos into albums
- View personal and public photos
- Delete photos
- Cache photos for improved performance

?? **Privacy & Security**
- Private/Public photo visibility control
- User-specific photo access
- Token authentication for API requests
- Cloudinary integration for secure cloud storage

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Django 6.0 |
| **API** | Django REST Framework |
| **Database** | MySQL |
| **Authentication** | Token Authentication |
| **Cache** | Redis |
| **Cloud Storage** | Cloudinary |
| **Environment** | Python 3.x |

---

## Project Structure

```
Instagram/
+-- manage.py                 # Django CLI
+-- Pipfile                   # Dependency management
+-- README.md                 # This file
¦
+-- Instagram/               # Project settings
¦   +-- settings.py          # Django configuration
¦   +-- urls.py              # Root URL configuration
¦   +-- wsgi.py              # WSGI application
¦   +-- asgi.py              # ASGI application
¦
+-- photo_vault/             # Main application
    +-- models.py            # Database models
    +-- views.py             # API endpoints
    +-- serializers.py       # DRF serializers
    +-- urls.py              # App URL routes
    +-- admin.py             # Django admin
    +-- throttle.py          # Rate limiting
    +-- migrations/          # Database migrations
    +-- tests.py             # Test suite
```

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Redis Server

### Installation Steps

1. **Clone the repository**
   ```bash
   cd Instagram
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # OR if using Pipfile
   pipenv install
   ```

3. **Create .env file** in project root
   ```env
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

4. **Configure MySQL Database**
   - Update `Instagram/settings.py` with your database credentials
   - Default: `photo_vault` database, `root` user

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start Redis Server**
   ```bash
   redis-server
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```
   Server runs on `http://localhost:8000/`

---

## API Endpoints

### Authentication Endpoints

#### **POST** `/signup/`
Register a new user account.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepass123",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
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

#### **POST** `/login/`
Authenticate user and get token. *Rate limited: 5 requests/minute*

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "token": "abc123xyz789",
  "message": "Login Successful"
}
```

---

#### **POST** `/logout/`
Logout user and revoke token.

**Headers:**
```
Authorization: Token abc123xyz789
```

**Response (200 OK):**
```json
{
  "message": "Logged out Successfully"
}
```

---

### Photo Management Endpoints

#### **POST** `/upload_photo/`
Upload a new photo.

**Headers:**
```
Authorization: Token abc123xyz789
```

**Request Body (multipart/form-data):**
```
title: "My vacation"
description: "Beach photos from summer"
photo: <image_file>
private: true
album: null  (optional, album ID)
```

**Response (201 Created):**
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

#### **GET** `/list_photos/`
Get all photos for authenticated user. *Cached for 15 minutes*

**Headers:**
```
Authorization: Token abc123xyz789
```

**Response (200 OK):**
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

#### **GET** `/view_photo/<photo_id>/`
Get a specific photo. *Cached for 15 minutes*

**Headers:**
```
Authorization: Token abc123xyz789
```

**Response (200 OK):**
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

#### **GET** `/public_photo/<photo_id>/`
View a public photo (no authentication required). *Cached for 15 minutes*

**Response (200 OK):**
```json
{
  "id": 3,
  "title": "Public Photo",
  "private": false,
  "photo": "https://cloudinary-url.com/..."
}
```

---

#### **GET** `/all_public_photos/`
Get all public photos. *Cached for 15 minutes*

**Response (200 OK):**
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

#### **DELETE** `/delete_photo/<photo_id>/`
Delete a photo.

**Headers:**
```
Authorization: Token abc123xyz789
```

**Response (202 Accepted):**
```json
{
  "message": "photo deleted"
}
```

---

#### **GET** `/get_album/<album_name>/`
Get all photos in an album. *Cached for 15 minutes*

**Headers:**
```
Authorization: Token abc123xyz789
```

**Response (200 OK):**
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
Extends Django's AbstractUser with unique email field.
```python
- username: CharField
- password: CharField
- email: EmailField (unique)
- first_name: CharField
- last_name: CharField
```

### Album
Groups photos together.
```python
- album_name: CharField (max 25 chars)
```

### Photo
Main model for storing photo metadata.
```python
- user: ForeignKey(CustomUser, CASCADE)
- title: CharField (max 25 chars)
- description: TextField
- photo: ImageField (stored in Cloudinary)
- private: BooleanField (default: True)
- album: ForeignKey(Album, DO_NOTHING, nullable)
```

---

## Configuration

### Important Settings (Instagram/settings.py)

**Database Configuration:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'photo_vault',
        'USER': 'root',
        'PASSWORD': 'louis@2007',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
```

**Authentication:**
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

**Caching (Redis):**
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
    }
}
```

**Cloudinary Storage:**
```python
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
```

**Rate Limiting:**
- Login endpoint: 5 requests per minute per IP

---

## Usage Examples

### Example 1: Register and Login
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

### Example 2: Upload and View Photos
```bash
# Upload photo
curl -X POST http://localhost:8000/upload_photo/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "photo=@/path/to/photo.jpg" \
  -F "title=My Photo" \
  -F "description=Beautiful sunset" \
  -F "private=true"

# List user's photos
curl -X GET http://localhost:8000/list_photos/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Example 3: View Public Photos
```bash
# Get all public photos (no token required)
curl http://localhost:8000/all_public_photos/

# Get specific public photo
curl http://localhost:8000/public_photo/3/
```

---

## Error Handling

All endpoints return standard HTTP status codes:
- **200** - OK
- **201** - Created
- **202** - Accepted
- **400** - Bad Request
- **401** - Unauthorized
- **404** - Not Found
- **429** - Too Many Requests (Rate Limit)
- **500** - Server Error

---

## License

This project is open source and available under the MIT License.

---

**Last Updated:** December 26, 2025
