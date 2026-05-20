# 🎵 Music Genre Classification

This project implements a multi-class machine learning classification pipeline to categorize musical tracks into genres (Classical, Jazz, Pop, Rock, Hip-hop) based on numerical acoustic features. It also outlines the preprocessing steps required to transform raw audio (WAV files) into tabular feature vectors using the `librosa` library.

## 🎯 Objectives
- Map raw signal properties (MFCCs, spectral shape, beat tempo) to musical genres.
- Implement a feature scaling pipeline to normalize feature units (e.g. BPM vs. Chroma scale).
- Train and compare:
  - **Support Vector Machine (SVM)** with radial basis function (RBF) kernel.
  - **Random Forest Classifier** (tree-based ensemble).
- Evaluate multi-class classification metrics (Accuracy, Macro-F1).
- Visualize class clustering using 2D Principal Component Analysis (PCA) projection.
- Demonstrate audio loading and feature extraction from WAV files using the `librosa` library.

## 🛠️ Tech Stack
- **Audio Processing**: Librosa (Signal handling)
- **Machine Learning**: Scikit-learn (SVC, RandomForestClassifier, StandardScaler, PCA, train_test_split)
- **Data Engineering**: Pandas, Numpy
- **Data Visualization**: Matplotlib, Seaborn

## ⚙️ Acoustic Feature Descriptions
- **Tempo**: Estimated Beats Per Minute (BPM).
- **Chroma STFT (Short-Time Fourier Transform)**: Measures the energy distribution across 12 semitone pitch classes.
- **Spectral Centroid**: Represents the "center of gravity" of the audio spectrum, indicating brightness.
- **Spectral Bandwidth**: Measures the spread of the spectrum around the centroid.
- **Spectral Rolloff**: The frequency below which 85% of the spectral energy lies.
- **Zero Crossing Rate (ZCR)**: The rate at which the audio signal changes sign (indicating noise/percussiveness).
- **Mel-Frequency Cepstral Coefficients (MFCCs)**: A representation of the short-term power spectrum of a sound (features 1-5 captured).

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate synthetic acoustic features dataset:
   ```bash
   python generate_data.py
   ```
3. Run the classification, dimensionality reduction, and evaluation pipeline:
   ```bash
   python analysis.py
   ```

## 📊 Key Deliverables
- `music_features.csv`: Acoustic features generated for 1,000 tracks.
- `music_classifier_comparison.csv`: Validation statistics comparing SVM and Random Forest models.
- `visualizations/confusion_matrix.png`: Multi-class confusion matrix mapping predictions against ground truth labels.
- `visualizations/pca_feature_space.png`: 2D PCA scatter plot showing how distinct genres form clean clusters in acoustic feature space.
