from transformers import BertTokenizer, BertForSequenceClassification, AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import database as db
import torch
import os


# Using softmax function to convert the presonality traits output as probabilities ranging from 0 and 1
def softmax(logits):
    exp_logits = np.exp(logits - np.max(logits))
    return exp_logits / exp_logits.sum(axis=-1, keepdims=True)


# Prepare the description text for persaonlity trait prediction
def description_text(profile):
    text = ""
    bio_rows, caption_rows = db.retrieve_data(profile)
    for row in bio_rows:
        text += row[0]

    for row in caption_rows:
        text += row[0]

    return text


# Personality detection based on bert-based personality model by Minej
def personality_detection_bert_base(profile):
    # Load the tokenizer and model from Hugging Face
    tokenizer = BertTokenizer.from_pretrained("Minej/bert-base-personality")
    model = BertForSequenceClassification.from_pretrained("Minej/bert-base-personality")

    text = description_text(profile)

    # Tokenize the input text
    inputs = tokenizer(text, truncation=True, padding=True, return_tensors="pt")

    # Get model prediction
    outputs = model(**inputs)
    predictions = outputs.logits.squeeze().detach().numpy()

    # Apply softmax to the prediction to get probabilities
    probabilities = softmax(predictions)

    # define personality traits
    label_names = ['Extroversion', 'Neuroticism', 'Agreeableness', 'Conscientiousness', 'Openness']

    # Map predictions to traits
    result = {label_names[i]: round(float(probabilities[i]), 2) for i in range(len(label_names))}

    return result


# Personality detection based on microsoft-finetuned personality model by Nasserelsaman
def personality_detection_microsoft_finetuned(profile, threshold=0.05, endpoint= 1.0):
    token=os.getenv('huggingface_access_token')
    tokenizer = AutoTokenizer.from_pretrained ("Nasserelsaman/microsoft-finetuned-personality",token=token)
    model = AutoModelForSequenceClassification.from_pretrained ("Nasserelsaman/microsoft-finetuned-personality",token=token)

    text = description_text(profile)

    inputs = tokenizer(text, truncation=True, padding='max_length', return_tensors="pt", max_length=512)
    outputs = model(**inputs)
    predictions = outputs.logits.squeeze().detach().numpy()
        
    # Get raw logits
    logits = model(**inputs).logits
        
    # Apply sigmoid to squash between 0 and 1
    probabilities = torch.sigmoid(logits)

    # Convert a probabilities tensor into a 1 dimensional probabilities list
    probabilities = probabilities.flatten().tolist()

    # Set values less than the threshold to 0.05
    predictions[predictions < threshold] = 0.05
    predictions[predictions > endpoint] = 1.0
        
    label_names = ['Agreeableness', 'Conscientiousness', 'Extraversion', 'Neuroticism', 'Openness']
    result = {label_names[i]: (probabilities[i], predictions[i]) for i in range(len(label_names))}
        
    return result



