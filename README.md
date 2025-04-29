# LangGraph Message Processor

A natural language processing system that uses LangGraph for intent-based routing to handle various types of requests.

## Features

- **Question Answering**: Get responses to your inquiries
- **Code Operations**: Generate and edit code across different programming languages
- **Text Operations**: Create and modify text content including creative writing

## Project Structure

```
.
├── Dockerfile
├── LICENSE
├── README.md
├── agent
│   ├── __init__.py
│   ├── config.py
│   ├── main.py # main fuction 
│   ├── nodes
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── code_processor.py
│   │   ├── intent_classifier.py
│   │   ├── question_handler.py
│   │   ├── response_generator.py
│   │   └── text_processor.py
│   └── utils
│       ├── __init__.py
│       ├── file_utils.py
│       ├── llm.py
│       ├── router.py
│       └── state.py
├── configs.yaml # configs
├── requirements.txt
└── run.py #runer of agent
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Option 1: Local Installation

1. Clone the repository
   ```bash
   git clone git@github.com:GoshKolotyan/Agentic-System.git
   cd Agentic-System
   ```

2. Create a virtual environment
   ```bash
   python -m venv agent-venv
   ```

3. Activate the virtual environment
   - On Windows:
     ```bash
     agent-venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source agent-venv/bin/activate
     ```

4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Docker

1. Build the Docker image
   ```bash
   docker build -t agent-image .
   ```

2. Run the container
   ```bash
   docker run -p 8000:8000 agent-image
   ```

**Note:**
Add your OPEN_AI_KEY like this
```bash
export OPEN_AI_KEY='your key'
```

## Usage

### Running the Application

```bash
python run.py
```

### Example Requests

1. **Question Answering**
   ```
   What is DNA?
   ```

2. **Code Generation**
   ```
   create a C loop that counts from 1 to 10 and save in loop.c
   ```

3. **Code Editing**
   ```
   Fix the bugs in this Python script:
   ```python
   def greet(name):
   if name == "":
       return "Hello, stranger!"
   else
       return "Hello, " + name + "!"
   # Test the function
   print(greet("Bob"))
   print(greet(""))
   ```
   ```

4. **Text Generation**
   ```
   Generate a short novel about Bernard Riemann
   ```

5. **Text Editing**
   ```
   Edit this text for me: The quik brown foxes jumps over the lasy dog and the moon is made of green cheese.
   ```
