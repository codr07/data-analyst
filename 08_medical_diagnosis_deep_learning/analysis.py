import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt

def main():
    print("[*] Starting Medical Diagnosis Deep Learning Pipeline...")
    csv_file = "patient_records.csv"
    
    if not os.path.exists(csv_file):
        print(f"[-] Data file {csv_file} not found! Run generate_data.py first.")
        return
        
    df = pd.read_csv(csv_file)
    print(f"[+] Loaded {len(df)} patient records.")
    
    # Features and target
    features = ["Age", "BMI", "Blood_Pressure", "Glucose_Level", "Cholesterol", "Insulin"]
    X = df[features]
    y = df["Diagnosis"]
    
    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Check for TensorFlow/Keras or PyTorch, else use MLPClassifier from sklearn
    use_tf = False
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Dropout
        from tensorflow.keras.callbacks import EarlyStopping
        use_tf = True
        print("[+] TensorFlow library detected. Building Deep Neural Network using Keras.")
    except ImportError:
        print("[*] TensorFlow not installed. Using Scikit-Learn MLPClassifier for Neural Network.")
        
    # Create visualizations folder
    os.makedirs("visualizations", exist_ok=True)
    
    if use_tf:
        # Build Keras MLP
        model = Sequential([
            Dense(32, activation='relu', input_shape=(len(features),)),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        
        # Fit model
        early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        history = model.fit(
            X_train_scaled, y_train,
            epochs=100,
            batch_size=32,
            validation_split=0.2,
            callbacks=[early_stop],
            verbose=0
        )
        
        # Predict probabilities and classes
        probs = model.predict(X_test_scaled).flatten()
        preds = (probs > 0.5).astype(int)
        
        # Plot Loss Curves
        plt.figure(figsize=(8, 5))
        plt.plot(history.history['loss'], label='Train Loss', color='#2980b9', linewidth=2)
        plt.plot(history.history['val_loss'], label='Val Loss', color='#e74c3c', linewidth=2)
        plt.title('Deep Neural Network Training Loss Curve', fontsize=12, fontweight='bold')
        plt.xlabel('Epochs')
        plt.ylabel('Binary Crossentropy')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.savefig("visualizations/neural_network_loss.png", dpi=150)
        plt.close()
        print("[+] Saved training curves to visualizations/neural_network_loss.png")
        
    else:
        # Scikit-Learn MLPClassifier
        # 3 hidden layers (32 neurons, 16 neurons, 8 neurons)
        mlp = MLPClassifier(hidden_layer_sizes=(32, 16, 8), max_iter=300, random_state=42, early_stopping=True)
        mlp.fit(X_train_scaled, y_train)
        
        preds = mlp.predict(X_test_scaled)
        probs = mlp.predict_proba(X_test_scaled)[:, 1]
        
        # Plot Loss Curve
        plt.figure(figsize=(8, 5))
        plt.plot(mlp.loss_curve_, label='Training Loss', color='#2980b9', linewidth=2)
        plt.title('MLP Classifier Training Loss Curve', fontsize=12, fontweight='bold')
        plt.xlabel('Iterations')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.savefig("visualizations/neural_network_loss.png", dpi=150)
        plt.close()
        print("[+] Saved training curves to visualizations/neural_network_loss.png")
        
    # Calculate classification metrics
    accuracy = accuracy_score(y_test, preds)
    precision = precision_score(y_test, preds)
    recall = recall_score(y_test, preds)  # Sensitivity/True Positive Rate
    f1 = f1_score(y_test, preds)
    roc_auc = roc_auc_score(y_test, probs)
    
    print("\n" + "="*40)
    print("      DIAGNOSIS MODEL METRICS")
    print("="*40)
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f} (Sensitivity)")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    print("="*40)
    
    # Save metrics report
    metrics_df = pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall (Sensitivity)', 'F1-Score', 'ROC-AUC'],
        'Value': [accuracy, precision, recall, f1, roc_auc]
    })
    metrics_df.to_csv("patient_diagnosis_metrics.csv", index=False)
    
    # Plot ROC Curve
    fpr, tpr, _ = roc_curve(y_test, probs)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='#e67e22', lw=2.5, label=f'ROC Curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='#7f8c8d', linestyle='--', lw=1.5)
    plt.title('ROC Curve for Patient Diagnosis Classifier', fontsize=12, fontweight='bold')
    plt.xlabel('False Positive Rate (1 - Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity / Recall)')
    plt.legend(loc='lower right')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("visualizations/roc_curve.png", dpi=150)
    plt.close()
    
    print("[+] Saved ROC Curve plot to visualizations/roc_curve.png")
    print("[+] Medical diagnosis pipeline finished successfully!")

if __name__ == "__main__":
    main()
