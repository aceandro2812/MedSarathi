# MedSarthi Chatbot

## Overview
MedSarthi is a conversational AI chatbot. Users can ask questions on a variety of topics, and the chatbot will attempt to answer using its general knowledge.

## Features
*   **Conversational AI:** Utilizes Google's Generative AI (Gemini Pro) for natural language understanding and response generation.
*   **General Knowledge:** Answers are based on the model's general knowledge.
*   **Web Interface:** Simple and intuitive chat interface for user interaction.
*   **FastAPI Backend:** Built with FastAPI, providing a robust and efficient API.
*   **Langchain Framework:** Leverages Langchain for managing interactions with the language model, document loading, and vector storage.

## Project Structure
The project is organized into the following main directories:

*   `app/`: Contains the core backend logic.
    *   `main.py`: The main FastAPI application file, defining API endpoints and application startup.
    *   `chatbot.py`: Houses the logic for the conversational AI agent.
    *   `Indian_Food_Dataset.csv`: This file was previously used for a food dataset but is no longer part of the application.
*   `static/`: Contains static assets for the frontend.
    *   `css/style.css`: Custom CSS styles (if any).
    *   `js/script.js`: JavaScript for frontend interactivity (handling chat messages, API calls).
*   `templates/`: Contains HTML templates.
    *   `index.html`: The main HTML file for the chat interface.
*   `requirements.txt`: Lists all Python dependencies for the project.
*   `.env`: (To be created by the user) Stores environment variables, specifically the `GOOGLE_API_KEY`.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create and activate a virtual environment:**
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    *   Create a `.env` file in the root directory of the project.
    *   Add your Google API key to this file:
        ```env
        GOOGLE_API_KEY="YOUR_ACTUAL_GOOGLE_API_KEY_HERE"
        ```
        Replace `"YOUR_ACTUAL_GOOGLE_API_KEY_HERE"` with your valid Google API key.

## Running the Application

1.  Ensure you are in the root directory of the project (where the `app` directory and `requirements.txt` are located) and your virtual environment is activated.

2.  Run the FastAPI server using Uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```
    The `--reload` flag enables auto-reloading when code changes, which is useful for development.

3.  Open your web browser and navigate to:
    [http://127.0.0.1:8000](http://127.0.0.1:8000)

## How to Use
Once the application is running and you have opened it in your browser:
1.  You will see a chat interface.
2.  Type your question or message into the input field at the bottom of the chat window.
3.  Press "Send" or hit the "Enter" key.
4.  The chatbot will process your request, and its response will appear in the chat window.
5.  You can continue the conversation by typing more messages. The chatbot will use the history of the current session to maintain context.

Example questions:
*   "What is the capital of France?"
*   "Explain the theory of relativity in simple terms."
*   "Suggest a good book to read."
