import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
import warnings

# Suppress Faker warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

fake = Faker()

def process_real_documents():
    """Process documents from sensitive/nonsensitive folders with auto-labeling"""
    base_dir = os.path.join(os.getcwd(), 'originaldocs')
    real_data = []
    
    if os.path.exists(base_dir):
        print("\nProcessing original documents...")
        
        # Process sensitive documents
        sensitive_dir = os.path.join(base_dir, 'sensitive')
        if os.path.exists(sensitive_dir):
            for filename in os.listdir(sensitive_dir):
                filepath = os.path.join(sensitive_dir, filename)
                if os.path.isfile(filepath):
                    try:
                        real_data.append(process_single_file(filepath, sensitive=1))
                    except Exception as e:
                        print(f"Error processing {filename}: {str(e)}")

        # Process non-sensitive documents
        nonsensitive_dir = os.path.join(base_dir, 'nonsensitive')
        if os.path.exists(nonsensitive_dir):
            for filename in os.listdir(nonsensitive_dir):
                filepath = os.path.join(nonsensitive_dir, filename)
                if os.path.isfile(filepath):
                    try:
                        real_data.append(process_single_file(filepath, sensitive=0))
                    except Exception as e:
                        print(f"Error processing {filename}: {str(e)}")

    return pd.DataFrame(real_data)

def process_single_file(filepath, sensitive):
    """Extract metadata from a single file"""
    stat = os.stat(filepath)
    return {
        'filename': os.path.basename(filepath),
        'extension': os.path.splitext(filepath)[1][1:].lower(),
        'size': stat.st_size,
        'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'sensitive': sensitive,
        'read_only': int(not os.access(filepath, os.W_OK))
    }

def analyze_real_data_patterns(real_df):
    """Analyze real data to guide synthetic generation"""
    patterns = {
        'sensitive': {'count': 0, 'size': [], 'extensions': [], 'dates': []},
        'nonsensitive': {'count': 0, 'size': [], 'extensions': [], 'dates': []}
    }
    
    if not real_df.empty:
        for _, row in real_df.iterrows():
            key = 'sensitive' if row['sensitive'] else 'nonsensitive'
            patterns[key]['count'] += 1
            patterns[key]['size'].append(row['size'])
            patterns[key]['extensions'].append(row['extension'])
            patterns[key]['dates'].append(datetime.strptime(row['created'], '%Y-%m-%d %H:%M:%S'))
    
    # Calculate statistics
    stats = {}
    for key in ['sensitive', 'nonsensitive']:
        stats[key] = {
            'size_mean': np.mean(patterns[key]['size']) if patterns[key]['size'] else 500000,
            'size_std': np.std(patterns[key]['size']) if patterns[key]['size'] else 200000,
            'common_ext': pd.Series(patterns[key]['extensions']).mode()[0] if patterns[key]['extensions'] else 'pdf',
            'date_range': (
                min(patterns[key]['dates']) if patterns[key]['dates'] else datetime(2018, 1, 1),
                max(patterns[key]['dates']) if patterns[key]['dates'] else datetime.now()
            )
        }
    
    return stats

def generate_realistic_filename(is_sensitive, real_stats):
    """Generate filename matching real patterns"""
    sensitive_keywords = ['aadhaar', 'pan', 'voter', 'passport', 'confidential','resume']
    non_sensitive_keywords = ['report', 'notes', 'documents', 'memo']
    
    if is_sensitive:
        base = random.choice(sensitive_keywords)
        variants = [
            f"{base}_{fake.random_number(digits=4)}.pdf",
            f"scan_{base}.pdf",
            f"{base}_card_{fake.last_name().lower()}.pdf",
            f"{base}_document_{datetime.now().year}.pdf"
        ]
    else:
        base = random.choice(non_sensitive_keywords)
        variants = [
            f"{base}_{fake.month_name().lower()}.pdf",
            f"{fake.file_name()}",
            f"{base}_draft_{fake.random_number(digits=2)}.pdf"
        ]
    
    return random.choice(variants)

def generate_synthetic_data(num_samples, real_stats):
    """Generate synthetic data matching real patterns"""
    synthetic_data = []
    
    for _ in range(num_samples):
        is_sensitive = random.choices([True, False], weights=[0.4, 0.6])[0]
        key = 'sensitive' if is_sensitive else 'nonsensitive'
        
        # Generate metadata based on real patterns
        filename = generate_realistic_filename(is_sensitive, real_stats)
        ext = real_stats[key]['common_ext']
        size = max(1000, int(np.random.normal(
            real_stats[key]['size_mean'], 
            real_stats[key]['size_std']
        )))
        
        # Generate realistic dates
        start_date = real_stats[key]['date_range'][0]
        end_date = real_stats[key]['date_range'][1]
        created_date = fake.date_time_between(
            start_date=start_date, 
            end_date=end_date
        )
        modified_date = created_date + timedelta(days=random.randint(0, 30))
        
        synthetic_data.append({
            'filename': filename,
            'extension': ext,
            'size': size,
            'created': created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'modified': modified_date.strftime('%Y-%m-%d %H:%M:%S'),
            'sensitive': int(is_sensitive),
            'read_only': random.choices([0, 1], weights=[0.7, 0.3])[0]
        })
    
    return pd.DataFrame(synthetic_data)

def main():
    total_samples = 1000  # Total desired dataset size
    
    # Process real documents
    real_df = process_real_documents()
    real_count = len(real_df)
    
    # Analyze real data patterns
    real_stats = analyze_real_data_patterns(real_df)
    
    # Generate synthetic data matching real patterns
    synthetic_count = max(total_samples - real_count, 0)
    synthetic_df = generate_synthetic_data(synthetic_count, real_stats)
    
    # Combine datasets
    combined_df = pd.concat([real_df, synthetic_df], ignore_index=True)
    
    # Save to CSV
    combined_df.to_csv('enhanced_hybrid_dataset.csv', index=False)
    print(f"\nDataset created with {real_count} real and {synthetic_count} synthetic entries")
    print(f"Sensitive file patterns: {real_stats['sensitive']}")
    print(f"Non-sensitive file patterns: {real_stats['nonsensitive']}")
    print("Saved as 'enhanced_hybrid_dataset.csv'")

if __name__ == "__main__":
    main()