# 🔐 VaultKeeper

A secure web-based password manager built with Flask, SQLite, bcrypt, and cryptography.

VaultKeeper allows users to create accounts, securely store passwords, generate strong passwords, and manage their personal vault through a modern web interface.

---

## ✨ Features

- User Registration
- User Authentication
- Secure Login Sessions
- Password Encryption
- Password Decryption on Demand
- Password Generator
- Search Stored Passwords
- Edit Saved Entries
- Delete Entries
- SQLite Database
- Dark Mode UI
- Docker Support

---

## 🛠️ Technologies

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite
- bcrypt
- cryptography
- Bootstrap 5
- Docker

---

## 📂 Project Structure

```text
VaultKeeper/
│
├── app.py
├── models.py
├── config.py
├── crypto.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── add_password.html
│   └── edit_password.html
│
├── static/
│   └── style.css
│
└── instance/
    └── vault.db
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/VaultKeeper.git

cd VaultKeeper
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

## 🐳 Docker

Build image:

```bash
docker build -t vaultkeeper .
```

Run container:

```bash
docker run -d -p 5000:5000 --name vaultkeeper vaultkeeper
```

Application URL:

```text
http://localhost:5000
```

---

## 🔒 Security

### Password Hashing

User passwords are hashed using:

```text
bcrypt
```

and are never stored in plain text.

### Encryption

Vault entries are encrypted using:

```text
cryptography.Fernet
```

before being saved to the database.

---

## 📸 Current Features

✅ Registration

✅ Login

✅ Logout

✅ Password Vault

✅ Encryption & Decryption

✅ Password Generator

✅ Search Functionality

✅ Edit Entries

✅ Delete Entries

✅ Docker Deployment

✅ Dark Theme Interface

---






