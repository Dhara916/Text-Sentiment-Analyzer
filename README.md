# Text Sentiment Analyzer

A Streamlit web app that analyzes the emotional tone of any text using **TextBlob** and **NLTK**.

## Features

- Overall sentiment classification — Positive, Negative, or Neutral
- Polarity gauge chart (–1.0 to +1.0)
- Sentence-by-sentence breakdown with per-sentence polarity bar chart
- Subjectivity score
- One-click example texts to try instantly

## Workflow

```
User Text
    ↓
Streamlit UI
    ↓
TextBlob / NLTK
    ↓
Sentiment Result (Polarity + Subjectivity + Label)
```

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/Dhara916/Text_Sentiment_Analyzer.git
cd Text_Sentiment_Analyzer

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## How It Works

| Score Range | Sentiment |
|-------------|-----------|
| > 0.05      | Positive  |
| –0.05 to 0.05 | Neutral |
| < –0.05     | Negative  |

- **Polarity**: –1.0 (very negative) → +1.0 (very positive)
- **Subjectivity**: 0.0 (objective) → 1.0 (subjective)

## Libraries Used

- [Streamlit](https://streamlit.io/) — UI
- [TextBlob](https://textblob.readthedocs.io/) — NLP & Sentiment
- [NLTK](https://www.nltk.org/) — Tokenization & Stopwords
- [Plotly](https://plotly.com/python/) — Charts

---
