import numpy as np
import pandas as pd
import matplotlib
# Use non-interactive Agg backend to prevent plt.show() from blocking
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Try to import TensorFlow for the DL part, fall back to scikit-learn's MLPClassifier if it fails
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout
    USE_TF = True
    print("TensorFlow imported successfully!")
except Exception as e:
    print(f"TensorFlow loading failed: {e}")
    print("Falling back to scikit-learn MLPClassifier (Neural Network)...")
    from sklearn.neural_network import MLPClassifier
    USE_TF = False

# 1. Fetch Real Data Directly from URL
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/breast-cancer-wisconsin.csv"

# This dataset doesn't have headers in its raw file, so we define them manually
column_names = [
    "clump_thickness", "uniformity_cell_size", "uniformity_cell_shape",
    "marginal_adhesion", "single_epithelial_cell_size", "bare_nuclei", 
    "bland_chromatin", "normal_nucleoli", "mitoses", "class"
]

df = pd.read_csv(url, names=column_names)
print(f"Real dataset loaded successfully! Shape: {df.shape}")

# 2. Data Cleaning (Handling real-world missing values denoted by '?')
df.replace('?', np.nan, inplace=True)
df.dropna(inplace=True) # Drop the rows with missing values
df['bare_nuclei'] = df['bare_nuclei'].astype(int) # Convert column to integer

# Map target: Original dataset uses 2 for Benign and 4 for Malignant. Let's make it 0 and 1.
df['class'] = df['class'].map({2: 0, 4: 1})

# Drop target column to get features (no ID column exists in this dataset version)
X = df.drop(columns=['class'])
y = df['class']

# 3. Train-Test Split & Normalization
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Data processed and split into Train/Test sets.")

# =====================================================================
# MACHINE LEARNING (Random Forest)
# =====================================================================
print("\nTraining Machine Learning Model (Random Forest)...")
ml_model = RandomForestClassifier(n_estimators=100, random_state=42)
ml_model.fit(X_train_scaled, y_train)

ml_preds = ml_model.predict(X_test_scaled)
ml_acc = accuracy_score(y_test, ml_preds)
print(f"ML Random Forest Accuracy: {ml_acc * 100:.2f}%")

# =====================================================================
# DEEP LEARNING (Artificial Neural Network - ANN)
# =====================================================================
print("\nTraining Deep Learning Model (Neural Network)...")

if USE_TF:
    # Build the structure of Neural Network using Keras
    dl_model = Sequential([
        Dense(32, activation='relu', input_shape=(X_train_scaled.shape[1],)),
        Dropout(0.2), # Prevents overfitting
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid') # Binary output layer (0 or 1)
    ])

    # Compile the Neural Network
    dl_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the Neural Network
    history = dl_model.fit(
        X_train_scaled, y_train, 
        validation_split=0.1, 
        epochs=25, 
        batch_size=16, 
        verbose=0 # Suppress long epoch log outputs
    )

    # Evaluate Deep Learning Model
    dl_loss, dl_acc = dl_model.evaluate(X_test_scaled, y_test, verbose=0)
else:
    # Train using scikit-learn MLPClassifier (Multi-Layer Perceptron)
    dl_model = MLPClassifier(
        hidden_layer_sizes=(32, 16),
        activation='relu',
        solver='adam',
        max_iter=500,
        batch_size=16,
        random_state=42
    )
    dl_model.fit(X_train_scaled, y_train)
    dl_preds = dl_model.predict(X_test_scaled)
    dl_acc = accuracy_score(y_test, dl_preds)

print(f"DL Neural Network Accuracy: {dl_acc * 100:.2f}%")

# =====================================================================
# COMPARISON VISUALIZATION
# =====================================================================
print("\nGenerating Project Comparison Metrics...")

plt.figure(figsize=(6, 4))
models = ['ML (Random Forest)', 'DL (Neural Network)']
accuracies = [ml_acc * 100, dl_acc * 100]

sns.barplot(x=models, y=accuracies, hue=models, palette='Set2', legend=False)
plt.ylabel('Accuracy Score (%)')
plt.title('Performance Comparison: Machine Learning vs. Deep Learning')
for i, val in enumerate(accuracies):
    plt.text(i, val - 10, f"{val:.2f}%", ha='center', color='white', fontweight='bold')
