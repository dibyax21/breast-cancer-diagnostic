from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Initialize presentation
prs = Presentation()

# Set to widescreen 16:9 format
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Design Colors
NAVY = RGBColor(10, 37, 64)
TEAL = RGBColor(0, 150, 136)
LIGHT_GREY = RGBColor(245, 247, 250)
CHARCOAL = RGBColor(45, 55, 72)
WHITE = RGBColor(255, 255, 255)
CARD_BG = RGBColor(235, 240, 245)

# Helper to configure slide background
def set_solid_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

# Helper to add standard slide accent bar
def add_teal_bar(slide):
    shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    shape.fill.solid()
    shape.fill.fore_color.rgb = TEAL
    shape.line.fill.background()

# Helper to add titles
def add_slide_title(slide, text):
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.8))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.bold = True
    p.font.size = Pt(36)
    p.font.color.rgb = NAVY
    p.font.name = "Arial"
    return tx_box

# Helper to add left-aligned bullet lists (leaves right side open for graphics)
def add_slide_bullets(slide, items, left=Inches(0.8), width=Inches(5.5)):
    tx_box = slide.shapes.add_textbox(left, Inches(1.5), width, Inches(5.0))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(17)
        p.font.color.rgb = CHARCOAL
        p.font.name = "Arial"
        p.level = 0
        p.space_after = Pt(12)
    return tx_box

# Helper to add an image container/card on the right side
def add_image_card(slide, image_path, left, top, width, height, card_title):
    # Add a soft background card behind the image
    card = slide.shapes.add_shape(
        1, 
        left - Inches(0.2), 
        top - Inches(0.5), 
        width + Inches(0.4), 
        height + Inches(0.8)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = TEAL
    
    # Add card title
    title_box = slide.shapes.add_textbox(left - Inches(0.2), top - Inches(0.45), width + Inches(0.4), Inches(0.4))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = card_title
    p.alignment = PP_ALIGN.CENTER
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = NAVY
    p.font.name = "Arial"
    
    # Add the actual image
    slide.shapes.add_picture(image_path, left, top, width, height)

# Helper to add structured footer
def add_footer(slide, current, total=10):
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.4))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"Breast Cancer AI Diagnosis Portal  |  Slide {current} of {total}"
    p.font.size = Pt(10)
    p.font.color.rgb = TEAL
    p.font.name = "Arial"

# ==========================================
# SLIDE 1: Title Slide (Dark Theme)
# ==========================================
slide_layout = prs.slide_layouts[6] # Blank layout
slide1 = prs.slides.add_slide(slide_layout)
set_solid_background(slide1, NAVY)

title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.33), Inches(3.0))
tf = title_box.text_frame
tf.word_wrap = True

# Main Title
p = tf.paragraphs[0]
p.text = "AI-Driven Breast Cancer Diagnostic Portal"
p.font.bold = True
p.font.size = Pt(46)
p.font.color.rgb = WHITE
p.font.name = "Arial"

# Subtitle
p2 = tf.add_paragraph()
p2.text = "Parallel Machine Learning & Deep Learning Decision Support"
p2.font.size = Pt(20)
p2.font.color.rgb = TEAL
p2.font.name = "Arial"
p2.space_before = Pt(14)

# Presenter metadata
p3 = tf.add_paragraph()
p3.text = "Clinical Classification System  |  Powered by Random Forest & Neural Networks"
p3.font.size = Pt(12)
p3.font.color.rgb = WHITE
p3.font.name = "Arial"
p3.space_before = Pt(40)


# ==========================================
# SLIDE 2: Clinical Context & Problem
# ==========================================
slide2 = prs.slides.add_slide(slide_layout)
set_solid_background(slide2, LIGHT_GREY)
add_teal_bar(slide2)
add_slide_title(slide2, "Clinical Context & Diagnostic Challenge")
add_slide_bullets(slide2, [
    "• Breast cancer remains a primary driver of global oncology mortality; rapid and highly accurate diagnosis is vital.",
    "• Cytological Analysis: Fine needle aspiration (FNA) biopsied cells are evaluated based on structural characteristics.",
    "• System Objective: Build an automated decision-support system to classify patient cell samples as Benign or Malignant.",
    "• Redundancy Strategy: Leverage parallel baseline Machine Learning and Deep Learning architectures to provide safety checks, preventing false negative diagnoses.",
    "• Key Challenge: Deal with real-world clinical dataset anomalies (e.g., missing data points) while maintaining predictive integrity."
], width=Inches(11.7))
add_footer(slide2, 2)


