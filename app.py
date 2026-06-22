import pickle
import numpy as np
import pandas as pd
import gradio as gr

# 1. Load the trained models, scaler, and metadata
try:
    with open('ml_model.pkl', 'rb') as f:
        ml_model = pickle.load(f)
    with open('dl_model.pkl', 'rb') as f:
        dl_model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('use_tf.pkl', 'rb') as f:
        USE_TF = pickle.load(f)
    with open('feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    print("Models and scaler loaded successfully!")
except FileNotFoundError as e:
    print(f"Error: Required model/scaler files not found. Please run 'train_models.py' first. Details: {e}")
    exit(1)

# 2. Prediction function
def predict_cancer(clump_thickness, cell_size_uniformity, cell_shape_uniformity,
                   marginal_adhesion, epithelial_size, bare_nuclei,
                   bland_chromatin, normal_nucleoli, mitoses):
    # Combine inputs into DataFrame matching features exactly
    input_df = pd.DataFrame([[
        clump_thickness, cell_size_uniformity, cell_shape_uniformity,
        marginal_adhesion, epithelial_size, bare_nuclei,
        bland_chromatin, normal_nucleoli, mitoses
    ]], columns=feature_names)
    
    # Scale input
    input_scaled = scaler.transform(input_df)
    
    # ML model prediction
    ml_pred = ml_model.predict(input_scaled)[0]
    
    # DL model prediction & probability
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

# 3. Create blocks layout
with gr.Blocks() as demo:
    gr.Markdown("# 🩺 AI-Driven Breast Cancer Diagnostic Portal")
    gr.Markdown("Clinical decision-support tool leveraging parallel Machine Learning and Deep Neural Networks. Input cellular biopsy parameters below to generate diagnostic predictions.")
    
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

if __name__ == "__main__":
    # Launch using Soft theme (Gradio 6.0 compatible style)
    demo.launch(theme=gr.themes.Soft())
