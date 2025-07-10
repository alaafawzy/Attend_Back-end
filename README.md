# College Attendance Management System

A clean, modular **College Attendance Management System** built with Django to streamline student attendance tracking for colleges and academies. It supports **multiple authentication methods (cookie-based sessions and JWT)**, enabling secure, flexible access from web dashboards and mobile apps.

## 🚀 Features

✅ **Multi-Authentication Support**
- Cookie-based authentication for web dashboards.
- JWT-based authentication for mobile and API usage.

✅ **Role-Based Access Control**
- Roles: Admin, Teacher, Student.
- Tiered permissions with secure user management.

✅ **Course and Session Management**
- Create/manage courses and sessions.
- Assign teachers and students to courses.
- Schedule sessions with automatic attendance tracking.

✅ **Attendance Tracking**
- Teachers can mark attendance in real-time.
- View attendance by course, session, and student.
- Attendance statistics for monitoring participation.

✅ **Secure User Management**
- User registration with random password generation.
- Profile update, password change, and reset endpoints.

✅ **RESTful API Design**
- Clean, extendable structure for mobile app integration.
- Supports pagination and filtering for scalable data handling.

✅ **Clean Codebase**
- Django best practices with modular, reusable apps.
- Structured serializers for clean API responses.

---

## 🛠 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/college-attendance.git
cd college-attendance
```

### 2️⃣ Create and activate a virtual environment:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Install required libraries:
```bash
pip install -r requirements.txt
```