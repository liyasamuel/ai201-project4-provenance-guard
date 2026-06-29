# ai201-project4-provenance-guard

\# Provenance Guard



Provenance Guard is a Flask-based API that estimates whether submitted text is more likely to be AI-generated or human-written. The system combines two independent detection signals—a large language model (Groq Llama 3.3) and a simple stylometric heuristic—to produce a confidence score, a transparency label, and an audit log entry. Users can also appeal a classification, allowing the submission to be marked for human review.



\---



\# Project Overview



The goal of this project is to build a transparent AI-content detection system rather than a simple classifier. Instead of making hidden decisions, the system records every submission, explains its confidence level, allows users to appeal decisions, and maintains an audit log for accountability.



\---



\# System Architecture



The application consists of two main components:



\* \*\*app.py\*\* – Implements the Flask API, manages submissions, confidence scoring, transparency labels, audit logging, rate limiting, and appeals.

\* \*\*detector.py\*\* – Implements the two detection signals:



&#x20; \* Groq Llama 3.3 AI detection signal

&#x20; \* Stylometric heuristic signal



Every submission follows this workflow:



1\. User submits text and creator ID.

2\. Groq produces an AI-likelihood score.

3\. The stylometric detector produces a writing-style score.

4\. Both scores are averaged into one confidence score.

5\. A transparency label is assigned.

6\. The submission is stored in the audit log.

7\. Users may later submit an appeal.



\---



\# Detection Signals



The system intentionally combines two different signals instead of relying on a single detector.



\## Signal 1 — Groq Llama 3.3



The first signal comes from the Groq API using the Llama 3.3 70B model. The model is prompted to estimate whether a passage appears AI-generated and returns a value between 0.0 and 1.0.



This signal captures linguistic patterns that are difficult to detect with simple rules.



\---



\## Signal 2 — Stylometric Heuristics



The second signal analyzes characteristics of the writing itself, including:



\* average sentence length

\* vocabulary diversity

\* punctuation usage



These features provide a lightweight estimate of writing style that complements the language model instead of replacing it.



\---



\# Confidence Scoring



The final confidence score is calculated by averaging the two detection signals:



```

confidence = (llm\_score + style\_score) / 2

```



This simple approach keeps the scoring process transparent and easy to understand.



If this system were deployed in production, I would replace this averaging approach with a trained calibration model using a much larger labeled dataset so that the confidence values better reflect real-world probabilities.



\---



\# Example Confidence Scores



\## Example 1



Text:



> Artificial intelligence represents a transformative paradigm shift in modern society...



Result:



\* LLM Score: \*\*0.80\*\*

\* Style Score: \*\*0.41\*\*

\* Final Confidence: \*\*0.60\*\*



Classification:



\*\*Uncertain\*\*



\---



\## Example 2



Text:



> I walked my dog this morning and then went to get coffee with a friend.



Result:



\* LLM Score: \*\*0.20\*\*

\* Style Score: \*\*0.42\*\*

\* Final Confidence: \*\*0.31\*\*



Classification:



\*\*Uncertain\*\*



These examples demonstrate that the confidence score varies depending on the submitted content instead of remaining constant.



\---



\# Transparency Labels



The system displays one of three transparency messages.



\## High-confidence AI



> Likely AI-generated. Our system has high confidence this content was generated with AI.



\---



\## High-confidence Human



> Likely human-written. Our system has high confidence this content was written by a person.



\---



\## Uncertain



> Uncertain. The system cannot confidently determine whether this content is AI-generated or human-written.



\---



\# API Endpoints



\## POST /submit



Accepts:



\* creator\_id

\* text



Returns:



\* content\_id

\* confidence

\* attribution

\* transparency label

\* detection scores



\---



\## POST /appeal



Allows a creator to submit an appeal with additional reasoning.



The submission status changes to:



```

under\_review

```



\---



\## GET /log



Returns the complete audit log containing:



\* submission ID

\* creator ID

\* timestamp

\* detection scores

\* confidence

\* transparency label

\* appeal status



\---



\# Rate Limiting



The API uses Flask-Limiter to reduce abuse.



Limits:



\* 10 requests per minute

\* 100 requests per day



\---



\# Known Limitations



The current system is intentionally simple and has several limitations.



One likely failure case is highly polished human writing, such as professionally edited essays or academic papers. Because the Groq detector and stylometric heuristics both favor consistent structure and formal language, these texts may receive higher AI-likelihood scores than they deserve.



Similarly, short AI-generated responses written in an informal style could appear more human because the stylometric signal has relatively little information to analyze.



\---



\# Spec Reflection



The project specification helped by clearly separating detection, transparency, appeals, and auditing into independent requirements. This made it easier to implement each feature incrementally.



One implementation difference is the confidence calculation. The specification encouraged thoughtful scoring rather than prescribing a specific algorithm. I chose a simple average of the two detection signals because it is easy to explain and demonstrates the required functionality, although a production system would likely use a learned calibration model.



\---



\# AI Usage



Artificial intelligence was used as a development assistant throughout this project.



\### Instance 1



I used AI to help debug Flask, PowerShell, Groq API, and Python errors encountered during implementation. I reviewed every suggested change, tested it locally, and only kept solutions that worked correctly.



\### Instance 2



I used AI to improve the project documentation by organizing the README, explaining architectural decisions, and refining wording. I verified that the descriptions matched the implementation before including them.



\---



\# Future Improvements



Possible future improvements include:



\* collecting a labeled evaluation dataset

\* replacing heuristic scoring with a trained classifier

\* improving stylometric feature extraction

\* adding persistent database storage

\* implementing authentication for creator accounts

\* supporting asynchronous review workflows



\---



\# Running the Project



1\. Clone the repository.



2\. Install dependencies:



```bash

pip install -r requirements.txt

```



3\. Create a `.env` file containing:



```

GROQ\_API\_KEY=your\_api\_key\_here

```



4\. Start the server:



```bash

python app.py

```



5\. The API runs at:



```

http://127.0.0.1:5000

```