# ==========================================
# SLIDE 3: System Pipeline & Data Flow
# ==========================================
slide3 = prs.slides.add_slide(slide_layout)
set_solid_background(slide3, LIGHT_GREY)
add_teal_bar(slide3)
add_slide_title(slide3, "System Pipeline & Data Flow Architecture")
add_slide_bullets(slide3, [
    "• Source Dataset: Features from the breast-cancer-wisconsin clinical repository.",
    "• Feature Vector: 9 input variables representing cellular properties (e.g., clump thickness, bare nuclei, mitosis rate).",
    "• Data Cleaning: Safely detected missing indices marked by '?' in raw clinical files and resolved them via dropping rows.",
    "• Scaling Phase: Passed features through StandardScaler to achieve zero-mean and unit-variance configuration.",
    "• Training Partition: Applied stratified split to allocate 80% train and 20% test data to preserve categorical representation."
], width=Inches(11.7))
add_footer(slide3, 3)


# ==========================================
# SLIDE 4: Parallel Dual-Model Framework
# ==========================================
slide4 = prs.slides.add_slide(slide_layout)
set_solid_background(slide4, LIGHT_GREY)
add_teal_bar(slide4)
add_slide_title(slide4, "Parallel Dual-Model Inference Pipeline")
add_slide_bullets(slide4, [
    "• Diagnostic Redundancy: Two independent models process the scaled clinical features in parallel.",
    "• Baseline Model: Random Forest Classifier provides structural interpretation and feature importance tracking.",
    "• Neural Network Model: Artificial Neural Network (ANN) computes deep mathematical mappings for probabilistic risk assessment.",
    "• Validation Strategy: Models are trained concurrently on the same stratified splits, and metrics are cross-compared.",
    "• Safety Catchment: Conflicting predictions alert clinical users to request manual sample re-evaluations."
], width=Inches(11.7))
add_footer(slide4, 4)


# ==========================================
# SLIDE 5: Machine Learning Baseline (Random Forest)
# ==========================================
slide5 = prs.slides.add_slide(slide_layout)
set_solid_background(slide5, LIGHT_GREY)
add_teal_bar(slide5)
add_slide_title(slide5, "Traditional ML Baseline: Random Forest")
add_slide_bullets(slide5, [
    "• Architecture: Ensemble classifier comprising 100 individual decision tree estimators.",
    "• Out-of-Sample Performance: Achieved a robust baseline accuracy of 95.62% on the validation test split.",
    "• Key Strength: Exceptionally resilient to outlier data points and completely avoids overfitting via random feature selection.",
    "• Parameter Configuration: Leveraged stratified classes, utilizing entropy-based gini splitting algorithms.",
    "• Explainability: Directly produces internal feature importance coefficients, highlighting diagnostic drivers."
], width=Inches(11.7))
add_footer(slide5, 5)


# ==========================================
# SLIDE 6: Performance Comparison (With Graphics)
# ==========================================
slide6 = prs.slides.add_slide(slide_layout)
set_solid_background(slide6, LIGHT_GREY)
add_teal_bar(slide6)
add_slide_title(slide6, "Model Performance Comparison")

# Left Column: Text description
add_slide_bullets(slide6, [
    "• Baseline Accuracy: The Random Forest ML model achieves a high score of 95.62%.",
    "• Neural Network (DL): The artificial neural network topology achieves a higher accuracy of 96.35%.",
    "• Model Synergy: Combining the ensemble trees with backpropagation neural layers increases diagnostic confidence.",
    "• Implementation safety: The DL framework falls back to scikit-learn MLP if local TensorFlow packages fail to initialize."
], left=Inches(0.8), width=Inches(5.5))

# Right Column: comparison.png
add_image_card(
    slide6, 
    'comparison.png', 
    left=Inches(7.1), 
    top=Inches(1.8), 
    width=Inches(5.4), 
    height=Inches(3.8), 
    card_title="ACCURACY COMPARISON (ML VS. DL)"
)
add_footer(slide6, 6)


