import nltk
from textblob import TextBlob

# Download required NLTK data (runs once)
def download_nltk_data():
    packages = ["punkt", "punkt_tab", "stopwords", "wordnet", "averaged_perceptron_tagger"]
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass

download_nltk_data()


def clean_text(text: str) -> str:
    """Basic text cleaning."""
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    import string

    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    # Keep stop words for sentiment — only strip punctuation
    cleaned = [t for t in tokens if t not in string.punctuation]
    return " ".join(cleaned)


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of given text.
    Returns a dict with:
        - sentiment: 'Positive' | 'Negative' | 'Neutral'
        - polarity: float in [-1.0, 1.0]
        - subjectivity: float in [0.0, 1.0]
        - emoji: matching emoji
        - color: hex color for UI
        - word_count: int
        - cleaned_text: str
    """
    if not text or not text.strip():
        return {
            "sentiment": "Neutral",
            "polarity": 0.0,
            "subjectivity": 0.0,
            "emoji": "😐",
            "color": "#FFA500",
            "word_count": 0,
            "cleaned_text": "",
        }

    cleaned = clean_text(text)
    blob = TextBlob(cleaned)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.05:
        sentiment, emoji, color = "Positive", "😊", "#2ECC71"
    elif polarity < -0.05:
        sentiment, emoji, color = "Negative", "😞", "#E74C3C"
    else:
        sentiment, emoji, color = "Neutral", "😐", "#F39C12"

    # Word-level breakdown
    words = text.split()

    return {
        "sentiment": sentiment,
        "polarity": round(polarity, 4),
        "subjectivity": round(subjectivity, 4),
        "emoji": emoji,
        "color": color,
        "word_count": len(words),
        "cleaned_text": cleaned,
    }


def get_sentence_sentiments(text: str) -> list[dict]:
    """Break text into sentences and analyze each."""
    blob = TextBlob(text)
    results = []
    for sentence in blob.sentences:
        result = analyze_sentiment(str(sentence))
        result["sentence"] = str(sentence)
        results.append(result)
    return results