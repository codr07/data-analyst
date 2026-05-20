# 💬 Social Media Sentiment Analysis

This project implements a Natural Language Processing (NLP) pipeline to clean, process, and classify the sentiment of social media posts (e.g., product feedback, reviews, tweets) into Positive, Neutral, or Negative categories.

## 🎯 Objectives
- Build a text cleaning utility to preprocess social media text (handles, hashtags, punctuation).
- Determine post sentiment using polarity scoring.
- Calculate performance accuracy against ground truth annotations.
- Visualize sentiment distributions and extract key positive/negative terms using horizontal bar graphs and Word Clouds.

## 🛠️ Tech Stack
- **Data Handling**: Pandas, Numpy
- **Natural Language Processing**: TextBlob, Regex tokenization
- **Data Visualization**: Matplotlib, WordCloud

## ⚙️ Architecture & Fallback
The sentiment analysis pipeline uses a layered approach to ensure the code is **resilient and unbreakable**:
- **Primary Engine**: `TextBlob` API for NLP polarity calculation.
- **Graceful Fallback**: If the `textblob` library is unavailable, the pipeline falls back to an integrated rule-based `SimpleSentimentAnalyzer` which matches terms against curated lexicons of positive and negative tokens.

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate the synthetic social media dataset:
   ```bash
   python generate_data.py
   ```
3. Run the sentiment classification and visualization pipeline:
   ```bash
   python analysis.py
   ```

## 📊 Key Deliverables
- `social_media_posts.csv`: Raw dataset containing posts, authors, timestamps, and target sentiment classes.
- `sentiment_analysis_output.csv`: Output table enriched with predicted sentiment classes and numerical polarity scores.
- `visualizations/sentiment_distribution.png`: Bar chart demonstrating category distribution.
- `visualizations/word_frequencies.png`: Horizontal bar charts showing top terms used in positive vs. negative posts.
- `visualizations/positive_wordcloud.png` & `visualizations/negative_wordcloud.png`: Word clouds of positive and negative keywords (generated if the `wordcloud` library is installed).
