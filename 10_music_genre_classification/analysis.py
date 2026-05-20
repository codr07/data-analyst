import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

# Feature extraction template using librosa (Mock example for user reference)
def extract_features_from_audio(file_path):
    """
    Template showing how features are extracted from a real WAV file using librosa.
    This function acts as a wrapper demonstrating the bridging between raw audio and tabular ML features.
    """
    try:
        import librosa
        print(f"[*] Loading audio file {file_path} via librosa...")
        y, sr = librosa.load(file_path, duration=30)
        
        # Extract features
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        chroma = np.mean(librosa.feature.chroma_stft(y=y, sr=sr))
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
        rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=5), axis=1)
        
        # Package features
        features = [
            tempo[0] if isinstance(tempo, (list, np.ndarray)) else tempo,
            chroma, centroid, bandwidth, rolloff, zcr
        ]
        features.extend(mfccs)
        return np.array(features).reshape(1, -1)
        
    except ImportError:
        print("[!] librosa library not found. Returning mock feature vector for demonstration.")
        # Return mock features (Rock-like profile)
        return np.array([[120.0, 0.40, 2100.0, 2200.0, 4500.0, 0.10, -115.0, 88.0, -28.0, 18.0, -18.0]])

def main():
    print("[*] Starting Music Genre Classification Analysis...")
    csv_file = "music_features.csv"
    
    if not os.path.exists(csv_file):
        print(f"[-] Data file {csv_file} not found! Run generate_data.py first.")
        return
        
    df = pd.read_csv(csv_file)
    print(f"[+] Loaded {len(df)} songs with acoustic features.")
    
    features = [
        "Tempo", "Chroma_STFT", "Spectral_Centroid", "Spectral_Bandwidth", 
        "Rolloff", "Zero_Crossing_Rate", "MFCC_1", "MFCC_2", "MFCC_3", "MFCC_4", "MFCC_5"
    ]
    X = df[features]
    y = df["Genre"]
    
    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train SVM Classifier
    svm = SVC(kernel='rbf', C=5.0, probability=True, random_state=42)
    svm.fit(X_train_scaled, y_train)
    svm_preds = svm.predict(X_test_scaled)
    
    # Train Random Forest Classifier (for comparison)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    
    # Evaluate
    svm_acc = accuracy_score(y_test, svm_preds)
    rf_acc = accuracy_score(y_test, rf_preds)
    svm_f1 = f1_score(y_test, svm_preds, average='macro')
    rf_f1 = f1_score(y_test, rf_preds, average='macro')
    
    print("\n" + "="*50)
    print("      GENRE CLASSIFICATION MODEL COMPARISON")
    print("="*50)
    print(f"SVM Accuracy:          {svm_acc:.4f} (Macro F1: {svm_f1:.4f})")
    print(f"Random Forest Accuracy: {rf_acc:.4f} (Macro F1: {rf_f1:.4f})")
    print("="*50)
    
    # Save performance metrics
    metrics_df = pd.DataFrame({
        'Model': ['SVM', 'Random Forest'],
        'Accuracy': [svm_acc, rf_acc],
        'Macro_F1': [svm_f1, rf_f1]
    })
    metrics_df.to_csv("music_classifier_comparison.csv", index=False)
    
    # Create visualizations
    os.makedirs("visualizations", exist_ok=True)
    
    # Plot 1: Confusion Matrix for SVM
    genres = sorted(y.unique())
    cm = confusion_matrix(y_test, svm_preds)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Purples', xticklabels=genres, yticklabels=genres)
    plt.title('SVM Music Genre Confusion Matrix', fontsize=12, fontweight='bold')
    plt.ylabel('Actual Genre')
    plt.xlabel('Predicted Genre')
    plt.tight_layout()
    plt.savefig("visualizations/confusion_matrix.png", dpi=150)
    plt.close()
    
    # Plot 2: 2D PCA Projection of Acoustic Feature Space
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(scaler.fit_transform(X))
    pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
    pca_df['Genre'] = y
    
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Genre', palette='Set1', alpha=0.7, edgecolors='w', s=50)
    plt.title('2D PCA Projection of Acoustic Feature Space', fontsize=12, fontweight='bold')
    plt.xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)')
    plt.ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("visualizations/pca_feature_space.png", dpi=150)
    plt.close()
    print("[+] Saved charts to visualizations/confusion_matrix.png and visualizations/pca_feature_space.png")
    
    # Test feature extraction template (Mock execution check)
    print("\n[*] Testing audio feature extraction template with mock WAV path...")
    mock_features = extract_features_from_audio("sample_song.wav")
    mock_features_scaled = scaler.transform(mock_features)
    pred_genre = svm.predict(mock_features_scaled)[0]
    print(f"[+] Predicted genre for sample_song.wav: {pred_genre}")
    
    print("[+] Music Genre Classification analysis finished successfully!")

if __name__ == "__main__":
    main()
