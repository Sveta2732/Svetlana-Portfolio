# Anti-Cyberbullying Web Application

**Data Science · AI · AWS · Full-Stack Collaboration · R · React · FastAPI · Python · MySQL**

This repository contains my individual Data Science and Backend Engineering contributions to a 6-student team project — an interactive anti-cyberbullying web application designed for teenagers.  
The platform combines educational content, AI-assisted text analysis, interactive visualisations and a gamified learning experience to help young people recognise, report and respond to online abuse.

Our team successfully presented the final product to industry professionals and **won the Monash PG Industry Experience Expo**.

---

## 🔍 Project Overview

Teenagers often struggle to recognise cyberbullying, understand how to respond, and know where to seek help.  
Our web application tackles this challenge through a **space-themed, story-driven learning experience** guided by **Gleepo**, a friendly alien who leads users through a safe and engaging anti-cyberbullying journey.

To help teens build real recognition and help-seeking skills, the platform combines:

- **Interactive data visualisations** — transforming abstract cyberbullying statistics into relatable, classroom-level insights.
- **Gamified learning** — teaching teens to differentiate between normal online behaviour and harmful interactions.
- **Real teen stories (video content)** — fostering emotional connection, validation, and awareness that they’re not alone.
- **AI-powered text checking** — identifying toxic or harmful language.
- **Resource pathways** — clear, easy-to-navigate links to professional support, reporting tools, and trusted adult advice.

This blend of **AI**, **data visualisation**, **game-based learning**, and **narrative design** makes the platform educational, relatable, and accessible for teenagers.

---

## ⭐ My Contributions

As the team’s **Data Scientist & Backend Engineer**, I was responsible for all data workflows, analytical components, backend logic for interactive features, and multiple AI-powered modules.

My key contributions include:

- **Topic Research & Dataset Analysis**  
  *(researching cyberbullying patterns, identifying risks for teens, cleaning and merging datasets, preparing formatted CSVs — R)*

- **Interactive Visualisations**  
  *(cyberbullying statistics & social media trends — fully designed and implemented React prototypes)*

- **“Clean My Feed” — Game API Development**  
  *(AWS Lambda + AWS MySQL backend logic for gameplay, scoring, analytics feedback)*

- **AI Toxicity Detection API**  
  *(FastAPI service integrating Hugging Face models + Gemini; logs predictions and paraphrased text to AWS MySQL)*

- **Database Schema & Data Flow Design**  
  *(designed and implemented the full relational database supporting players, comments, results, toxicity logs, and game analytics)*

Below is a detailed breakdown of each area.

---

### Topic Research & Dataset Analysis

Conducted research and analyzed multiple datasets on teen cyberbullying.  

- Cleaned, merged, and formatted data in R for consistent use.  
- Produced statistics to guide visualisation and gameplay design.  
- Prepared CSVs for backend and interactive features.  

---

### Interactive Visualisations

I designed and implemented two interactive visualisations to make cyberbullying statistics engaging for teenagers:

