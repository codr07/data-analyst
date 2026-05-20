# 🧠 Medical Diagnosis using Deep Learning

This project implements a Multi-Layer Perceptron (MLP) Deep Neural Network to assist in medical diagnostic classification (detecting high-risk patients based on key clinical biomarkers). It features full dataset scaling, dense multilayer network modeling, and comprehensive classification validation with a strong emphasis on medical sensitivity (Recall).

## 🎯 Objectives
- Build a structured patient biomarker database capturing clinical details (Age, BMI, Blood Pressure, Glucose levels, Cholesterol, and Insulin).
- Preprocess medical data using standardization scaling.
- Build a Dense Feed-Forward Neural Network to classify patients.
- Compute critical diagnostic evaluation parameters (Accuracy, Precision, Recall/Sensitivity, F1-Score, and ROC-AUC).
- Plot training loss curves and Receiver Operating Characteristic (ROC) curves.

## 🛠️ Tech Stack
- **Deep Learning & Modeling**: Python, TensorFlow / Keras (Sequential API), Scikit-learn (MLPClassifier fallback, StandardScaler)
- **Data Engineering**: Pandas, Numpy
- **Data Visualization**: Matplotlib

## ⚙️ Model Architecture & Fallback
To ensure complete system reliability (**unbreakable standard**), the modeling pipeline uses an adaptive classifier:
1. **Primary Network**: Keras Sequential deep neural network (Dense 32, ReLU -> Dropout 0.2 -> Dense 16, ReLU -> Dense 1, Sigmoid), optimized using Adam optimization and binary cross-entropy loss.
2. **Fallback Network**: If `tensorflow` is not present in the local environment, the pipeline falls back to Scikit-learn's `MLPClassifier` running three feed-forward hidden layers `(32, 16, 8)`.

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate synthetic diagnostic biomarker data:
   ```bash
   python generate_data.py
   ```
3. Run the Deep Learning training and evaluation pipeline:
   ```bash
   python analysis.py
   ```

## 📊 Key Deliverables
- `patient_records.csv`: Simulated patient clinical records.
- `patient_diagnosis_metrics.csv`: Performance datasheet recording Accuracy, Recall (Sensitivity), and ROC-AUC.
- `visualizations/neural_network_loss.png`: Iterative loss convergence curve mapping gradient steps.
- `visualizations/roc_curve.png`: ROC plot calculating True Positive Rate vs False Positive Rate.
