# Cyberbullying Detection API 🛡️

**Project type:** Machine Learning | NLP | Web App  
**Stack:** Python, Hugging Face, Gradio, Google Gemini API, AWS RDS (MySQL), JSON, NLP Models

---

## 🎯 Description
This API is part of an anti-cyberbullying web platform designed for teenagers. It analyzes text for toxic or harmful content using multiple ML models hosted on Hugging Face. If any model flags toxicity, the message is considered potentially harmful. The tool can suggest safer rephrasing using the Gemini API, and if unavailable, falls back to a local text rephrasing model. All text and results are logged securely in an AWS database for analysis.

---

## ⚙️ Stack / Technologies

- **Python** – main backend language  
- **Hugging Face Models** – for toxicity and cyberbullying detection  
- **Google Gemini API** – for text rephrasing (fallback to local NLP model if API fails)  
- **Gradio** – user-friendly interface for demo/testing  
- **AWS RDS (MySQL)** – storing messages, results, and suggestions  
- **JSON** – custom toxic words list  

---

## ⚡ Features

- Detects toxic or bullying text messages using multiple ML models  
- Assigns severity zones based on combined model outputs:  
  - 🟢 Green – Low likelihood  
  - 🟡 Yellow – Medium likelihood  
  - 🟠 Orange – High likelihood  
  - 🔴 Red – Very high likelihood  
- Uses an extensible teen-slang toxicity dictionary that can be updated as new slang and harmful expressions emerge  
- Suggests safer, non-bullying rephrasing using the Google Gemini API, with a local fallback paraphraser if the API is unavailable  
- Logs all analyzed messages, model outputs, and suggested rephrases to an AWS database  
- Provides a clean Gradio web interface for testing and live demonstrations  
- Fully integrated into the anti-cyberbullying website, where the frontend calls the API endpoint to analyze user-submitted messages in real time  

---

## ⚡ How It Works

1. The user submits a message through the website, which sends the text to the project’s REST API endpoint.
2. The API evaluates the text using several ML models hosted on Hugging Face, each scoring the message for toxicity and cyberbullying.
3. If any model flags the text as harmful, the system marks the message as toxic.
4. If the message is harmful:
   - The API attempts to generate a safer, non-bullying rephrase using the Google Gemini API
   - If Gemini is unavailable, the system falls back to a local positive-rephrasing model
5. The API returns a structured result containing:
   - severity zone
   - likelihood score
   - automatic comment
   - suggested alternative wording
6. All processed text, model outputs, and suggestions are stored in an AWS MySQL database for analytics and monitoring.
7. A Gradio interface is also provided for testing and demonstration, but it is not part of the production pipeline.

---

## 🧠 What I Learned – Short Reflection

This project helped me strengthen my skills in building end-to-end machine learning systems.  
I gained experience in:  

- Creating a production-ready REST API that integrates multiple ML toxicity-detection models  
- API integration, including using Google Gemini for advanced rephrasing with a custom fallback model  
- Database logging and monitoring, securely storing analysis results on AWS  
- Designing a full-stack ML workflow that connects backend processing, NLP models, and a live web interface  

Overall, this project demonstrates my ability to build a real-world ML application that combines natural language processing, API orchestration, cloud storage, and practical safety features.

---

## 📂 Project Structure
```text
ml-cyberbullying-detector-api/
│
├─ src/                          # Main application code
│   ├─ app.py                    # REST API endpoint (used by website)
│   ├─ toxicity_model.py         # ML/NLP toxicity detection functions
│
├─ data/                         # Supporting datasets
│   └─ toxic_words.json          # Custom extensible teen-slang toxicity dictionary
│
├─ demo/                         # Demonstration materials
│   ├─ demo.gif                  
│   ├─ video_demo.mp4            
│   ├─ video_demo2.mp4
│   ├─ website_demo.png
│   └─ interface_demo.png
│
├─ requirements.txt              # Python dependencies
└─ README.md                     # Project documentation
```
---

## 🔗 Live Demo

### Website Screenshots
![Website Demo](https://raw.githubusercontent.com/Sveta2732/Svetlana-Portfolio/75b920712a0cd7551c4f28b4695a33fbde8f9ddd/ml-cyberbullying-detector-api/demo/website_demo.png)
![Interface Demo](https://raw.githubusercontent.com/Sveta2732/Svetlana-Portfolio/75b920712a0cd7551c4f28b4695a33fbde8f9ddd/ml-cyberbullying-detector-api/demo/interface_demo.png)

### GIF Demo of API in action
![Demo GIF](https://raw.githubusercontent.com/Sveta2732/Svetlana-Portfolio/75b920712a0cd7551c4f28b4695a33fbde8f9ddd/ml-cyberbullying-detector-api/demo/demo.gif)

### Full Video Demo
[video demo](https://github.com/Sveta2732/Svetlana-Portfolio/raw/75b920712a0cd7551c4f28b4695a33fbde8f9ddd/ml-cyberbullying-detector-api/demo/demo_video.mp4)

### Second Video Demo
[video demo 2](https://raw.githubusercontent.com/Sveta2732/Svetlana-Portfolio/75b920712a0cd7551c4f28b4695a33fbde8f9ddd/ml-cyberbullying-detector-api/demo/demo_video2.mp4)

### Cyberbullying Detection API live on Hugging Face Spaces:  
[Anti-Bullying ML Demo](https://huggingface.co/spaces/sste0051/AntiBullyinghf)

---

## 🔒 Model Licenses

This project uses the following pre-trained models and their licenses:

- **s-nlp/roberta_toxicity_classifier** — License: OpenRAIL++  
  [Model page](https://huggingface.co/s-nlp/roberta_toxicity_classifier)  

- **ggallipoli/bart-base_neg2pos** — License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)  
  [Model page](https://huggingface.co/ggallipoli/bart-base_neg2pos)  

- **Detoxify (original)** — License: Apache 2.0  
  [GitHub repo](https://github.com/unitaryai/detoxify)  

- **spaCy English model (en_core_web_sm)** — License: see [spaCy model card](https://spacy.io/models/en)  
