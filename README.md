# Project Name

A  real-time one-to-one chat application built with Django, Django Channels, WebSocket

---

## Overview

- Real-time chat application
- Built with Django & WebSockets
- Supports private messaging

---

## Features

### Authentication

- User Registration
- Login / Logout
- Only authenticated users can access chat
- LoginRequiredMixin for protected views

### Real-Time Chat

- WebSocket-based communication
- One-to-one private chat rooms
- Messages saved in database
- Real-time message broadcast

### Typing Indicator

- Shows "User is typing..."
- Debounced typing events
- Stops automatically after inactivity

### Online / Offline Status

- Real-time user presence tracking
- Broadcast user status to chat room

---

## Tech Stack

- Python 3
- Django
- Django Channels
- Redis (Channel Layer Backend)
- SQLite
- Bootstrap 5
- JavaScript (WebSocket)

---

## Project Structure

```bash

chat_app/
│
├── chat/                 # Chat application
│   ├── consumers.py       # WebSocket consumer logic
│   ├── views.py           # Chat & AJAX views
│   ├── models.py          # ChatRoom & Message models
│   ├── routing.py         # WebSocket URL routing
│   ├── urls.py            # App URLs
|   ├── utils.py           # Helper function file
|   ├── templates/
│       ├── user_list.html
|       ├── chat.html
│       ├── login.html
│       ├── register.html             
│
├── chat_app/
│   ├── asgi.py            # ASGI configuration
│   ├── settings.py        # Project settings
│   ├── urls.py            # Project URLs
│
├── templates/
│   ├── base.html
│   
│
└── README.md
```

## Local Installation & Setup
 
1) Clone Repository

```bash
   git clone <your-repo-url>
   cd chat_app
```

2) Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

```

3) Install Dependencies

```bash
pip install -r requirements.txt
```

4) Configure Redis

Make sure Redis is installed and running:

```bash
redis-server
```

Test Redis:
```bash
redis-cli ping
```

Should return:

```bash
PONG
```

5) Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

6) Run Development Server

```bash
python -m daphne -b 127.0.0.1 -p 8000 chat_app.asgi:application
```

Open:
```bash
http://127.0.0.1:8000/
```

## Environment Variables

Create a .env file and configure:

```bash
Create a .env file and configure:
```



