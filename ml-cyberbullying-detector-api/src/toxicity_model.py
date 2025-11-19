from detoxify import Detoxify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline , AutoModelForSequenceClassification, RobertaTokenizer, RobertaForSequenceClassification
import re
import json
import google.generativeai as genai
import os
import spacy
import torch
import torch.nn.functional as F

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GENIE_API_KEY"))

# Load custom toxic phrases and modifiers from JSON

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOXIC_WORDS_PATH = os.path.join(BASE_DIR, "data", "toxic_words.json")
with open(TOXIC_WORDS_PATH, "r") as f:
    custom_data = json.load(f)
custom_words = custom_data["custom_toxic_phrases"]
modifiers = custom_data["modifiers"]

# Load pre-trained models
# Detoxify model for general toxicity scoring
tox_model = Detoxify("original")

# HuggingFace sentiment model
sentiment_model = pipeline("sentiment-analysis")

# Local paraphrasing model (negative -> positive)
model_name = "ggallipoli/bart-base_neg2pos"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# HateBERT-like toxicity classifier
tokenizer2 = RobertaTokenizer.from_pretrained('s-nlp/roberta_toxicity_classifier')
model2 = RobertaForSequenceClassification.from_pretrained('s-nlp/roberta_toxicity_classifier')

def check_toxicity(text):
    """
    Predicts the general toxicity of the given text using Detoxify.
    
    Args:
        text (str): Input text to evaluate.
    
    Returns:
        float: Toxicity score.
    """
    result = tox_model.predict(text)
    toxicity_score = result.get("toxicity", 0)
    return toxicity_score


def is_custom_toxic(text):
    """
    Checks if text contains any custom-defined toxic phrases,
    optionally combined with modifiers.
    
    Args:
        text (str): Input text to check.
    
    Returns:
        bool: True if custom toxic phrase is found, else False.
    """
    text = text.lower()
    for word in custom_words:
        base = word.lower()
        patterns = [base]
        for m in modifiers:
            patterns.append(f"{m} {base}")
        for p in patterns:
            if re.search(r'\b' + re.escape(p) + r'\b', text):
                return True
    return False

def check_sentiment(text):
    """
    Uses sentiment analysis to score negative sentiment in text.
    
    Args:
        text (str): Input text.
    
    Returns:
        float: Sentiment score.
    """
    result = sentiment_model(text)[0]
    if result["label"] == "NEGATIVE":
        return result["score"]
    return 0


def paraphrase_text_local(text):
    """
    Locally paraphrases text using a BART model trained to convert
    negative text to a positive/neutral tone.
    
    Args:
        text (str): Input text.
    
    Returns:
        str: Paraphrased text.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=100, num_beams=5, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def paraphrase_text(text):
    """
    Paraphrases text using Google Gemini API with a fallback
    to local model if the API fails.
    
    Args:
        text (str): Input text.
    
    Returns:
        str: Paraphrased text.
    """
    prompt = (
        f"Rewrite the following social media comment to keep the meaning very close to the original without adding or removing key ideas. "
        f"The rewritten version should be concise, not exceeding twice the length of the original. "
        f"It should sound friendly, respectful, and either neutral or slightly positive—something teenagers might say casually to each other online. "
        f"Avoid any form of bullying, blaming, sarcasm, mockery, offensive language, or any harsh or judgmental tone. "
        f"Replace all harmful, negative, or offensive expressions with more neutral, respectful language while preserving the original intent of the message. "
        f"Ensure the response is just the rewritten comment with no additional explanation or reasoning. "
        f"The rewritten version should be appropriate for all audiences and sound conversational, like something a teen would write to a friend. "
        f"Reply with the new sentence only: {text}"
    )


    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        return response.text.strip()

    #except Exception as e:
        print(f"Error during paraphrasing: {e}")
        return None
    except Exception as e:
        print("Gemini error:", e)
        
        return paraphrase_text_local(text)
    
    
def check_cyberbullying_with_hatebert(text):
    """
    Uses HateBERT-style model to check toxicity in text.
    
    Args:
        text (str): Input text.
    
    Returns:
        float: Toxicity probability score.
    """
    inputs = tokenizer2(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model2(**inputs)
    probs = F.softmax(outputs.logits, dim=1)
    toxicity_score = probs[0][1].item()  

    #if toxicity_score > 0.4:  
        #return True
    #return False
    return toxicity_score

spacy.cli.download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")


first_person_pronouns = ["I", "me", "my", "mine", "we", "our", "ours"]

def is_person_or_pronoun(text):
    """
    Checks if text mentions another person (not first-person)
    or contains a pronoun referring to someone else.
    
    Args:
        text (str): Input text.
    
    Returns:
        bool: True if another person is mentioned, else False.
    """
    doc = nlp(text)
    
    for token in doc:
        if token.pos_ == "PRON" and token.text.lower() not in [pron.lower() for pron in first_person_pronouns]:
            return True
        
        if token.ent_type_ == "PERSON" or re.match(r"^@", token.text):  # @username
            return True
        
    return False