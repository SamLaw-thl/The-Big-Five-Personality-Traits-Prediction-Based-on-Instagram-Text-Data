from transformers import AutoTokenizer, AutoModelForSequenceClassification
import instaloader
import numpy as np
import database as db
import torch
import os


def softmax(logits: np.ndarray) -> np.ndarray:
    """
    Applies the softmax function to convert logits into probabilities.

    Args:
        logits (np.ndarray): An array of unnormalized logit values.

    Returns:
        np.ndarray: An array of probabilities, each ranging from 0 to 1.
    """
    exp_logits = np.exp(logits - np.max(logits))
    return exp_logits / exp_logits.sum(axis=-1, keepdims=True)


def description_text(profile: instaloader.Profile) -> str:
    """
    Prepares the description text for personality trait prediction.

    Args:
        profile (instaloader.Profile): The Instagram user profile object.

    Returns:
        str: A concatenated string containing user biography and post captions.
    """
    text = ""
    bio_rows, caption_rows = db.retrieve_data(profile)
    for row in bio_rows:
        text += row[0]

    for row in caption_rows:
        text += row[0]

    return text


def personality_detection_microsoft_finetuned(profile: instaloader.Profile, threshold: float=0.05, endpoint: float= 1.0) -> dict[str, tuple[float, float]]:
    """
    Predicts personality traits based on the Microsoft-finetuned personality model by Nasserelsaman.

    Args:
        profile (instaloader.Profile): The Instagram user profile object.
        threshold (float, optional): Threshold for setting low probabilities. Defaults to 0.05.
        endpoint (float, optional): Endpoint for setting high probabilities. Defaults to 1.0.

    Returns:
        dict[str, tuple[float, float]]: A dictionary containing predicted personality traits.
            - Keys: 'Agreeableness', 'Conscientiousness', 'Extraversion', 'Neuroticism', 'Openness'
            - Values: A tuple with two floats (raw probability, adjusted probability)
    """
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







