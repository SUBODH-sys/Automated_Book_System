from transformers import pipeline
import os

# Initialize Hugging Face pipelines
paraphraser = pipeline("text2text-generation", model="t5-small", device=-1, clean_up_tokenization_spaces=True)  # CPU for simplicity
reviewer = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english", device=-1)

def spin_content(text):
    """
    Spin (paraphrase) content using T5 model.
    """
    try:
        # Split text into chunks to handle model input limits
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        spun_chunks = []
        for chunk in chunks:
            result = paraphraser(f"paraphrase: {chunk}", max_length=150, num_return_sequences=1)
            spun_chunks.append(result[0]["generated_text"])
        spun_text = "\n".join(spun_chunks)
        
        # Save spun content
        output_path = "data/content/chapter1_spun.txt"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(spun_text)
        
        return spun_text
    
    except Exception as e:
        raise Exception(f"Content spinning failed: {str(e)}")

def review_content(text):
    """
    Review content for sentiment and provide feedback using DistilBERT.
    """
    try:
        # Analyze sentiment for the first 512 characters (model limit)
        result = reviewer(text[:512])
        sentiment = result[0]["label"]
        score = result[0]["score"]
        review_note = f"Sentiment: {sentiment}, Confidence: {score:.2f}"
        
        # Provide suggestions based on sentiment
        if sentiment == "NEGATIVE":
            review_note += "\nSuggestion: Revise for clarity and positive tone."
        elif score < 0.7:
            review_note += "\nSuggestion: Improve coherence and flow."
        
        # Save reviewed content and feedback
        output_path = "data/content/chapter1_reviewed.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"{text}\n\n--- Review Notes ---\n{review_note}")
        
        return text, review_note
    
    except Exception as e:
        raise Exception(f"Content review failed: {str(e)}")