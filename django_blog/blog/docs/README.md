# Authentication System - django_blog


## Features
- User registration with username, email, password
- Secure login & logout using Django’s built-in system
- Profile page (view & update username/email)
- CSRF protected forms
- Passwords securely hashed by Django


## How to Test
1. Run `python3 manage.py runserver`
2. Visit `/register/` to create a new account
3. Visit `/login/` and `/logout/` for authentication
4. Visit `/profile/` (must be logged in) to update your account
5. Run `python3 manage.py test` for automated tests
