# bcrypt Flask App

A simple Flask web application with user registration, login, animated welcome, and dashboard features.

## Features
- User registration and login with bcrypt password hashing
- Animated welcome page after login
- Dashboard with personalized avatar and logout
- Modern, interactive UI/UX

## Setup
1. Install dependencies:
   ```bash
   pip install flask bcrypt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Access in browser:
   - Registration: `http://127.0.0.1:5000/register`
   - Login: `http://127.0.0.1:5000/login`

## Folder Structure
- `app.py` — Main Flask application
- `templates/` — HTML templates
- `static/` — Static files (e.g., reg.mp4 for background video)

## Notes
- Make sure `reg.mp4` is in the `static` folder for background video.
- Dashboard shows the logged-in username and avatar.
- Logout securely ends the session.

---
Feel free to replicate the UI/UX in Go or Rust web frameworks!
