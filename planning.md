

# Provenance Guard Planning

## Architecture

When a user submits text, the system receives the request through the `/submit` endpoint. The submission is analyzed using two independent detection signals: a Groq LLM-based detector and simple stylometric heuristics. The results are combined into a single confidence score that determines the transparency label returned to the user. Every submission is recorded in an audit log.

If the creator disagrees with the result, they can submit an appeal through the `/appeal` endpoint. The appeal changes the submission status to **Under Review** and records the action in the audit log.

### Architecture Diagram

```text
                User
                  |
                  v
           POST /submit
                  |
        -------------------
        |                 |
        v                 v
   Groq Detector   Stylometric Detector
        |                 |
        -------------------
                  |
                  v
        Combined Confidence Score
                  |
                  v
        Transparency Label
                  |
                  v
             Audit Log
                  |
                  v
             JSON Response

                User
                  |
                  v
           POST /appeal
                  |
                  v
        Update Submission Status
                  |
                  v
             Audit Log
                  |
                  v
             JSON Response
```

---

# Detection Signals

## Signal 1: Groq LLM Detection

The submitted text is sent to the Groq Llama 3.3 model, which estimates whether the writing appears more likely to be human-written or AI-generated. The model returns a confidence score between 0 and 1.

**Strengths**

* Understands context and writing quality
* Can recognize AI writing patterns

**Weaknesses**

* Can confidently misclassify unusual human writing
* Depends on an external API

---

## Signal 2: Stylometric Heuristics

The system calculates simple writing statistics such as:

* Average sentence length
* Vocabulary diversity
* Punctuation density

These values are converted into a second confidence score.

**Strengths**

* Fast
* Does not require an API
* Easy to explain

**Weaknesses**

* Less accurate on short passages
* Creative writing may produce misleading scores

---

# Confidence Score

The final confidence score is calculated by averaging both detection signals.

```
Final Confidence = (Groq Score + Stylometric Score) / 2
```

---

# Transparency Labels

The final score determines the label shown to the user.

| Confidence Score | Label               |
| ---------------- | ------------------- |
| 0.00 – 0.39      | Likely Human        |
| 0.40 – 0.69      | Uncertain           |
| 0.70 – 1.00      | Likely AI Generated |

---

# Audit Log

Each submission stores:

* Submission ID
* Timestamp
* Submitted text
* Groq score
* Stylometric score
* Final confidence
* Transparency label
* Current status
* Appeal status (if submitted)

---

# Appeal Workflow

1. User submits an appeal.
2. The submission status changes to **Under Review**.
3. The appeal is recorded in the audit log.
4. The API returns confirmation that the appeal was received.

---

# API Endpoints

## POST /submit

Accepts submitted text, analyzes it using both detection signals, calculates a confidence score, stores the result, and returns the transparency label.

---

## POST /appeal

Receives a submission ID and appeal message, updates the submission status to **Under Review**, records the appeal, and returns a confirmation response.

---

# Assumptions

* All submissions are plain text.
* The Groq API is available during analysis.
* Scores are normalized between 0 and 1.
* Appeals are recorded but are not automatically reviewed.
* The audit log is stored locally for this project.

---

# Minimal Implementation Plan

1. Build the `/submit` endpoint.
2. Implement the Groq detector.
3. Implement the stylometric detector.
4. Combine both scores into one confidence score.
5. Return a transparency label.
6. Save the submission to the audit log.
7. Build the `/appeal` endpoint.
8. Record appeals in the audit log.
