
# 🔒 8bitSquad: Sensitive Document Classification System
### Classify document sensitivity using metadata only – No content scanning!
### Preserve privacy while automating compliance with AI-powered metadata analysis.

## 🚀 Features

✅ Hybrid Dataset Generation – Combine real documents + AI-generated synthetic data

✅ Privacy-First Approach – No content scanning; only metadata is analyzed

✅ High Accuracy – Achieves 89.39% precision using SVM and Logistic Regression models

✅ Easy-to-Use CLI – Classify documents via a simple command-line interface

✅ Smart Preprocessing – Automated feature engineering pipeline for better predictions

---

## 📦 Installation

# Clone the repository
```bash
git clone https://github.com/yourusername/8bitSquad_SensitiveDocumentClassification.git
cd 8bitSquad_SensitiveDocumentClassification
```

# Install dependencies
```bash
pip install -r requirements.txt
```


## 🛠️ Usage Guide
### 1️⃣ Dataset Generation
```bash
cd datasetgenerator
```


## 📂 Folder Structure:
```bash
├── originaldocs/
│   ├── sensitive/      # Add sensitive documents here
│   └── nonsensitive/   # Add non-sensitive documents here
```
🔹 Generate Dataset:
```bash
python generator.py
```
📌 Output: enhanced_hybrid_dataset.csv (Combines real + synthetic data)



### 2️⃣ Model Training
📜 Open SensitiveDocumentClassification.ipynb in Jupyter Notebook.

🔹 Run all cells to:

Train SVM and Logistic Regression models
Generate preprocessor.pkl and svm.pkl
Save model artifacts in the models/ directory


### 3️⃣ CLI Classification
```bash
cd "CLI interface"
```
🔹 Classify a single file:

```bash
python classifier.py --file "path/to/your/document.pdf"
```

### 📌 Sample Output:

┌───────────────────────────────┬────────────┬───────────────────────┬─────────────────┐
│ File Name                     │ File Type  │ Prediction            │ Confidence      │
├───────────────────────────────┼────────────┼───────────────────────┼─────────────────┤
│ aadharcard.pdf                │ PDF        │ Sensitive (Y)         │  92%            │
└───────────────────────────────┴────────────┴───────────────────────┴─────────────────┘
---

## 📂 Project Structure
```bash
8bitSquad_SensitiveDocumentClassification/
├── CLI_interface/
│   ├── classifier.py         # Classification script
│   ├── preprocessor.pkl      # Feature engineering pipeline
│   └── svm.pkl               # Trained model
│
├── datasetgenerator/
│   ├── generator.py          # Dataset creation script
│   ├── originaldocs/         # User-provided documents
│   │   ├── sensitive/        # Labeled sensitive files
│   │   └── nonsensitive/     # Labeled non-sensitive files
│   └── enhanced_hybrid_dataset.csv  # Generated dataset
│
├── SensitiveDocumentClassification.ipynb  # Model training notebook
└── requirements.txt           # Dependency list
```
