
# Museum Chatbot

Museum Chatbot is an interactive web application designed for museum visitors to explore artists and artworks, ask questions, and receive information through a conversational interface. The project features an admin panel, logging, and a modular architecture for easy maintenance and extension.

---

**Note:**
Kai Essig from Hochschule Rhein-Waal University has the right to update and use this project. This project was voluntarily provided for the Usability Lab.

---

## Features
- Interactive chatbot for museum visitors
- Information about artists and artworks
- Admin panel for managing content and logs
- User-friendly web interface
- Modular codebase (Flask, SQLite, OpenAI integration)

## Project Architecture

```
+-------------------+
|   User Interface  |
|  (HTML/CSS/JS)    |
+---------+---------+
          |
          v
+-------------------+
|      Flask App    |
|     (app.py)      |
+---------+---------+
          |
   +------+------+
   |             |
   v             v
[OpenAI API]  [SQLite DB]
(chat_openai) (database.py)
```

- **app.py**: Main Flask application, routing, and logic
- **chat_openai.py**: Handles communication with OpenAI API
- **database.py**: Manages SQLite database for messages/logs
- **prompts.py**: Stores prompt templates for the chatbot
- **static/**: Static files (images, CSS)
- **templates/**: HTML templates for the web interface

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/gulsumergin/museum_chatbot.git
   cd museum_chatbot
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your API keys and configuration.

## Usage
To run the application, use the following command in your terminal:
```
py -m flask run
```

The app will be available at http://127.0.0.1:5000/

## License & Rights
Kai Essig from Hochschule Rhein-Waal University has the right to update and use this project. This project was voluntarily provided for the Usability Lab.

---

For questions or contributions, please contact the repository owner.