plt.ylim(0, 110)
plt.tight_layout()
plt.savefig('comparison.png', dpi=300)
print("Saved comparison plot to comparison.png")


# =====================================================================
# 1. EVALUATION TOOLKIT (ROC CURVE & CONFUSION MATRIX)
# =====================================================================
print("\nGenerating Evaluation Toolkit (ROC & Confusion Matrix)...")
from sklearn.metrics import roc_curve, auc, confusion_matrix

# Get prediction probabilities
ml_probs = ml_model.predict_proba(X_test_scaled)[:, 1]
if USE_TF:
    dl_probs = dl_model.predict(X_test_scaled).ravel()
    dl_preds = (dl_probs >= 0.5).astype(int)
else:
    dl_probs = dl_model.predict_proba(X_test_scaled)[:, 1]
    dl_preds = dl_model.predict(X_test_scaled)

# Compute ROC Metrics
fpr_ml, tpr_ml, _ = roc_curve(y_test, ml_probs)
roc_auc_ml = auc(fpr_ml, tpr_ml)

fpr_dl, tpr_dl, _ = roc_curve(y_test, dl_probs)
roc_auc_dl = auc(fpr_dl, tpr_dl)

# Confusion Matrix for DL
cm = confusion_matrix(y_test, dl_preds)

# Subplots side-by-side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left plot: ROC Curve Comparison
ax1.plot(fpr_ml, tpr_ml, color='darkorange', lw=2, label=f'Random Forest (AUC = {roc_auc_ml:.4f})')
ax1.plot(fpr_dl, tpr_dl, color='blue', lw=2, label=f'Neural Network (AUC = {roc_auc_dl:.4f})')
ax1.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
ax1.set_xlim([0.0, 1.0])
ax1.set_ylim([0.0, 1.05])
ax1.set_xlabel('False Positive Rate')
ax1.set_ylabel('True Positive Rate')
ax1.set_title('Receiver Operating Characteristic (ROC) Comparison')
ax1.legend(loc="lower right")

# Right plot: Confusion Matrix for DL
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax2,
            xticklabels=['Benign', 'Malignant'],
            yticklabels=['Benign', 'Malignant'])
ax2.set_xlabel('Predicted Label')
ax2.set_ylabel('True Label')
ax2.set_title('Confusion Matrix: Deep Learning Model')

plt.tight_layout()
plt.savefig('evaluation_toolkit.png', dpi=300)
print("Saved evaluation toolkit plot to evaluation_toolkit.png")


# =====================================================================
# 2. EXPLAINABLE AI (FEATURE IMPORTANCE)
# =====================================================================
print("\nGenerating Feature Importance Plot...")

importances = ml_model.feature_importances_
indices = np.argsort(importances)
features = X.columns[indices]
sorted_importances = importances[indices]

plt.figure(figsize=(8, 5))
plt.barh(features, sorted_importances, color='teal')
plt.xlabel('Relative Importance')
plt.title('Clinical Feature Importance (Random Forest Baseline)')
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300)
print("Saved feature importance plot to feature_importance.png")

# Save the trained models and scaler for use in the app
import pickle
print("\nSaving trained models and scaler to disk...")
with open('ml_model.pkl', 'wb') as f:
    pickle.dump(ml_model, f)
with open('dl_model.pkl', 'wb') as f:
    pickle.dump(dl_model, f)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
with open('use_tf.pkl', 'wb') as f:
    pickle.dump(USE_TF, f)
with open('feature_names.pkl', 'wb') as f:
    pickle.dump(list(X.columns), f)
print("Saved ml_model.pkl, dl_model.pkl, scaler.pkl, use_tf.pkl, feature_names.pkl successfully!")



