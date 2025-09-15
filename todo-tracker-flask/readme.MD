# Todo Tracker ✅

A **Flask-based Todo Tracker** web app to manage daily tasks, track progress, and maintain a task history.  
It allows adding, updating, deleting tasks, and marking them complete on a daily basis — with progress tracking.

---

## 🚀 Features

- Add new tasks  
- Prevent duplicate tasks  
- Update / edit task names  
- Delete tasks  
- Track task completion on a daily basis  
- View history of tasks across multiple days  
- Visualize daily progress (percentage of tasks completed)  
- Task persistence using a database  

---

## 🛠 Tech Stack

- **Backend**: Flask (Python)  
- **Database**: SQLAlchemy ORM (with Day, Tasks, TaskStatus models)  
- **Frontend**: HTML + Jinja templates (index, edit, update, etc.)  

---

## 📂 Routes Overview

### Home
- `/` → Show all tasks, daily progress %, and task history  

### Task Management
- `/task/add` → Add a new task  
- `/task/save` → Save today's completed tasks  
- `/task/edit` → View all tasks and edit options  
- `/task/update/<task_id>` → Update a task name  
- `/task/delete/<task_id>` → Delete a task  

---

## 🏗 Database Models (from `app/models/tasks.py`)

- **Tasks** → Stores task names  
- **Day** → Stores calendar days  
- **TaskStatus** → Stores whether a task was completed on a specific date  

---

## 📋 Requirements

Dependencies are listed in [`requirements.txt`](requirements.txt).  
Install them with:

```bash
pip install -r requirements.txt
