# Anti-Cyberbullying Web Application

**Data Science · AI · AWS · Full-Stack Collaboration · R · React · FastAPI · Python · MySQL**

This repository contains my individual Data Science and Backend Engineering contributions to a 6-student team project — an interactive anti-cyberbullying web application designed for teenagers.  
The platform combines educational content, AI-assisted text analysis, interactive visualisations and a gamified learning experience to help young people recognise, report and respond to online abuse.

Our team successfully presented the final product to industry professionals and **won the Monash PG Industry Experience Expo**.

---
## TL;DR – Quick Overview

**Type:** Group Project · Data Science · AI · Full-Stack Web App  
**Role:** Data Scientist & Backend Engineer  

**Goal:**  
Teen-focused platform to help recognise, report, and respond to cyberbullying. Combines AI, gamified learning, and interactive visualisations.

**My Key Contributions:**  
- **Data Analysis & Research:** Cleaned and merged teen cyberbullying datasets.  
- **Interactive Visualisations:** React dashboards showing cyberbullying stats.  
- **Game API ("Clean My Feed"):** AWS Lambda + MySQL backend for gamified learning.  
- **Toxicity Detection API:** FastAPI + pre-trained Hugging Face models + Gemini API with AWS MySQL logging.  
- **Database Design:** Centralized schema supporting APIs, scoring, and analytics.

### 🧠 Data Science / Data Analysis / Data Management Skills

**Data Science & Analysis**
- Data wrangling & preprocessing (R, Python)
- Cleaning and merging large heterogeneous datasets
- Preparing structured datasets for analysis and visualisation
- Requirements-driven analytical workflows (dataset auditing, consistency checks)

**Data Visualisation & Storytelling**
- Designing age-appropriate, user-centric visualisations
- Communicating statistics to non-technical audiences (teenagers, educators)
- Building interactive dashboards (React)

**Database & Data Engineering**
- ETL pipeline development (R → MySQL → AWS)
- MySQL schema design for multiple platform features & normalisation
- AWS RDS deployment and maintenance
- Backend data-access layers (Lambda, FastAPI)
- Data validation & integrity checks
- Ensured consistent data formatting across services (preprocessing + schema alignment)

**Applied Machine Learning**
- Integrated multiple pre-trained NLP models (Detoxify, RoBERTa-based classifier, Sentiment model)
- Built hybrid ML + LLM decision pipeline (HuggingFace models + Gemini API)
- Developed rule-based logic combining model outputs for cyberbullying detection
- Implemented paraphrasing pipeline using Gemini with local model fallback
- Logged model outputs to AWS RDS for analytics and system monitoring

**Data Management**
- Designed a centralised MySQL database supporting multiple platform services
- Created structured tables for analytics, gameplay, and toxicity logs
- Implemented consistent data flow between APIs and the database
- Maintained clean, well-organised data structures for downstream analysis

**Tech Stack:**  
R, Python, React, FastAPI, AWS Lambda, MySQL, Hugging Face NLP models (pre-trained), Gemini API

