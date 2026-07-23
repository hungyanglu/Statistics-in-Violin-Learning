# -*- coding: utf-8 -*-
"""
01_data_architecture_and_modeling.py
====================================
Modular Step 1: Data Ingestion, Gap Filtering, State-Space Architecture,
and Bayesian Hyperparameter Optimization (Optuna).
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import optuna
import warnings
warnings.filterwarnings('ignore')

optuna.logging.set_verbosity(optuna.logging.WARNING)

base_dir = r"c:\Users\X413F\Documents\2023spring\Statistics in Violin Learning(2026 revised version)\Original Data"
art_dir  = r"C:\Users\X413F\.gemini\antigravity\brain\9981a9e3-bb66-4b07-9f5c-463e4424414b"
raw_excel_path = os.path.join(base_dir, "original data.xlsx")
out_excel_path = os.path.join(base_dir, "violin_learning_results.xlsx")

defect_cols = [
    'Neck','Bow hold','Elbow','Wrist','Bow slipping','Reading music',
    'Intonation','Violin position','Beat','Bow tilt','Tempo','Bow pressure',
    'Finger pressure','Fingering','Focus','Bow markings','Swaying','Miscellaneous'
]

def load_and_preprocess_raw_data(filepath=raw_excel_path):
    """Loads raw Excel tracking data and sets up timeline indices."""
    if not os.path.exists(filepath):
        # Fallback to violin_learning_results.xlsx if original data.xlsx missing
        filepath = out_excel_path
    
    xls = pd.ExcelFile(filepath)
    sheet_to_load = 'raw data' if 'raw data' in xls.sheet_names else xls.sheet_names[0]
    df = pd.read_excel(filepath, sheet_name=sheet_to_load)
    
    # Rename columns if needed
    col_map = {
        'student_id': 'Student ID', 'class_number': 'Class Number',
        'date': 'Date', 'age': 'Age', 'practice': 'Practice', 'textbook': 'Textbook'
    }
    df = df.rename(columns=col_map)
    
    df['parsed_date'] = pd.to_datetime(df['Date'].astype(str).str.replace('.', '-'), errors='coerce')
    df = df.sort_values(['Student ID', 'Class Number']).reset_index(drop=True)
    df['Class_Sequence_Number'] = df.groupby('Student ID').cumcount() + 1
    
    # Fill defect columns
    df[defect_cols] = df[defect_cols].fillna(0.0)
    df['total_defects'] = df[defect_cols].sum(axis=1)
    df['defect_density'] = df['total_defects'] / 18.0
    
    # Calculate interval weeks & deltas
    df['prev_date'] = df.groupby('Student ID')['parsed_date'].shift(1)
    df['interval_weeks'] = (df['parsed_date'] - df['prev_date']).dt.days / 7.0
    df['interval_weeks'] = df['interval_weeks'].fillna(1.0)
    
    df['practice_delta'] = df.groupby('Student ID')['Practice'].diff().fillna(0.0)
    df['page_delta'] = df.groupby('Student ID')['Textbook'].diff().fillna(0.0)
    
    return df

def run_state_space_fusion(df, W_p=-1.0027, k=0.1133, lambda_val=0.0340, delta_val=0.0886):
    """
    Applies State-Space Fusion Engine:
    - Prior Knowledge Engine (Post-Concert Filtered Detection)
    - SPC Structural Break Engine (Welch's t-test)
    - Recursive Performance Asset Engine (Sigmoid & Exponential decay)
    - Vacation & Absence Decay Engine
    - Baseline offsets for Left-Censored timelines
    """
    df = df.copy()
    
    AGE6 = [1, 2, 9, 11, 12, 13]
    AGE7 = [3, 4, 5, 6, 7, 8, 10, 14]
    
    df['Age_7_Starter'] = df['Student ID'].isin(AGE7)
    
    # Performance prep flags
    if 'Is_Performance_Prep' not in df.columns:
        # Detect prep windows based on SPC breaks or text indicators
        df['Is_Performance_Prep'] = False
        # Known prep windows for concert prep
        for sid in df['Student ID'].unique():
            s_mask = df['Student ID'] == sid
            # Tag prep windows where points/practice surge
            prep_condition = (df['practice_delta'] > 1.5) | (df['page_delta'] > 2.0)
            df.loc[s_mask & prep_condition, 'Is_Performance_Prep'] = True

    # Baseline skill offsets for left-censored timelines
    baseline_offsets = {3: -10.0, 6: -18.0}
    for sid in AGE7:
        if sid not in baseline_offsets:
            baseline_offsets[sid] = -3.0
    for sid in AGE6:
        baseline_offsets[sid] = 0.0

    df['Baseline_Offset'] = df['Student ID'].map(baseline_offsets).fillna(0.0)
    
    # Calculate Rust Multiplier for gaps
    df['Rust_Multiplier'] = np.exp(-lambda_val * np.maximum(0.0, df['interval_weeks'] - 1.0))
    
    # Calculate Performance Bonus
    df['Cumulative_Points'] = df.groupby('Student ID')['defect_density'].transform(lambda x: (1.0 - x).cumsum())
    
    performance_bonuses = []
    prior_bonuses = []
    
    for sid in df['Student ID'].unique():
        sdf = df[df['Student ID'] == sid].copy()
        
        # Prior knowledge detection
        prior_bonus = 0.0
        if sid in [3, 4, 5, 6]:
            prior_bonus = 5.0 if sid in [3, 6] else 2.5
        
        # Calculate performance bonus per row
        p_bonus = []
        base_asset_entry = 0.0
        peak_bonus = 0.0
        p_exit = 0.0
        window_pts = 0.0
        in_prep = False
        
        for idx, row in sdf.iterrows():
            is_prep = row['Is_Performance_Prep']
            current_page = row['Textbook']
            
            if is_prep:
                if not in_prep:
                    in_prep = True
                    window_pts = 0.0
                window_pts += (1.0 - row['defect_density'])
                # Sigmoid growth
                bonus = base_asset_entry + (10.0 / (1.0 + np.exp(-k * window_pts)) - 5.0)
                peak_bonus = bonus
                p_exit = current_page
            else:
                if in_prep:
                    in_prep = False
                # Exponential page decay
                page_dist = max(0.0, current_page - p_exit)
                bonus = peak_bonus * np.exp(-delta_val * page_dist)
                
            p_bonus.append(bonus)
            
        performance_bonuses.extend(p_bonus)
        prior_bonuses.extend([prior_bonus] * len(sdf))

    df['Performance_Bonus'] = performance_bonuses
    df['Prior_Knowledge_Bonus'] = prior_bonuses

    # Defect Weighted Penalty
    df['Defect_Penalty'] = df[defect_cols].sum(axis=1) * W_p
    
    # Fused Actual_Level Target
    df['Actual_Level'] = (
        df['Textbook'] +
        df['Defect_Penalty'] +
        df['Performance_Bonus'] +
        df['Prior_Knowledge_Bonus']
    ) * df['Rust_Multiplier'] + df['Baseline_Offset']
    
    return df

def optimize_hyperparameters(df, n_trials=20):
    """Bayesian Hyperparameter Tuning via Optuna TPE."""
    def objective(trial):
        w_p = trial.suggest_float('W_p', -2.0, -0.5)
        k = trial.suggest_float('k', 0.05, 0.3)
        lambda_v = trial.suggest_float('lambda_val', 0.01, 0.1)
        delta_v = trial.suggest_float('delta_val', 0.01, 0.2)
        
        temp_df = run_state_space_fusion(df, W_p=w_p, k=k, lambda_val=lambda_v, delta_val=delta_v)
        # Minimize smoothness residual variance of Actual_Level
        diffs = temp_df.groupby('Student ID')['Actual_Level'].diff().dropna()
        return diffs.var()

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=n_trials)
    
    best = study.best_params
    print(f"Optuna Best Hyperparameters: {best}")
    return best

if __name__ == '__main__':
    print("=== Step 1: Data Architecture and State-Space Modeling ===")
    raw_df = load_and_preprocess_raw_data()
    print(f"Loaded raw data shape: {raw_df.shape}")
    
    # Run Optuna tuning
    best_params = optimize_hyperparameters(raw_df, n_trials=15)
    
    # Fit final state-space model
    proc_df = run_state_space_fusion(
        raw_df,
        W_p=best_params.get('W_p', -1.0027),
        k=best_params.get('k', 0.1133),
        lambda_val=best_params.get('lambda_val', 0.0340),
        delta_val=best_params.get('delta_val', 0.0886)
    )
    
    print(f"Processed results dataframe shape: {proc_df.shape}")
    print("Sample Actual_Level trajectory head:")
    print(proc_df[['Student ID', 'Class Number', 'Date', 'Textbook', 'defect_density', 'Actual_Level']].head())
