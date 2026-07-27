# Authentication Module

This module handles user security, password hashing, JWT creation/validation, and route authorization.

### Responsibilities:
- `hashing.py`: Passlib/bcrypt password hashing & verification utilities.
- `jwt_handler.py`: Generates and decodes signed JWT access tokens.
- `dependencies.py`: FastAPI `get_current_user` dependency for securing protected endpoints.
- `auth_service.py`: Business logic for user registration and authentication handling.
