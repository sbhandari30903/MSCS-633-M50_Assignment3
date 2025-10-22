# MSCS-633-M50_Assignment3

# Django + ChatterBot Terminal Chat Client

This project implements a simple terminal-based chatbot using **Django** (for environment configuration) and **ChatterBot** (for conversational AI).  
It is a lightweight, single-file implementation designed for easy setup and demonstration.

---

## Requirements

Create a file named `requirements.txt` with the following dependencies:

```
Django>=4.2,<5.1
chatterbot==1.2.8
chatterbot-corpus==1.2.2
SQLAlchemy>=2.0,<2.1
mathparse>=0.2,<0.3
python-dateutil>=2.8.2
pint>=0.20
spacy>=3.0.0
```

Install all dependencies:

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

Finally, install the required English model for spaCy:

```bash
python -m spacy download en_core_web_sm
```

---

## How to Run

### Step 1: Initial Training
Run the following command once to train the chatbot with default English corpora and a few custom responses:
```bash
python chatbot.py --fresh-train
```

### Step 2: Start Chatting
After the first training, you can start chatting any time:
```bash
python chatbot.py
```

### Step 3: Example Conversation
```
user: Good morning! How are you doing?
bot: I am doing very well, thank you for asking.
user: You're welcome.
bot: Do you like hats?
user: How do I exit?
bot: Type /quit and press Enter.
```

Use `/quit` or press `Ctrl + C` to exit the chat.

---

## Project Structure

```
chatbot.py          # Main and only Python file
requirements.txt    # Manifest file listing dependencies
README.md           # Project documentation
bot_db.sqlite3      # Auto-generated ChatterBot database (after training)
```

---

## Notes

- The chatbot uses Django only to initialize configuration; it does not create a web project.
- ChatterBot automatically creates and stores data in `bot_db.sqlite3`.
- If you want to reset training, simply delete `bot_db.sqlite3` and run with `--fresh-train` again.
- The model learns and stores responses between sessions.

---

## Deliverables

1. Python source file: `chatbot.py`  
2. Manifest file: `requirements.txt`  
3. Screenshot of terminal chat session (included in Word submission)  
4. GitHub repository link  


## Author Information

**Name:** Shimon Bhandari  
**Course:** MSCS-633-M50 – Artificial Intelligence  
**University:** University of the Cumberlands
