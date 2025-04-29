# **LangGraph Message Processor**
A natural language processing system that uses LangGraph for intent-based routing to handle various types of requests.
## **Features**
- **Question Answering**: Get responses to your inquiries
- **Code Operations**: Generate and edit code across different programming languages
- **Text Operations**: Create and modify text content including creative writing
## **Project Structure**
```
.
├── Dockerfile
├── LICENSE
├── README.md
├── agent
│ ├── __init__.py
│ ├── config.py
│ ├── main.py # main function
│ ├── nodes
│ │ ├── __init__.py
│ │ ├── analyzer.py
│ │ ├── code_processor.py
│ │ ├── intent_classifier.py
│ │ ├── question_handler.py
│ │ ├── response_generator.py
│ │ └── text_processor.py
│ └── utils
│ ├── __init__.py
│ ├── file_utils.py
│ ├── llm.py
│ ├── router.py
│ └── state.py
├── configs.yaml # configs
├── requirements.txt
└── run.py # runner of agent
```
## **Installation**
### **Prerequisites**
- Python 3.10 or higher
- pip package manager
### **Option 1: Local Installation**
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
### **Option 2: Docker**
1. Build and run using Docker Compose
 ```bash
docker-compose up
 ```

2. For detached mode and interactive access
 ```bash
docker-compose up -d
docker attach synopsis-langgraph-processor-1
 ```

**Note:**
Add your OpenAI API key as an environment variable
```bash
export OPENAI_API_KEY='your-api-key'
```

## **Usage**
### **Running the Application**
```bash
python run.py
```
### **Example Requests**
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