**Live Demo:**  
[Website](https://worldwecreated.org/) (project now owned by Monash; some features may be inactive)
> Note: Full platform rights were transferred to Monash University after project completion.
The student team no longer maintains the live site, so certain features may not function as originally designed.
For an accurate view of the system, please refer to the attached GIFs and demo videos in the repository. 

**Outcome:**  
- Presented to industry professionals; **won Monash PG Industry Experience Expo**  
- Integrated AI, data-driven insights, and gamified UX for teenagers
> For full details, see below.
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
- Used **real Australian cyberbullying data** from official sources:
  - **ABS (Australian Bureau of Statistics)** – nationally representative datasets with calibrated weights and population benchmarks (ERP)
  - **data.gov.au** – publicly available, peer-reviewed datasets
  - **Google Trends** – public search trend data for correlation analysis

- Cleaned large heterogeneous datasets on teen cyberbullying (CSV, Excel) in R.
- Merged multiple sources into analysis-ready structured datasets.
- Generated descriptive statistics to guide UX design and game balancing.
- Validated dataset quality before database ingestion.
- Prepared CSVs for backend and interactive features.  


---

### Data Visualisation & Data Storytelling

I designed two interactive visualisations focused on **age-appropriate** communication, transforming complex cyberbullying statistics into accessible insights for teenagers.

Because teenagers do not engage with traditional statistical charts, I applied data storytelling principles:
- Simplified statistical indicators without losing meaning
- Used character-guided narrative (Gleepo) to communicate complex trends
- Integrated animation and interactivity to increase engagement  

**Visualisation 1 – "How My Class Looks Like":**  
  A personalised snapshot of cyberbullying prevalence, showing teens they are not alone and encouraging them to seek help. 
  *(Displayed on the website under **“Cyber Stats”**)*
  ![How My Class Looks Like](https://github.com/Sveta2732/Svetlana-Portfolio/raw/f5985b9978ec192729a76d4bec635a39363e6f70/cyberbullying-team-project-web/demo/visualisation1.gif)


**Visualisation 2 – "Social Media & Cyberbullying":**  
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

  **Endpoint:**  
   `POST /postResult2 https://25g8thdik5.execute-api.ap-southeast-2.amazonaws.com/default/postResult2)`

     **Request Body (JSON):**
  ```json
  {
    "submission": [
      { "comment_id": 2, "response_status": "like", "response_time": 3000 },
      { "comment_id": 4, "response_status": "dislike", "response_time": 3000 },
      { "comment_id": 3, "response_status": "dislike", "response_time": 2000 }
    ]
  }
  ```
   **Example Response (JSON):**
  ```json
    {
    "mistakes": [
      ["Maybe stick to doing something else, because this just doesn't work.", "bullying"],
      ["I enjoyed watching, though some parts felt a bit slow.", "positive"]
    ],
    "problem": "general negative",
    "summary": "Growth Area: Detecting offensive behavior. You sometimes missed comments that were actually bullying. Remember that even general insults and offensive language can be forms of cyberbullying.",
    "score": 0,
    "answered": 3,
    "answered_cor": 1,
    "percent": "33.3%",
    "submission_id": 372,
    "comparison": "20.7"
  }
  ```
  **Postman Demo:**  
  <img src="https://raw.githubusercontent.com/Sveta2732/Svetlana-Portfolio/8acbd2c8a705004d09430dcbfdb9168a0340185c/cyberbullying-team-project-web/demo/postmen2.png" 
      alt="Postman Screenshot2" width="400"/>


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

![API Demo](https://github.com/Sveta2732/Svetlana-Portfolio/raw/1662e103f3c33e4747b79994b034dd71f0d4eaa8/ml-cyberbullying-detector-api/demo/demo.gif)


---

### Database Schema & Data Flow

A central **MySQL database** supports all platform features — gameplay, analytics, and toxicity detection.


#### **ETL Pipeline (R → MySQL → AWS)**


- Prepared processed datasets for import into MySQL.  
- Executed the ETL workflow:  
  **Extract** (CSV) → **Transform** (R scripts) → **Load** (MySQL on AWS RDS).



#### **Database Design & Data Management (MySQL, AWS RDS)**

- Designed relational tables for:
  - **Comments dataset** (source text used in the game)  
  - **Gameplay responses & scoring results**  
  - **Toxicity detection logs** from the FastAPI ML pipeline  
  - **User submissions & paraphrasing outputs**

- Created structured, well-organised tables supporting analytics and API workflows.  
- Deployed and configured a **MySQL RDS** instance.  
- Connected backend services (FastAPI, Lambda) to the shared database.  
- Ensured consistent data formatting and schema alignment across services.


#### **Backend Data Access (AWS Lambda)**

- Developed Python Lambda functions as lightweight data-access microservices.  
- Added CORS handling for frontend requests.  
- Supported storage and retrieval of:
  - Player responses  
  - Comment rotation and assignments  
  - Scoring and performance logs  



#### **Tech Stack**

**MySQL · AWS RDS · AWS Lambda · FastAPI · Python · R**


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

