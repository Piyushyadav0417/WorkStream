📌 ProjectManager – Project Collaboration Platform (Django REST Framework)
🚀 Overview

ProjectManager is a full-featured Project Collaboration & Task Management API, built with Django REST Framework.
It’s inspired by tools like Trello and Asana and demonstrates my ability to design and implement production-ready backend systems.

Key highlights:

Custom User Authentication with JWT

Role-based access control (RBAC) for Projects, Boards, and Tasks

Task assignments, comments, and notifications

Join requests & membership management

Razorpay integration (₹5 to create a new project)

Clean, modular, and scalable API design

🛠️ Tech Stack

Backend Framework: Django 5, Django REST Framework

Database: PostgreSQL / SQLite (dev)

Authentication: JWT (JSON Web Tokens)

Payments: Razorpay

Background Jobs: APScheduler / ThreadPoolExecutor

Frontend (Optional): Django Templates + Python requests

✨ Features
👥 User Management

Custom AbstractUser model

JWT-based authentication (register, login, logout)

📂 Projects & Memberships

Create projects (₹5 payment required)

Join requests (approve/reject)

Role-based permissions: Manager, Employee, Viewer

🗂️ Boards & Tasks

Boards → TaskLists → Tasks

Assign users to tasks

Add comments & threaded replies

Automatic notifications

🔒 Permissions

Project owners: full control

Task owners/assignees: limited control

Fine-grained access like industry tools

⚡ Background Processing

Long-running tasks handled via threads/APScheduler
