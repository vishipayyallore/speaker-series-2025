# Global AI Hyderabad - Monthly Online Event - Mar 2025

## Date Time: 23-Mar-2025 at 09:00 AM IST

## Event URL: [https://www.meetup.com/global-ai-hyderabad/events/306606120](https://www.meetup.com/global-ai-hyderabad/events/306606120)

## YouTube: [https://www.youtube.com/watch?v=RUeaM9Rix60](https://www.youtube.com/watch?v=RUeaM9Rix60)

<!-- ![Viswanatha Swamy P K |150x150](./Documentation/Images/ViswanathaSwamyPK.PNG) -->

---

### Software/Tools

> 1. OS: Windows 10/11 x64
> 1. Python / .NET 8
> 1. Visual Studio 2022
> 1. Visual Studio Code

### Prior Knowledge

> 1. Programming knowledge in C# / Python

## Technology Stack

> 1. .NET 8, AI, Open AI

## Information

![Information | 100x100](../Documentation/Images/Information.PNG)

## What are we doing today?

> 1. The Big Picture
> 1. SUMMARY / RECAP / Q&A

### Please refer to the [**Source Code**](https://github.com/Swamy-s-Tech-Skills-Academy/learn-ai-102-code) of today's session for more details

---

![Information | 100x100](../Documentation/Images/SeatBelt.PNG)

---

## 1. Introduction

> 1. Discussion and Demo

![Singl Turn Chat BOT](./Documentation/Images/STChatBOT.PNG)

## 2. Project Setup

> 1. Discussion and Demo
> 1. Create a virtual environment and install dependencies.

## 3. Folder Structure

- Explain the folder structure (briefly, using a simplified diagram).

```text
openai-chat-flask/
├── app.py                  # Application entry point
├── requirements.txt        # Dependencies
├── .env                    # Environment variables
├── README.md               # Documentation
└── website/                # Main Flask package
    ├── __init__.py         # App factory (configures app, database, registers blueprints)
    ├── data/               # Database-related code
    │   ├── __init__.py     # (Optional) Exposes models
    │   └── models.py       # SQLAlchemy models (e.g., ChatHistory)
    ├── api/                # API endpoints
    │   ├── __init__.py     # Imports blueprint from chat.py
    │   └── chat.py         # Chat API route that interacts with OpenAI
    ├── views/              # View (template) routes
    │   ├── __init__.py     # Imports blueprint from home.py
    │   └── home.py         # Routes for Home, ST Chat Bot, and History pages
    ├── static/             # Static assets (CSS, images)
    │   ├── favicon.ico
    │   └── globalstyles.css
    └── templates/          # Jinja2 templates
        ├── base.html       # Base layout (includes navbar and footer)
        ├── navbar.html     # Navbar (included in base.html)
        ├── Footer.html     # Footer (included in base.html)
        ├── home.html       # Home page overview
        ├── stchatbot.html  # Single Turn Chat Bot page (chat interface)
        └── history.html    # Search History page (placeholder or history display)
```

## 4. App Initialization

### 4.1. What Is an App Factory?

An app factory is a function (commonly named create_app()) that sets up and returns a fully configured Flask application instance. This pattern allows you to configure your application dynamically, register blueprints (which help separate different parts of your app), and initialize extensions (like SQLAlchemy) all in one place.

### 4.2. Role of app.py

app.py serves as the entry point of your application. Its main job is to call the app factory and start the server. This keeps the configuration logic (like registering blueprints, setting up the database, and loading environment variables) separate from the code that actually runs the server.

## 1. Blueprint Structure

- Explain how you separated view routes, API endpoints, and models.
- Walk through key files (e.g., `website/__init__.py`, `website/views/home.py`, and `website/api/chat.py`).

## 1. Running the App:

- Demonstrate starting the Flask app and navigating between routes (Home, ST Chat Bot, History).

## 1. Live Demo:

- Show the chat interface in action and interact with the OpenAI API.
- Optionally, discuss the benefits of the modular design.

## SUMMARY / RECAP / Q&A

> 1. SUMMARY / RECAP / Q&A
> 2. Any open queries, I will get back through meetup chat/twitter.

---
