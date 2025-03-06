import os
import argparse
import re
import joblib
import pandas as pd
from datetime import datetime

# Load artifacts
preprocessor = joblib.load('preprocessor.pkl')
model = joblib.load('svm.pkl')  

def get_file_metadata(file_path):
    """Extract OS-level metadata"""
    stat = os.stat(file_path)
    
    return {
        'filename': os.path.basename(file_path),
        'extension': os.path.splitext(file_path)[1].lower().strip('.'),
        'size': stat.st_size,
        'created': datetime.fromtimestamp(stat.st_ctime),
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'read_only': not os.access(file_path, os.W_OK),
        'executable': os.access(file_path, os.X_OK)
    }

def process_features(metadata):
    """Replicate training feature engineering"""
    # Secret keyword detection
    # secret_pattern = r'(?i)(?:^|[_-])(confidential|secret|private|aadhar|aadhaar|pan|salary|bank|account|ifsc|password|pin|credit|debit|ssn|passport|financial|income|tax|loan|transaction|insurance|agreement|contract|classified|office|official|employee|hr|budget|audit|payroll|statement|balance|investment)'
    secret_pattern = r'(?i)(?:^|[_-])(confidential|secret|private|certificate|aadhar|aadhaar|pan|salary|bank|account|ifsc|password|pin|credit|debit|ssn|passport|financial|income|tax|loan|transaction|insurance|agreement|contract|classified|office|official|employee|hr|budget|audit|payroll|statement|balance|investment)(?:[_-]|$)'
    metadata['has_secret_keyword'] = int(bool(re.search(secret_pattern, metadata['filename'])))
    
    # Size categorization
    size_bins = [0, 1024, 10240, 102400, 1048576]
    size_labels = ['tiny', 'small', 'medium', 'large']
    metadata['size_category'] = pd.cut([metadata['size']], bins=size_bins, labels=size_labels)[0]
    
    # Temporal features
    now = datetime.now()
    metadata['age_days'] = (now - metadata['created']).days
    metadata['modified_recency'] = (now - metadata['modified']).days
    
    return pd.DataFrame([metadata])

def main():
    parser = argparse.ArgumentParser(description='Classify file sensitivity')
    parser.add_argument('--file', type=str, required=True, help='Path to file for classification')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found - {args.file}")
        return

    # Extract metadata
    metadata = get_file_metadata(args.file)
    
    # Process features
    df = process_features(metadata)
    
    # Transform and predict
    X = preprocessor.transform(df)
    proba = model.predict_proba(X)[0][1]
    prediction = model.predict(X)[0]
    
    # Console output
    print("\nClassification Results:")
    print(f"File: {args.file}")
    print(f"Prediction: {'SENSITIVE (🔴)' if prediction else 'INSENSITIVE (🟢)'}")
    print(f"Confidence: {proba:.1%}")
    print("\nMetadata Analysis:")
    for k,v in metadata.items():
        print(f"{k.upper():<20}: {v}")

if __name__ == "__main__":
    main()