# =====================================================================
# 3. POLISHED, MEDICAL-GRADE WEB FRONTEND (Gradio App)
# =====================================================================
print("\nSetting up Gradio Medical Portal...")
try:
    import gradio as gr
    
    def predict_cancer(clump_thickness, cell_size_uniformity, cell_shape_uniformity,
                       marginal_adhesion, epithelial_size, bare_nuclei,
                       bland_chromatin, normal_nucleoli, mitoses):
        # Combine inputs into DataFrame matching features
        input_df = pd.DataFrame([[
            clump_thickness, cell_size_uniformity, cell_shape_uniformity,
            marginal_adhesion, epithelial_size, bare_nuclei,
            bland_chromatin, normal_nucleoli, mitoses
        ]], columns=X.columns)
        
        # Scale input
        input_scaled = scaler.transform(input_df)
        
        # ML prediction
        ml_pred = ml_model.predict(input_scaled)[0]
        
        # DL prediction & probability
        if USE_TF:
            dl_prob = dl_model.predict(input_scaled)[0][0]
            dl_pred = int(dl_prob >= 0.5)
            dl_prob_pct = dl_prob * 100
        else:
            dl_prob = dl_model.predict_proba(input_scaled)[0][1]
            dl_pred = dl_model.predict(input_scaled)[0]
            dl_prob_pct = dl_prob * 100

        # Format predictions
        if ml_pred == 1:
            ml_result = "🚨 MALIGNANT (High Risk - Immediate Attention Required)"
        else:
            ml_result = "🟢 BENIGN (Low Risk - Safe)"
            
        if dl_pred == 1:
            dl_result = f"🚨 MALIGNANT (High Risk - Immediate Attention Required)\n[Malignancy Probability: {dl_prob_pct:.2f}%]"
        else:
            dl_result = f"🟢 BENIGN (Low Risk - Safe)\n[Malignancy Probability: {dl_prob_pct:.2f}%]"
            
        return ml_result, dl_result

    # Create custom theme and interface layout
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🩺 AI-Driven Breast Cancer Diagnostic Portal")
        gr.Markdown("Clinical decision-support tool utilizing parallel Machine Learning and Deep Neural Networks. Input cellular biopsy parameters below to generate diagnostic predictions.")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Cellular Biopsy Parameters")
                clump_thickness = gr.Slider(1, 10, step=1, value=5, label="Clump Thickness")
                cell_size_uniformity = gr.Slider(1, 10, step=1, value=5, label="Uniformity of Cell Size")
                cell_shape_uniformity = gr.Slider(1, 10, step=1, value=5, label="Uniformity of Cell Shape")
                marginal_adhesion = gr.Slider(1, 10, step=1, value=5, label="Marginal Adhesion")
                epithelial_size = gr.Slider(1, 10, step=1, value=5, label="Single Epithelial Cell Size")
                bare_nuclei = gr.Slider(1, 10, step=1, value=5, label="Bare Nuclei")
                bland_chromatin = gr.Slider(1, 10, step=1, value=5, label="Bland Chromatin")
                normal_nucleoli = gr.Slider(1, 10, step=1, value=5, label="Normal Nucleoli")
                mitoses = gr.Slider(1, 10, step=1, value=5, label="Mitoses")
                
                run_btn = gr.Button("Run Diagnostic Assessment", variant="primary")
                
            with gr.Column(scale=1):
                gr.Markdown("### Diagnostic Predictions")
                ml_output = gr.Textbox(
                    label="🌲 Traditional ML Baseline (Random Forest Result)",
                    interactive=False
                )
                dl_output = gr.Textbox(
                    label="🧠 Deep Learning Predictive Insight (ANN Result)",
                    interactive=False
                )
                
        run_btn.click(
            fn=predict_cancer,
            inputs=[
                clump_thickness, cell_size_uniformity, cell_shape_uniformity,
                marginal_adhesion, epithelial_size, bare_nuclei,
                bland_chromatin, normal_nucleoli, mitoses
            ],
            outputs=[ml_output, dl_output]
        )

    # Launch block checks if we are running in an interactive terminal to prevent lock
    import sys
    if sys.stdout.isatty():
        print("Launching Gradio interface...")
        demo.launch(share=False)
    else:
        print("Gradio portal defined successfully (skipped launch in non-interactive environment).")
except ImportError:
    print("Gradio library not found. Please install via 'pip install gradio' to launch the web portal.")
