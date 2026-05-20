# 🔐 Email Fraud Detection

This project builds a Natural Language Processing (NLP) machine learning pipeline to classify email communications as spam/phishing/fraud (Label `1`) or legitimate/ham (Label `0`). It transforms raw unstructured text into TF-IDF vector features and fits classifiers to predict security risks.

## 🎯 Objectives
- Clean and convert raw text messages into a structured sparse matrix using TF-IDF.
- Train and compare two classification models: **Multinomial Naive Bayes** (probabilistic) and **Logistic Regression** (linear).
- Calculate performance benchmarks: Accuracy, Precision, Recall, and F1-Score.
- Extract and visualize keywords that trigger fraud/spam alarms versus those indicating trusted emails.

## 🛠️ Tech Stack
- **Text Processing & ML**: Python, Scikit-learn (TfidfVectorizer, MultinomialNB, LogisticRegression, train_test_split)
- **Data Handling**: Pandas, Numpy
- **Data Visualization**: Matplotlib, Seaborn

## ⚙️ Mathematical Model
1. **Term Frequency-Inverse Document Frequency (TF-IDF)**:
   $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$
   Where:
   - $\text{TF}(t, d)$ is the frequency of word $t$ in email $d$.
   - $\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$, scaling down frequent words (e.g. "the", "and").
2. **Naive Bayes Classifier**:
   $$P(\text{Spam} | \text{Words}) \propto P(\text{Spam}) \prod_{i=1}^{n} P(w_i | \text{Spam})$$
   Classifies the email as spam if the posterior probability exceeds that of ham.

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate synthetic email dataset:
   ```bash
   python generate_data.py
   ```
3. Run the vectorization, training, and evaluation script:
   ```bash
   python analysis.py
   ```

## 📊 Key Deliverables
- `email_dataset.csv`: Simulated text corpus comprising spam/phishing messages and business/personal communications.
- `email_classifier_comparison.csv`: Comparative model performance sheet.
- `visualizations/confusion_matrix.png`: Confusion matrix mapping True Positives, False Positives, True Negatives, and False Negatives.
- `visualizations/feature_coefficients.png`: Visual chart showing words with the strongest mathematical coefficients indicating Spam (red) and Ham (blue).
