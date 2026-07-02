# SHL Assessment Recommendation Agent

An AI-powered recommendation agent that helps recruiters identify the most suitable SHL assessments based on hiring requirements. The application provides intelligent assessment recommendations, comparison of SHL assessments, clarification for ambiguous requests, and off-topic query handling through a conversational API.

---

## Features

- Recommend relevant SHL assessments based on job role, skills, and experience.
- Compare two SHL assessments using catalog information.
- Ask follow-up questions when user requirements are incomplete.
- Reject queries unrelated to SHL assessments.
- REST API built with FastAPI.
- AI-generated responses using Google's Gemini API.
- Lightweight keyword-based retrieval over the SHL assessment catalog.

---

## Tech Stack

- Python 3.11
- FastAPI
- Google Gemini API
- Pydantic
- JSON Catalog
- Uvicorn

---

## Project Structure

```
SHL Assessment Agent/
│
├── app/
│   ├── agent.py
│   ├── api.py
│   ├── llm.py
│   ├── models.py
│   ├── retriever.py
│   └── utils.py
│
├── data/
│   └── shl_catalog.json
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Architecture

```
                User Query
                     │
                     ▼
              FastAPI Endpoint
                     │
                     ▼
               SHL Agent
                     │
      ┌──────────────┴──────────────┐
      │                             │
Intent Detection             Clarification
      │
      ▼
Retriever
      │
      ▼
Relevant SHL Assessments
      │
      ▼
Gemini LLM
      │
      ▼
JSON Response
```

---

## Retrieval Strategy

The recommendation engine uses a weighted keyword retrieval approach.

Each assessment is indexed using:

- Assessment Name
- Description
- Assessment Category
- Job Levels
- Languages

The retriever assigns weighted scores based on keyword matches.

Higher priority is given to:

- Assessment names
- Technical skills (Java, Python, SQL)
- Multiple keyword matches

Only highly relevant assessments are returned to the language model.

---

## API Endpoints

### Health Check

```
GET /health
```

Response

```json
{
  "status": "ok"
}
```

---

### Chat Endpoint

```
POST /chat
```

Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer with 4 years of experience"
    }
  ]
}
```

Example Response

```json
{
  "reply": "...",
  "recommendations": [
    {
      "name": "Core Java (Advanced Level) (New)",
      "url": "...",
      "test_type": "Knowledge & Skills"
    }
  ],
  "end_of_conversation": true
}
```

---

## Supported Conversation Types

### Assessment Recommendation

```
Hiring a Java developer with 4 years of experience
```

---

### Clarification

```
Need assessment
```

The agent asks follow-up questions to gather sufficient hiring requirements.

---

### Assessment Comparison

```
Compare OPQ32r and Verify
```

The agent compares two assessments using catalog information.

---

### Off-topic Queries

```
Who won the IPL?
```

The agent politely informs the user that it only answers SHL assessment-related queries.

---

## Running Locally

Clone the repository

```bash
git clone https://github.com/Zamishi/shl-assessment-agent.git
```

Move into the project

```bash
cd shl-assessment-agent
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

Start the server

```bash
uvicorn app.api:app --reload
```

Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Deployment

The application is deployed on Render.
<img width="2784" height="716" alt="image" src="https://github.com/user-attachments/assets/201bbad1-bf8b-40b6-afa5-b74b8c19afaf" />


**Live API**

https://shl-assessment-agent-gifk.onrender.com

Swagger Documentation

https://shl-assessment-agent-gifk.onrender.com/docs

Health Endpoint

https://shl-assessment-agent-gifk.onrender.com/health

---

## Design Decisions

- FastAPI was chosen for building lightweight REST APIs.
- Gemini is used for natural language understanding and response generation.
- A custom weighted retrieval algorithm was implemented instead of vector search due to the relatively small catalog size (377 assessments), providing low latency and explainable ranking.
- The application is stateless, making it easy to deploy and scale.

---

## Future Improvements

- Hybrid semantic search using embeddings.
- Better ranking with learning-to-rank techniques.
- Conversation memory for longer interactions.
- More robust comparison parsing.
- Automatic evaluation metrics.

---

## Author

**Amishi Sharma**

GitHub: https://github.com/Zamishi