# ==========================================
# SLIDE 7: Evaluation Toolkit (With Graphics)
# ==========================================
slide7 = prs.slides.add_slide(slide_layout)
set_solid_background(slide7, LIGHT_GREY)
add_teal_bar(slide7)
add_slide_title(slide7, "Comparative Performance Evaluation")

# Left Column: Text description
add_slide_bullets(slide7, [
    "• Area Under the Curve (AUC): Random Forest AUC is 0.9926 and Neural Network AUC is 0.9859.",
    "• Sensitivity Analysis: Deep Learning model showed zero False Negatives on the test dataset (critical for diagnostic safety).",
    "• Specificity Metrics: Highly configured decision boundary reduces False Positives, avoiding unnecessary patient stress.",
    "• Verdict: The parallel approach successfully balances high-recall sensitivity with high-precision specificity."
], left=Inches(0.8), width=Inches(5.0))

# Right Column: evaluation_toolkit.png (ROC & Confusion Matrix)
add_image_card(
    slide7, 
    'evaluation_toolkit.png', 
    left=Inches(6.4), 
    top=Inches(2.1), 
    width=Inches(6.2), 
    height=Inches(3.2), 
    card_title="ROC CURVE COMPARISON & CONFUSION MATRIX"
)
add_footer(slide7, 7)


# ==========================================
# SLIDE 8: Explainable AI (With Graphics)
# ==========================================
slide8 = prs.slides.add_slide(slide_layout)
set_solid_background(slide8, LIGHT_GREY)
add_teal_bar(slide8)
add_slide_title(slide8, "Explainable AI: Clinical Feature Importance")

# Left Column: Text description
add_slide_bullets(slide8, [
    "• Method: Extracted feature importances from the Random Forest baseline to clarify the black-box models.",
    "• Primary Malignancy Indicators: Uniformity of Cell Size and Uniformity of Cell Shape are the top contributors.",
    "• Secondary Clinical Markers: Bare Nuclei and Bland Chromatin show moderate significance.",
    "• Clinical Impact: Empowers oncologists to cross-reference model diagnostic decisions with physical cell morphology metrics."
], left=Inches(0.8), width=Inches(5.5))

# Right Column: feature_importance.png
add_image_card(
    slide8, 
    'feature_importance.png', 
    left=Inches(7.1), 
    top=Inches(1.8), 
    width=Inches(5.4), 
    height=Inches(3.8), 
    card_title="RANDOM FOREST BASELINE FEATURE IMPORTANCE"
)
add_footer(slide8, 8)


# ==========================================
# SLIDE 9: Interactive Diagnostic Web Portal
# ==========================================
slide9 = prs.slides.add_slide(slide_layout)
set_solid_background(slide9, LIGHT_GREY)
add_teal_bar(slide9)
add_slide_title(slide9, "Interactive Medical-Grade Web Portal")
add_slide_bullets(slide9, [
    "• Web Framework: Standalone application built using the Gradio library (app.py).",
    "• Interface Theme: Uses a clean, professional Soft dashboard layout suited for medical applications.",
    "• User Inputs: 9 biopsy attribute sliders ranging from 1 to 10 for easy clinical testing.",
    "• Output System: Displays parallel diagnostic responses side-by-side (ML result vs. DL predictive insight).",
    "• Probability output: Neural network output prints calculated malignancy percentage probability (e.g. 98.42%)."
], width=Inches(11.7))
add_footer(slide9, 9)


# ==========================================
# SLIDE 10: Conclusion & Next Steps
# ==========================================
slide10 = prs.slides.add_slide(slide_layout)
set_solid_background(slide10, LIGHT_GREY)
add_teal_bar(slide10)
add_slide_title(slide10, "Summary & Future Outlook")
add_slide_bullets(slide10, [
    "• Main Achievement: Developed a robust, parallel classification system achieving >95.5% accuracy.",
    "• Diagnostic Safety: Multi-model system provides safety checks to minimize misdiagnoses.",
    "• System Portability: Implemented model pickle serialization and a lightweight Gradio server.",
    "• Clinical Scaling: Planned integrations include testing on larger, multi-center hospital biopsy databases.",
    "• Deployment Vision: Wrap model endpoints into REST APIs to integrate directly with hospital EHR databases."
], width=Inches(11.7))
add_footer(slide10, 10)

# Save presentation
prs.save("breast_cancer_diagnostic_presentation_v2.pptx")
print("Presentation generated successfully with embedded graphics!")

