# 🔬 DermaAI — Skin Disease Classification System

A professional, multi-model ensemble skin disease classifier with real-time
image validation, camera capture, and an elegant dark-theme UI.

---

## 📁 Project Structure

```
skin_ai/
├── app.py              ← Main Streamlit application (entry point)
├── model_loader.py     ← Loads all .h5 and .joblib models
├── preprocessor.py     ← Image validation + preprocessing pipeline
├── predictor.py        ← Ensemble prediction engine
├── disease_info.py     ← Disease descriptions and precautions
├── ui_components.py    ← Custom CSS and all UI rendering functions
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
└── models/             ← Place ALL model files here
    ├── BEST_MODEL_SVM.joblib    ← Primary (highest weight: 35%)
    ├── SVM.joblib               ← Secondary SVM (15%)
    ├── RandomForest.joblib      ← RF classifier (10%)
    ├── feature_scaler.joblib    ← Sklearn scaler for SVM/RF
    ├── MobileNetV2_best.h5      ← Best MobileNetV2 (20%)
    ├── MobileNetV2_final.h5     ← Final MobileNetV2 (8%)
    ├── MobileNetV2_Phase1.h5    ← Phase-1 MobileNetV2 (5%)
    ├── AlexNet_best.h5          ← AlexNet (4%)
    └── LeNet_best.h5            ← LeNet (3%)
```

---

## 🚀 Setup & Run

### 1. Clone / copy project files
```bash
mkdir skin_ai && cd skin_ai
# Place all .py files here
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Place your model files
```bash
mkdir models
# Copy all .h5 and .joblib files into the models/ directory
```

### 5. Run the application
```bash
streamlit run app.py
```

The app opens automatically at: **http://localhost:8501**

---

## 🧠 Ensemble Architecture

| Model              | Type       | Weight | Input Size |
|--------------------|------------|--------|------------|
| BEST_MODEL_SVM     | SVM        | 35%    | 64×64 flat |
| SVM                | SVM        | 15%    | 64×64 flat |
| MobileNetV2_best   | CNN (Keras)| 20%    | 224×224    |
| RandomForest       | RF         | 10%    | 64×64 flat |
| MobileNetV2_final  | CNN (Keras)| 8%     | 224×224    |
| MobileNetV2_Phase1 | CNN (Keras)| 5%     | 224×224    |
| AlexNet_best       | CNN (Keras)| 4%     | 227×227    |
| LeNet_best         | CNN (Keras)| 3%     | 32×32 gray |

Missing models are gracefully skipped — weights are renormalized automatically.

---

## ✅ Image Validation Checks

| Check       | Condition                    |
|-------------|------------------------------|
| Brightness  | Mean pixel value 50–230      |
| Focus       | Laplacian variance > 80      |
| Skin region | HSV skin mask coverage > 5%  |
| Resolution  | Minimum 64×64 pixels         |

Border turns **🟢 GREEN** when all checks pass, **🔴 RED** otherwise.

---

## 🏥 Detectable Conditions (13 classes)

- Acne
- Acne Scars  
- Contact Dermatitis
- Eczema / Atopic Dermatitis
- Folliculitis
- Fungal Infection
- Hyperpigmentation
- Normal Skin
- Pseudofolliculitis Barbae
- Rosacea
- Seborrheic Dermatitis
- Sunburn
- Vitiligo

---

## ⚠️ Disclaimer

This application is for **educational and research purposes only**.  
It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.  
Always consult a licensed dermatologist for skin concerns.

---

## 🛠️ Troubleshooting

| Issue                         | Solution                                          |
|-------------------------------|---------------------------------------------------|
| TF/Keras model fails to load  | Check TF version matches .h5 save version         |
| SVM feature size mismatch     | App auto-tries HOG features as fallback           |
| Camera not working            | Use "Upload Image" tab; check browser permissions |
| ModuleNotFoundError           | Re-run `pip install -r requirements.txt`          |
| Too slow on CPU               | CNN models are heavy; SVM-only mode still works   |
