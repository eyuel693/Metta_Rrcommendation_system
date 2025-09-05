# Mini-Recommendation System with MeTTa Knowledge Representation

## Overview

This project demonstrates how to build a **knowledge-based movie recommendation system** by combining the reasoning capabilities of the **MeTTa programming language** with the flexibility of **Python**. Unlike traditional black-box recommenders, this system provides **explainable suggestions**, allowing users to understand *why* a particular movie is recommended.

The project integrates **content-based filtering**, **collaborative filtering**, and **hybrid recommendation** into a unified framework. It leverages MeTTa for knowledge representation and reasoning, Python for integration and interaction, and a simple API/frontend for user experience.

---

## How It Works

### 1. Knowledge Representation (MeTTa)

All facts about movies, genres, directors, and user preferences are represented as **atoms** in MeTTa. Example:

```metta
(likes alice inception)
(genre inception sci-fi)
(director inception christopher-nolan)
```

These structured atoms allow the system to reason about similarities between movies and relationships between users.

### 2. Reasoning Rules (MeTTa)

Recommendation rules are defined in MeTTa:

* **Content-Based (Genre/Director)**: Suggests movies that share the same genre or director as the user’s liked movies.
* **Collaborative Filtering**: Suggests movies liked by similar users.
* **Hybrid Recommendations**: Combines multiple strategies into a single unified function.

Example rule:

```metta
(= (recommend-to $user $movie)
   (or (content-similarity $user $movie)
       (director-match $user $movie)
       (collaborative-rec $user $movie)))
```

### 3. Python Integration

Python is used to:

* Initialize and load the MeTTa knowledge base.
* Execute queries and retrieve recommendations.
* Generate explanations for why a movie is recommended.
* Expose recommendations and explanations through APIs.

Example integration snippet:

```python
hybrid_recs = execute_query(metta, f'!(recommend-to {user} $movie)')
```

### 4. REST API (Flask)

A Flask backend provides REST endpoints:

* `GET /recommendations/<user>` → Returns recommended movies for a user.
* `POST /update-preferences` → Updates user preferences dynamically.
* `GET /explanations/<user>` → Returns human-readable explanations.

### 5. Frontend (HTML/css/JS)

A simple web interface allows users to:

* Enter their preferences (favorite genres, directors, or actors).
* View personalized movie recommendations.
* See **explanations** of why each movie was recommended.
* Provide feedback (likes/dislikes) to dynamically update the knowledge base.

---

## Components

1. **MeTTa Knowledge Base (`recommendation.metta`)**

   * Stores all facts about users, movies, genres, and directors.
   * Defines reasoning rules for recommendations.

2. **Python Integration (`recommender.py`)**

   * Handles queries to the MeTTa engine.
   * Processes and deduplicates recommendations.
   * Retrieves explanations and user similarity.

3. **Flask API (`app.py`)**

   * Exposes recommendation logic as REST endpoints.
   * Connects the knowledge engine with the frontend.

4. **Frontend (`index.html styles.css`)**

   * Simple UI for user interaction.
   * Displays recommendations and explanations.

5. **Utility Functions (`utils.py`)**

   * Helper functions to initialize MeTTa, execute queries, and process results.

---

## Example Workflow

1. User logs in as **Alice**.
2. The system checks Alice’s liked movies and identifies genres and directors.
3. MeTTa rules infer new movies Alice might like.
4. The Python layer queries the hybrid recommendation function.
5. The system returns a list of recommended movies *with explanations*.
6. Alice provides feedback → MeTTa knowledge base is updated dynamically.

---

## Learning Outcomes

* Understand how **knowledge graphs** can power explainable recommendations.
* Learn how to define and query structured knowledge in **MeTTa**.
* Gain experience integrating symbolic reasoning with **Python**.
* Explore **content-based, collaborative, and hybrid** filtering in practice.
* Build APIs and frontends that expose explainable AI functionality.

---

