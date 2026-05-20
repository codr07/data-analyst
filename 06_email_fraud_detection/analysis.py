import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("[*] Starting Email Fraud Detection Analysis...")
    csv_file = "email_dataset.csv"
    
    if not os.path.exists(csv_file):
        print(f"[-] Data file {csv_file} not found! Run generate_data.py first.")
        return
        
    df = pd.read_csv(csv_file)
    print(f"[+] Loaded {len(df)} emails.")
    
    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(df['Text'], df['Label'], test_size=0.2, random_state=42)
    
    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train Multinomial Naive Bayes
    nb_model = MultinomialNB()
    nb_model.fit(X_train_vec, y_train)
    nb_preds = nb_model.predict(X_test_vec)
    
    # Train Logistic Regression (for comparison)
    lr_model = LogisticRegression(random_state=42)
    lr_model.fit(X_train_vec, y_train)
    lr_preds = lr_model.predict(X_test_vec)
    
    # Performance metrics
    metrics = {
        'Classifier': ['Naive Bayes', 'Logistic Regression'],
        'Accuracy': [accuracy_score(y_test, nb_preds), accuracy_score(y_test, lr_preds)],
        'Precision': [precision_score(y_test, nb_preds), precision_score(y_test, lr_preds)],
        'Recall': [recall_score(y_test, nb_preds), recall_score(y_test, lr_preds)],
        'F1_Score': [f1_score(y_test, nb_preds), f1_score(y_test, lr_preds)]
    }
    
    metrics_df = pd.DataFrame(metrics)
    print("\n" + "="*80)
    print("                    MODEL PERFORMANCE COMPARISON")
    print("="*80)
    print(metrics_df.to_string(index=False))
    print("="*80)
    
    # Detailed classification report for the primary classifier (Naive Bayes)
    print("\nNaive Bayes Classification Report:")
    print(classification_report(y_test, nb_preds, target_names=['Ham', 'Spam/Fraud']))
    
    # Save metrics report
    metrics_df.to_csv("email_classifier_comparison.csv", index=False)
    print("[+] Saved metrics summary to email_classifier_comparison.csv")
    
    # Create visualizations
    os.makedirs("visualizations", exist_ok=True)
    
    # Plot Confusion Matrix for Naive Bayes
    cm = confusion_matrix(y_test, nb_preds)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Ham', 'Spam/Fraud'], yticklabels=['Ham', 'Spam/Fraud'])
    plt.title('Naive Bayes Confusion Matrix', fontsize=12, fontweight='bold')
    plt.ylabel('Actual Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig("visualizations/confusion_matrix.png", dpi=150)
    plt.close()
    
    # Plot Feature Importance (Logistic Regression Coefficients)
    feature_names = vectorizer.get_feature_names_out()
    coefs = lr_model.coef_[0]
    coef_df = pd.DataFrame({'Word': feature_names, 'Coefficient': coefs})
    # Top 10 words indicating Spam (positive coefficients) and Top 10 words indicating Ham (negative coefficients)
    top_spam_words = coef_df.sort_values(by='Coefficient', ascending=False).head(10)
    top_ham_words = coef_df.sort_values(by='Coefficient', ascending=True).head(10)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    sns.barplot(ax=axes[0], data=top_spam_words, x='Coefficient', y='Word', palette='Reds_r')
    axes[0].set_title('Top 10 Words Predicting Fraud/Spam', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Coefficient (Spam Association)')
    
    sns.barplot(ax=axes[1], data=top_ham_words, x='Coefficient', y='Word', palette='Blues')
    axes[1].set_title('Top 10 Words Predicting Legitimate/Ham', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Coefficient (Ham Association)')
    
    plt.tight_layout()
    plt.savefig("visualizations/feature_coefficients.png", dpi=150)
    plt.close()
    print("[+] Saved charts to visualizations/confusion_matrix.png and visualizations/feature_coefficients.png")
    
    print("[+] Email Fraud Detection analysis finished successfully!")

if __name__ == "__main__":
    main()