- **Visualisation 1 – "How My Class Looks Like":**  
  A personalised snapshot of cyberbullying prevalence, showing teens they are not alone and encouraging them to seek help. 
  *(Displayed on the website under **“Cyber Stats”**)*
  ![How My Class Looks Like](https://github.com/Sveta2732/Svetlana-Portfolio/raw/f5985b9978ec192729a76d4bec635a39363e6f70/cyberbullying-team-project-web/demo/visualisation1.gif)


- **Visualisation 2 – "Social Media & Cyberbullying":**  
  Highlights cyberbullying patterns on popular platforms with an age-appropriate, stylised format and links to reporting tools.
  *(Displayed on the website under **“Net Quiz”**)*
  ![Social Media & Cyberbullying](https://github.com/Sveta2732/Svetlana-Portfolio/raw/f5985b9978ec192729a76d4bec635a39363e6f70/cyberbullying-team-project-web/demo/visualisation2.gif)


**Implementation:**  
- Built full prototypes in **React** with all logic and interactivity.  
- Teammate helped integrate into the main website and split into reusable components.

---

### “Clean My Feed” — Game API Development

Backend logic for **“Clean My Feed”**, a gamified learning experience helping teenagers identify cyberbullying in realistic comments. Focused on **data-driven gameplay, personalised feedback, and analytical insights**.

**Key Components:**

- **Comment Delivery API (AWS Lambda + MySQL)**  
  - Retrieves and shuffles comments from the database.  
  - Balanced exposure: 4 positive + 6 non-positive comments per block.  
  - Returns comments in JSON format with CORS headers.

- **Feedback API (AWS Lambda + MySQL)**  
  - Processes player submissions and validates responses against labelled comments.  
  - Calculates scores, highlights mistakes, and identifies growth areas.  
  - Logs submissions and responses for analytics.  
  - Returns detailed summaries:  
    - Correct vs incorrect responses  
    - Weak areas by bullying type  
    - Comparative performance with other users  
    - Total score and percentile ranking  

**Demo:**  
![Clean My Feed Demo](https://github.com/Sveta2732/Svetlana-Portfolio/raw/f5985b9978ec192729a76d4bec635a39363e6f70/cyberbullying-team-project-web/demo/cleen_my_feed.gif)

[View full API source files →](https://github.com/Sveta2732/Svetlana-Portfolio/tree/main/cyberbullying-team-project-web/src/api)


**Technical Stack:** Python, MySQL, AWS Lambda, JSON, CORS, serverless backend

---

### Toxicity Detection API

Analyzes user-submitted messages to detect harmful or bullying content and offers **rephrased, safer alternatives**.  

- **FastAPI + Hugging Face + Gemini + MySQL (AWS)**  
  - Evaluates the **likelihood of cyberbullying** in text.  
  - Provides paraphrased suggestions for safer communication.  
  - Logs results in MySQL for tracking.  
  - Integrates with the web frontend for real-time feedback.

This API has its **own repository**: [ml-cyberbullying-detector-api](https://github.com/Sveta2732/Svetlana-Portfolio/tree/main/ml-cyberbullying-detector-api)  

**Technical Stack:** FastAPI, Python, Hugging Face, Gemini, MySQL (AWS)

---

### Database Schema & Data Flow

A centralized **MySQL database** underpins all game and analysis APIs:  

- Stores comments, user submissions, and individual responses.  
- Supports balanced comment delivery and scoring logic.  
- Logs player actions and performance for analytics and growth tracking.  

**Technical Stack:** MySQL (AWS)

---

## 🛠️ Tech Stack

- **Programming & Analysis:** R (data processing, cleaning, merging), Python (AWS Lambda, FastAPI)  
- **Frontend & Visualisation:** React (interactive visualisations, prototypes)  
- **Backend & Database:** MySQL (AWS) — centralized schema for all APIs  
- **Cloud & Serverless:** AWS Lambda, AWS RDS  
- **AI & NLP:** Hugging Face models, Gemini (text toxicity detection & paraphrasing)  
- **Data & File Handling:** CSV, JSON, structured data pipelines  
- **Deployment & Integration:** CORS-enabled APIs, RESTful services

---

## 📂 Project Structure
```text
cyberbullying-team-project-web/
│
├─ data/                          # Datasets used for analysis and visualisations
├─ notebooks/                     # Data analysis and prototyping notebooks
├─ public/                        # Static assets (images, gifs, audio) for visualisations
│   └─ quizPage/                  # Assets used specifically in visualisation / quiz pages
├─ demo/                          # Screenshots, GIFs, and video demonstrations
└─ src/                           # Application source code
    ├─ api/                       # Backend API (AWS Lambda functions)
    ├─ components/                 # React components for visualisations
    ├─ hooks/                      # Custom React hooks for visualisations
    └─ pages/                      # React page components (visualisation pages)

```
## 🏆 Key Learnings & Skills Developed

### Technical Skills
- **Data Science & Analysis:** Cleaning, merging, transforming datasets (R, Python, CSV/Excel)  
- **Interactive Visualisations:** Designing age-appropriate, engaging visualisations (React, CSS)  
- **Backend & APIs:** Serverless AWS Lambda APIs for gameplay, scoring, feedback (Python, MySQL, AWS)  
- **AI Integration:** NLP-based toxicity detection with FastAPI and Hugging Face  
- **Database Design:** Schemas and data flows for multiple APIs (MySQL, AWS)  

### Collaboration & Project Management
- **Teamwork & Communication:** Coordinating contributions and explaining technical results  
- **Problem Solving & Planning:** Managing deadlines, scalable solution design, multi-stream integration  

This experience combined **data science, backend engineering, and UX-focused design**, preparing me for interdisciplinary projects.

---

## 🌐 Live Demo

A live version of the website is available at [worldwecreated.org](https://worldwecreated.org/)

> **Note:** Rights were transferred to Monash University; some features may not be fully functional.  
> Recommended to view attached **videos and GIFs** in the repository for a complete demonstration of functionality.

