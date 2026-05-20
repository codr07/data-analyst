import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# A lightweight fallback rule-based sentiment analyzer in case TextBlob is not installed
class SimpleSentimentAnalyzer:
    def __init__(self):
        self.positive_words = {
            'love', 'great', 'best', 'incredible', 'fast', 'smooth', 'excellent', 'fantastic',
            'impressed', 'clean', 'save', 'game', 'changer', 'premium', 'elegant', 'stunning',
            'happy', 'perfect', 'awesome', 'good', 'ux', 'support', 'resolved'
        }
        self.negative_words = {
            'disappointed', 'slow', 'rip-off', 'bug', 'outdated', 'crash', 'clunky',
            'unresponsive', 'waste', 'lag', 'crashed', 'timeout', 'expensive', 'freeze',
            'freezing', 'terrible', 'error', 'failed', 'bad', 'worst', 'hate'
        }
        
    def analyze(self, text):
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        
        if pos_count > neg_count:
            return 'Positive', 0.5 + (0.1 * (pos_count - neg_count))
        elif neg_count > pos_count:
            return 'Negative', -0.5 - (0.1 * (neg_count - pos_count))
        else:
            return 'Neutral', 0.0

def main():
    print("[*] Starting Social Media Sentiment Analysis...")
    csv_file = "social_media_posts.csv"
    
    if not os.path.exists(csv_file):
        print(f"[-] Data file {csv_file} not found! Run generate_data.py first.")
        return
        
    df = pd.read_csv(csv_file)
    print(f"[+] Loaded {len(df)} social media posts.")
    
    # Try importing TextBlob
    use_textblob = False
    try:
        from textblob import TextBlob
        use_textblob = True
        print("[+] TextBlob library detected. Using TextBlob for sentiment analysis.")
    except ImportError:
        print("[*] TextBlob not installed. Using fallback rule-based SimpleSentimentAnalyzer.")
        analyzer = SimpleSentimentAnalyzer()
        
    # Run sentiment analysis
    pred_sentiments = []
    polarities = []
    
    for text in df['Text']:
        if use_textblob:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            polarities.append(polarity)
            if polarity > 0.1:
                pred_sentiments.append('Positive')
            elif polarity < -0.1:
                pred_sentiments.append('Negative')
            else:
                pred_sentiments.append('Neutral')
        else:
            sentiment, polarity = analyzer.analyze(text)
            pred_sentiments.append(sentiment)
            polarities.append(polarity)
            
    df['Predicted_Sentiment'] = pred_sentiments
    df['Polarity'] = polarities
    
    # Calculate accuracy comparing to True_Sentiment
    correct = (df['Predicted_Sentiment'] == df['True_Sentiment']).sum()
    accuracy = (correct / len(df)) * 100
    print(f"[+] Sentiment Analysis Accuracy: {accuracy:.2f}%")
    
    # Save the classification output
    df.to_csv("sentiment_analysis_output.csv", index=False)
    print("[+] Saved predictions to sentiment_analysis_output.csv")
    
    # Create visualizations directory
    os.makedirs("visualizations", exist_ok=True)
    
    # Visualization 1: Sentiment Distribution Chart
    plt.figure(figsize=(8, 6))
    colors = ['#2ecc71', '#95a5a6', '#e74c3c']
    sentiment_counts = df['Predicted_Sentiment'].value_counts()
    # Order them logically
    ordered_counts = [sentiment_counts.get('Positive', 0), sentiment_counts.get('Neutral', 0), sentiment_counts.get('Negative', 0)]
    plt.bar(['Positive', 'Neutral', 'Negative'], ordered_counts, color=colors, edgecolor='none', width=0.6)
    plt.title('Sentiment Distribution on Social Media', fontsize=14, fontweight='bold', color='#2c3e50')
    plt.xlabel('Sentiment Class')
    plt.ylabel('Count')
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.savefig("visualizations/sentiment_distribution.png", dpi=150)
    plt.close()
    
    # Visualization 2: Word Frequency analysis for Positive and Negative sentiments
    # Tokenize and count words
    def get_word_freq(texts):
        word_counts = {}
        stop_words = {'the', 'is', 'and', 'a', 'to', 'in', 'it', 'has', 'for', 'on', 'with', 'our', 'this', 'my', 'that', 'of', 'we', 'i'}
        for text in texts:
            words = re.findall(r'\b\w+\b', text.lower())
            for w in words:
                if len(w) > 2 and w not in stop_words:
                    word_counts[w] = word_counts.get(w, 0) + 1
        return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
    pos_texts = df[df['Predicted_Sentiment'] == 'Positive']['Text']
    neg_texts = df[df['Predicted_Sentiment'] == 'Negative']['Text']
    
    pos_words = get_word_freq(pos_texts)
    neg_words = get_word_freq(neg_texts)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    if pos_words:
        words, counts = zip(*pos_words)
        axes[0].barh(words, counts, color='#2ecc71')
        axes[0].set_title('Top Positive Words', fontsize=12, fontweight='bold')
        axes[0].invert_yaxis()
        
    if neg_words:
        words, counts = zip(*neg_words)
        axes[1].barh(words, counts, color='#e74c3c')
        axes[1].set_title('Top Negative Words', fontsize=12, fontweight='bold')
        axes[1].invert_yaxis()
        
    plt.tight_layout()
    plt.savefig("visualizations/word_frequencies.png", dpi=150)
    plt.close()
    print("[+] Saved word frequencies to visualizations/word_frequencies.png")
    
    # Try generating a WordCloud if installed
    try:
        from wordcloud import WordCloud
        print("[*] WordCloud detected. Generating positive and negative word clouds...")
        
        all_pos_text = " ".join(pos_texts)
        all_neg_text = " ".join(neg_texts)
        
        # Positive WordCloud
        wc_pos = WordCloud(width=600, height=400, background_color='white', colormap='summer').generate(all_pos_text)
        wc_pos.to_file("visualizations/positive_wordcloud.png")
        
        # Negative WordCloud
        wc_neg = WordCloud(width=600, height=400, background_color='white', colormap='autumn').generate(all_neg_text)
        wc_neg.to_file("visualizations/negative_wordcloud.png")
        print("[+] Saved WordClouds to visualizations/")
    except ImportError:
        print("[*] WordCloud not installed. Skipping WordCloud generation.")
        
    print("[+] Social Media Sentiment Analysis finished successfully!")

if __name__ == "__main__":
    main()
