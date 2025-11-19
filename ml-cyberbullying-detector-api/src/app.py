from fastapi import FastAPI
import gradio as gr
from toxicity_model import check_toxicity, is_custom_toxic, check_sentiment, paraphrase_text, paraphrase_text_local, check_cyberbullying_with_hatebert, is_person_or_pronoun
import mysql.connector
import threading
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# FastAPI setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MySQL connection settings
db_config = {
    'host': 'cyberbullying.cbo2y20cex64.ap-southeast-2.rds.amazonaws.com',
    'user': 'root',
    'password': 'Beauisagoodboy',
    'database': 'cyberbullying'
}

# Database logging
def log_to_rds(text, is_bullying, tox_score, sentiment_score, suggested,  person_or_pronoun, cyberbullying_flag, zone_db, likelihood, comment):
    """
    Logs analyzed message data into MySQL database.
    """
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        tox_score = float(tox_score)
        sentiment_score = float(sentiment_score)

        insert_query = """
        INSERT INTO MESSAGE (text, is_bullying, toxicity_score, sentiment_score, suggested_text, person_or_pronoun, cyberbullying_flag, zone, likelihood, comment)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            text,
            int(is_bullying),
            tox_score,
            sentiment_score,
            suggested or "",
            int(person_or_pronoun),
            int(cyberbullying_flag),
            zone_db,
            likelihood,
            comment

                
        ))

        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")


# Analysis function
def analyze(text):
    """
    Performs cyberbullying analysis on text using multiple models and rules.
    """
    tox_score = round(check_toxicity(text),2)
    sent_score = round(check_sentiment(text), 2)
    custom_flag = is_custom_toxic(text)
    person_or_pronoun = is_person_or_pronoun(text)
    cyberbullying_flag = check_cyberbullying_with_hatebert(text)

    # Determine if message is bullying based on thresholds
    #is_bullying = person_or_pronoun and (
    is_bullying =  custom_flag or tox_score >= 0.4 or cyberbullying_flag >=0.5
    suggested_text = paraphrase_text(text) if is_bullying else None

    # Assign zone, likelihood, and comment based on severity
    if custom_flag or tox_score >= 0.7 or cyberbullying_flag >=0.7:
        zone = '🔴 Red Zone'
        zone_db = 'Red Zone'
        likelihood = 'Very high likelihood of bullying'
        comment = 'Warning: this message looks very harmful. It may seriously hurt someone. This may cross the line into cyberbullying.'
    elif tox_score >= 0.4 or cyberbullying_flag >=0.4:
        zone = '🟠 Orange Zone '
        zone_db = 'Orange Zone'
        likelihood = 'High likelihood of bullying'
        comment = 'This could hurt someone’s feelings — try to say it in a more positive way.'
    elif tox_score >= 0.2 or cyberbullying_flag >=0.2:
        zone = '🟡 Yellow Zone  '
        zone_db = 'Yellow Zone'
        likelihood = 'Medium likelihood of bullying'
        comment = 'Looks safe, but context matters — make sure it won’t hurt anyone.' 
    else:
        zone = '🟢 Green Zone  '
        zone_db = 'Green Zone'
        likelihood = 'Low likelihood of bullying'
        comment = 'Looks good! No red flags here. Nice one!'   

    # Log analysis to database
    log_to_rds(text, is_bullying, tox_score, sent_score, suggested_text, zone_db, likelihood, comment)
    return text, str(is_bullying), tox_score, sent_score, suggested_text, person_or_pronoun, cyberbullying_flag, zone, zone_db, likelihood, comment

# Gradio interface
def start_gradio():
    iface = gr.Interface(
    fn=analyze,
    inputs=gr.Textbox(label="Enter text", lines=3),
    outputs=[
        gr.Textbox(label="Original Text"),
        gr.Textbox(label="Is Bullying?"),
        gr.Number(label="Toxicity Score"),
        gr.Number(label="Sentiment Score"),
        gr.Textbox(label="Suggested Text")
    ],
    title="Cyberbullying Detection Tool"
)
    iface.launch(share=True)  


# FastAPI API endpoint
class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_api(request: TextRequest):
    """
    API endpoint to analyze text via POST request.
    Returns zone, likelihood, comment, and suggested text.
    """
    text = request.text  # Access the 'text' from the request body

    # Perform analysis
    tox_score = round(check_toxicity(text),2)
    sent_score = round(check_sentiment(text), 2)
    custom_flag = is_custom_toxic(text)
    person_or_pronoun = is_person_or_pronoun(text)
    cyberbullying_flag = check_cyberbullying_with_hatebert(text)
    is_bullying =  custom_flag or tox_score >= 0.4 or cyberbullying_flag >=0.5

    # Determine severity zone
    if custom_flag or tox_score >= 0.7 or cyberbullying_flag >=0.7:
        zone = '🔴 Red Zone'
        zone_db = 'Red Zone'
        likelihood = 'Very high likelihood of bullying'
        comment = 'Warning: this message looks very harmful. It may seriously hurt someone. This may cross the line into cyberbullying.'
    elif tox_score >= 0.4 or cyberbullying_flag >=0.4:
        zone = '🟠 Orange Zone '
        zone_db = 'Orange Zone'
        likelihood = 'High likelihood of bullying'
        comment = 'This could hurt someone’s feelings — try to say it in a more positive way.'
    elif tox_score >= 0.2 or cyberbullying_flag >=0.2:
        zone = '🟡 Yellow Zone  '
        zone_db = 'Yellow Zone'
        likelihood = 'Medium likelihood of bullying'
        comment = 'Looks safe, but context matters — make sure it won’t hurt anyone.' 
    else:
        zone = '🟢 Green Zone  '
        zone_db = 'Green Zone'
        likelihood = 'Low likelihood of bullying'
        comment = 'Looks good! No red flags here. Nice one!'

    
    suggested_text = paraphrase_text(text) if is_bullying else None
    suggested_text = str(suggested_text)

    # Log analysis to RDS
    log_to_rds(text, is_bullying, tox_score, sent_score, suggested_text, person_or_pronoun, cyberbullying_flag, zone_db, likelihood, comment)

    # Convert tox_score and sent_score to float
    return {
        #"text": text,
        #"is_bullying": str(is_bullying),
        #"toxicity_score": f"{tox_score:.2f}",
        #"sentiment_score": f"{sent_score:.2f}",
        #"suggested_text": suggested_text or "",
        #"person_or_pronoun": str(person_or_pronoun),
        #"cyberbullying_flag": str(cyberbullying_flag)
        "zone": zone,
        "likelihood": likelihood,
        "comment": comment,
        "suggested_text": suggested_text or ""
    }

# Run FastAPI (and optionally Gradio)
def run():
    #import uvicorn
    # Run FastAPI in background thread
    #threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000)).start()

    # Start Gradio interface
    #start_gradio()
    #threading.Thread(target=start_gradio).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    run()
