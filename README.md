# Museum Chatbot

This project is a museum-themed chatbot web application built with Flask. It allows users to interact with a bot that responds in the persona of various artists and artworks. The bot's responses are generated using OpenAI's language models, and all conversations are stored in a local SQLite database. The app also includes admin features for viewing and downloading chat logs.

## Features
- Select artist and artwork personas
- Chat with the bot about artworks
- Store conversations in a database
- Admin login to view/download logs
- Contact form with email notifications
- Modern UI with images and styles

## Project Structure
```
app.py                # Main Flask application
chat_openai.py        # Bot response logic (OpenAI integration)
database.py           # Database models and setup
prompts.py            # Persona prompt generation
requirements.txt      # Python dependencies
instance/messages.db  # SQLite database
static/               # Images and CSS
templates/            # HTML templates
```

## Setup Instructions

### 1. Prerequisites
- Python 3.10+ (recommended)
- pip (Python package manager)
- (Optional) virtualenv for isolated environments

### 2. Installation
#### Windows, Linux, or MacOS
1. Clone or download this repository.
2. Open a terminal (Command Prompt/PowerShell on Windows, Terminal on Mac/Linux).
3. (Optional) Create and activate a virtual environment:
   - Windows:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration
- The app uses SQLite by default (no setup needed).
- For email features, update `MAIL_USERNAME` and `MAIL_PASSWORD` in `app.py` with your own Gmail credentials or use environment variables for security.
- OpenAI API integration: Ensure your API key is set in `chat_openai.py` or as an environment variable if required.


### 4. Running the App
- You can start the project in the VS Code terminal using:
  ```powershell
  py -m flask run
  ```
- After running the command, click the link shown in the terminal (usually `http://127.0.0.1:5000/`) to open the app in your browser.
- Alternatively, you can run:
  ```bash
  python app.py
  ```
- Visit `http://localhost:5000` in your browser.

### 5. Usage
- Select an artist and artwork to start chatting.
- Admins can log in at `/admin-login` to view/download chat logs.
- Use the contact form to send feedback (requires email setup).

## Project Permissions & Funding

- This project is funded by Hochschule Rhein-Waal (HSRW).
- Professor Kai Essig (HSRW) has full permission to make any changes to the project as needed for academic or research purposes.

## Project Motivation & Research Context

This project was developed as part of a Human-Computer Interaction (HCI) course at Hochschule Rhein-Waal (HSRW), Germany. The main research question addressed is:

> **How can AI chatbots in a contemporary art exhibition increase young visitors’ understanding of the stories behind artefacts?**

The core idea is to help visitors, especially young people, better understand abstract art by providing artist-driven explanations through an AI chatbot. In Germany, privacy and security are critical concerns, so the project was designed with awareness of data protection, contract rules, and regulatory requirements. This prototype serves as a proof-of-concept for exploring the intersection of AI, art, and visitor engagement in a secure and ethical manner.

## Why Fine-Tuning?

Fine-tuning was used in this project to improve the chatbot's ability to respond in the style and persona of specific artists and artworks. By training the language model on curated examples and prompts, the bot can:
- Provide more contextually relevant and engaging responses
- Reflect the unique voice and background of each artist
- Enhance the educational and interactive experience for museum visitors

Fine-tuning ensures that the chatbot is not just generic, but tailored to the museum's content and goals, making conversations more authentic and informative.

## Project Flow & Architecture

### Overview
The Museum Chatbot is a web-based application that guides users through a conversational experience centered on contemporary art. The flow is designed to be intuitive and privacy-conscious:

1. **User Registration**: Visitors enter their name and age to personalize the experience.
2. **Artist & Artwork Selection**: Users select an artist and then choose an artwork to explore.
3. **Chat Interaction**: The chatbot, powered by a fine-tuned AI model, responds in the persona of the selected artist, providing insights and stories about the chosen artwork.
4. **Conversation Logging**: All chat messages are securely stored in a local SQLite database. Only authorized admins can view or download logs.
5. **Admin Features**: Admins can log in to review conversations and download chat logs as PDFs for research or analysis.
6. **Contact & Feedback**: Users can send feedback via a contact form, which is delivered to the project team via email.

### Architecture Diagram

```
User Browser
    |
    v
Flask Web Server (app.py)
    |
    +---> Database (SQLite, database.py)
    |
    +---> OpenAI Integration (chat_openai.py)
    |
    +---> Prompt Generation (prompts.py)
    |
    +---> Email Notifications (Flask-Mail)
    |
    +---> Static Files (images, CSS)
    |
    +---> HTML Templates
```

### Security & Privacy Considerations
- User data is stored locally and not shared externally.
- Admin access is password-protected.
- No personal data is used for commercial purposes.
- The project is mindful of German privacy laws and regulations.

## Notes
- For production, consider using a production-ready server (e.g., Gunicorn) and secure your credentials.
- The app is cross-platform and works on Windows, Linux, and MacOS.
- Images and styles are in the `static/` folder; templates are in `templates/`.

## Summary

This prototype demonstrates how AI chatbots can enhance the museum experience by making abstract art more accessible and engaging, especially for young visitors. It is designed with privacy, security, and educational value in mind, and serves as a foundation for further research and development in human-computer interaction and digital museum experiences.

## Recommended Development Environment

- Visual Studio Code (VS Code) is recommended for development and running the project. The integrated terminal and debugging tools make it easy to manage and test the application.


## License
This project is for educational and non-commercial use. Hochschule Rhein-Waal and Professor Kai Essig have full rights to modify and use the project. Please credit the original authors if you use or modify it.
