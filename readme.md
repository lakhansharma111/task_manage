# 🧾 Django Task Manager (REST API + CLI)

A complete **Task Management System** built using **Django REST Framework** with a powerful **Command-Line Interface (CLI)** for managing tasks directly from your terminal.

This project demonstrates clean code structure, full CRUD support, input validation, and persistent storage.

---

## 🚀 Features

### 🧩 REST API

* Create, Read, Update, Delete (CRUD) tasks
* Filter tasks by completion status, priority, and due date
* Mark tasks as complete/incomplete
* Assign and manage priority levels (`low`, `medium`, `high`)
* Fully persistent data (SQLite database)

### 💻 CLI Interface

* Interact with the system via `python manage.py taskcli`
* Perform all CRUD operations from the terminal
* Create and manage tasks quickly
* Display tasks in a clear, readable format
* Includes robust input validation and error handling

---

## ⚙️ Technologies Used

| Component         | Technology                |
| ----------------- | ------------------------- |
| Backend Framework | Django 5.x                |
| REST API          | Django REST Framework     |
| Database          | SQLite3 (default)         |
| CLI Tool          | Django Management Command |
| Language          | Python 3.8+               |

---

## 🧠 Business Logic

Each **Task** includes:

| Field         | Type      | Description                       |
| ------------- | --------- | --------------------------------- |
| `title`       | CharField | Title of the task (required)      |
| `description` | TextField | Optional details about the task   |
| `completed`   | Boolean   | Marks if task is completed or not |
| `priority`    | CharField | `low`, `medium`, or `high`        |
| `created_at`  | DateTime  | Automatically added timestamp     |
| `due_date`    | Date      | Optional due date for the task    |

---

## 📦 Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/django-task-manager.git
cd django-task-manager
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\\Scripts\\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Run the development server

```bash
python manage.py runserver
```

Visit 👉 **[http://127.0.0.1:8000/api/tasks/](http://127.0.0.1:8000/api/tasks/)** to view API output.
Interactive API docs are available at 👉 **[http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)** (if enabled).

---

## 🧩 REST API Endpoints

| Method      | Endpoint                      | Description             |
| ----------- | ----------------------------- | ----------------------- |
| `GET`       | `/api/tasks/`                 | List all tasks          |
| `POST`      | `/api/tasks/`                 | Create a new task       |
| `GET`       | `/api/tasks/{id}/`            | Retrieve a single task  |
| `PUT/PATCH` | `/api/tasks/{id}/`            | Update a task           |
| `DELETE`    | `/api/tasks/{id}/`            | Delete a task           |
| `POST`      | `/api/tasks/{id}/complete/`   | Mark task as complete   |
| `POST`      | `/api/tasks/{id}/incomplete/` | Mark task as incomplete |

### 🔍 Filtering

You can filter tasks using query parameters:

```
/api/tasks/?completed=true
/api/tasks/?priority=high
/api/tasks/?due_before=2025-11-10
/api/tasks/?due_after=2025-11-01
```

### 🧪 Example Request

**POST /api/tasks/**

```json
{
  "title": "Prepare project report",
  "description": "Write and review final report",
  "priority": "high",
  "due_date": "2025-11-06"
}
```

---

## 🧰 CLI Command Usage

You can manage tasks directly via the command line using the built-in Django command `taskcli`.

### General Syntax

```bash
python manage.py taskcli <action> [options]
```

### Actions Supported

| Action       | Description             |
| ------------ | ----------------------- |
| `list`       | Show all tasks          |
| `create`     | Create a new task       |
| `update`     | Update existing task    |
| `delete`     | Delete a task           |
| `complete`   | Mark task as complete   |
| `incomplete` | Mark task as incomplete |

---

### 💻 CLI Examples

#### List all tasks

```bash
python manage.py taskcli list
```

#### Create a new task

```bash
python manage.py taskcli create --title "Finish Django Project" --priority high --due_date 2025-11-10
```

#### Update a task

```bash
python manage.py taskcli update --id 1 --description "Refactor and add unit tests" --priority medium
```

#### Delete a task

```bash
python manage.py taskcli delete --id 2
```

#### Mark complete / incomplete

```bash
python manage.py taskcli complete --id 1
python manage.py taskcli incomplete --id 1
```

---

## ⚡ Error Handling

| Scenario                    | Example Message                                       |
| --------------------------- | ----------------------------------------------------- |
| Missing required title      | `Error: Title is required for creating a task.`       |
| Invalid date format         | `Error: Invalid due_date format. Use YYYY-MM-DD.`     |
| Missing ID on update/delete | `Error: Task ID (--id) is required to update a task.` |
| Task not found              | `Error: Task with ID 99 not found.`                   |
| Already completed           | `Error: Task #1 is already completed.`                |

---

## 🧩 Requirements

**requirements.txt**

```
Django>=4.2
djangorestframework>=3.14
django-filter>=23.0
```

---

## 🧪 Example Test Data

To add some test tasks quickly:

```bash
python manage.py shell
```

```python
from tasks.models import Task
from datetime import date, timedelta

Task.objects.create(title="Write documentation", description="Finalize README", priority="high", due_date=date.today() + timedelta(days=2))
Task.objects.create(title="Deploy app", description="Deploy to staging server", priority="medium")
Task.objects.create(title="Review PRs", description="Code review for pending pull requests", priority="low")
```

Then list them:

```bash
python manage.py taskcli list
```

---

## 📖 Assumptions

* No authentication required (for simplicity)
* SQLite database used for persistence
* CLI interacts with local database (not API)
* Follows PEP 8 standards and modular structure

---

## 🧩 Future Enhancements

* ✅ Add authentication (JWT-based)
* ✅ Add pagination & search
* ✅ Add export/import (CSV, JSON)
* ✅ Integrate frontend with React or Next.js

---

## 🧡 Author

**Developed by:** *Your Name / Your Company*
**Email:** [yourname@example.com](mailto:yourname@example.com)
**GitHub:** [@yourusername](https://github.com/yourusername)
