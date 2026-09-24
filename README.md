# AI Health Assistant

An AI-powered health and nutrition assistant that provides personalized diet recommendations and answers health & nutrition questions using **RAG (Retrieval-Augmented Generation)** and **GPT-OSS-120B**.

The application combines user health information, nutrition knowledge from a PDF knowledge base, FAISS vector search, Hugging Face embeddings, and an OpenAI-compatible Hugging Face API.

## Features

### Personalized Health Dashboard

The application calculates:

- BMI
- BMI Category
- BMR
- TDEE
- Daily Calorie Target
- Estimated Protein Target

Users can provide:

- Gender
- Age
- Weight
- Height
- Activity Level
- Health Goal
- Diet Type
- Food Allergies

### Diet Recommendations

The AI generates a personalized one-day diet plan containing:

1. Breakfast
2. Morning Snack
3. Lunch
4. Evening Snack
5. Dinner

Each meal includes:

- Food
- Portion
- Approximate Calories
- Approximate Protein

The recommendation considers the user's:

- Fitness goal
- Diet type
- Calorie target
- Protein target
- Food allergies
- Nutrition knowledge base

### AI Health Assistant

Users can ask natural-language questions about:

- Nutrition
- Protein
- Calories
- Vegetarian foods
- Meal planning
- Healthy foods
- General wellness

The assistant retrieves relevant information from the nutrition knowledge base before generating an answer.

## RAG Architecture

This project uses Retrieval-Augmented Generation.

The workflow is:

User Question
        ↓
FAISS Vector Database
        ↓
Similarity Search
        ↓
Relevant Nutrition Documents
        ↓
Context + User Health Profile
        ↓
GPT-OSS-120B
        ↓
AI Response

The nutrition PDF is processed into smaller text chunks and converted into vector embeddings.

These embeddings are stored in a FAISS vector database and retrieved when the user asks a question.

## Technology Stack

### Frontend

- Streamlit

### Programming Language

- Python

### AI / LLM

- GPT-OSS-120B
- Hugging Face Router
- OpenAI-compatible API

### RAG

- LangChain
- FAISS
- Hugging Face Embeddings
- Sentence Transformers

### Embedding Model

`sentence-transformers/all-MiniLM-L6-v2`

### Libraries

- Streamlit
- LangChain
- LangChain Community
- LangChain Hugging Face
- OpenAI
- FAISS
- PyPDF
- Python Dotenv

## Project Structure

```text
ai-health-assistant/
│
├── data/
│   └── nutrition.pdf
│
├── vectorstore/
│   ├── index.faiss
│   └── index.pkl
│
├── api.py
├── app.py
├── create_database.py
├── diet.py
├── rag.py
├── llm_test.py
├── prompt.md
├── requirements.txt
├── .gitignore
└── README.md
