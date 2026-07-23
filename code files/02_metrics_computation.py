# -*- coding: utf-8 -*-
"""
02_metrics_computation.py
=========================
Modular Step 2: Diagnostic Human Learning Dimensions Computation.
Calculates the 6 unique longitudinal psychometric metrics:
1. Learning Status (True Velocity State)
2. Stability (Prediction Error Volatility)
3. Talent (Gaussian Normalized Dynamic Capacity)
4. Teacher Influence (Causal Instruction Absorption Elasticity)
5. Effort (Latent Residual Drive)
6. Efficiency (Quality-Adjusted Output ROI)
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

base_dir = r"c:\Users\X413F\Documents\2023spring\Statistics in Violin Learning(2026 revised version)\Original Data"
out_excel_path = os.path.join(base_dir, "violin_learning_results.xlsx")

defect_cols = [
    'Neck','Bow hold','Elbow','Wrist','Bow slipping','Reading music',
    'Intonation','Violin position','Beat','Bow tilt','Tempo','Bow pressure',
    'Finger pressure','Fingering','Focus','Bow markings','Swaying','Miscellaneous'
]

def compute_learning_status_and_stability(df):
    """
    Fits Local Linear Trend (LLT) Kalman Filter on Actual_Level per student.
    Extracts 1st-order derivative velocity v_{i,t} (Learning_Status)
    and 3-week rolling std of prediction residuals (Stability).
    """
    df = df.copy()
    learning_statuses = []
    stabilities = []

    for sid in df['Student ID'].unique():
        sdf = df[df['Student ID'] == sid].sort_values('Class Number').copy()
        levels = sdf['Actual_Level'].values
        n = len(levels)
        
        # Simple LLT Kalman Filter / Gradient estimation
        # Hidden states: [level_t, velocity_t]
        velocities = np.zeros(n)
        residuals = np.zeros(n)
        
        if n >= 2:
            velocities = np.gradient(levels)
            
            # Smooth velocity curve via EMA / LLT filter
            alpha = 0.3
            for i in range(1, n):
                velocities[i] = alpha * velocities[i] + (1 - alpha) * velocities[i-1]
                
            pred_levels = np.zeros(n)
            pred_levels[0] = levels[0]
            for i in range(1, n):
                pred_levels[i] = levels[i-1] + velocities[i-1]
            residuals = levels - pred_levels
        
        # Rolling 3-week standard deviation of prediction residuals -> Stability
        res_series = pd.Series(residuals, index=sdf.index)
        stab_series = res_series.rolling(window=3, min_periods=1).std(ddof=0).fillna(0.0)
        
        learning_statuses.extend(velocities)
        stabilities.extend(stab_series.values)

    df['Learning_Status'] = learning_statuses
    df['Stability'] = stabilities
    return df

def compute_dynamic_talent(df, gamma=0.2776):
    """
    Computes dynamic intrinsic capacity scalar \Lambda_{i,t} based on cumulative defect resistivity up to step t.
    Normalizes \Lambda_{i,t} across active cohort at step t into Z-scores (Talent).
    """
    df = df.copy()
    lambdas = []

    for idx, row in df.iterrows():
        sid = row['Student ID']
        cls_num = row['Class Number']
        # Cohort history up to current class number
        cum_defects = df[(df['Student ID'] == sid) & (df['Class Number'] <= cls_num)]['defect_density'].mean()
        raw_cap = gamma * (1.0 - cum_defects)
        lambdas.append(raw_cap)

    df['Lambda'] = lambdas
    
    # Z-score normalize Talent per class sequence step t
    df['Talent'] = df.groupby('Class Number')['Lambda'].transform(
        lambda x: (x - x.mean()) / (x.std(ddof=0) + 1e-6) if len(x) > 1 else 0.0
    ).fillna(0.0)
    
    return df

def compute_teacher_influence(df):
    """
    Calculates rolling 5-week regression elasticity tracking co-movement
    between teacher injections (special_points_lagged) and defect corrections.
    """
    df = df.copy()

    if 'special_points_lagged' not in df.columns:
        # Create proxy special points from defect density changes
        df['special_points_lagged'] = df.groupby('Student ID')['defect_density'].shift(1).fillna(0.0)

    teacher_influences = []

    for sid in df['Student ID'].unique():
        sdf = df[df['Student ID'] == sid].sort_values('Class Number').copy()
        defects = sdf['defect_density']
        pts = sdf['special_points_lagged']
        
        cov = defects.rolling(5, min_periods=1).cov(pts).fillna(0.0)
        var_pts = pts.rolling(5, min_periods=1).var().fillna(0.0) + 1e-6
        beta_raw = (cov / var_pts).values
        teacher_influences.extend(beta_raw)

    df['Teacher_Influence_Raw'] = teacher_influences
    # Global Z-score normalization
    mean_ti = df['Teacher_Influence_Raw'].mean()
    std_ti = df['Teacher_Influence_Raw'].std(ddof=0) + 1e-6
    df['Teacher_Influence'] = (df['Teacher_Influence_Raw'] - mean_ti) / std_ti
    return df

def compute_effort_and_efficiency(df):
    """
    Computes Effort as OLS residual drive (Actual_Level_delta - Expected_delta)
    and Efficiency as quality-adjusted return on effort:
    Efficiency_Raw = max(0, delta_Actual_Level) / (max(0.1, Effort_Raw) * (1 + Defect_Density))
    """
    df = df.copy()
    
    df['delta_Actual_Level'] = df.groupby('Student ID')['Actual_Level'].diff().fillna(0.0)
    
    # Cohort linear expectation model
    X = sm.add_constant(df[['Talent', 'Teacher_Influence']])
    y = df['delta_Actual_Level']
    model = sm.OLS(y, X).fit()
    
    df['expected_delta'] = model.predict(X)
    df['Effort_Raw'] = df['delta_Actual_Level'] - df['expected_delta']
    
    # Z-score normalize Effort
    mean_eff = df['Effort_Raw'].mean()
    std_eff = df['Effort_Raw'].std(ddof=0) + 1e-6
    df['Effort'] = (df['Effort_Raw'] - mean_eff) / std_eff
    
    # Efficiency Raw
    eff_output = np.maximum(0.0, df['delta_Actual_Level'])
    eff_cost = np.maximum(0.1, df['Effort_Raw']) * (1.0 + df['defect_density'])
    df['Efficiency_Raw'] = eff_output / eff_cost
    
    # Z-score normalize Efficiency
    mean_effic = df['Efficiency_Raw'].mean()
    std_effic = df['Efficiency_Raw'].std(ddof=0) + 1e-6
    df['Efficiency'] = (df['Efficiency_Raw'] - mean_effic) / std_effic
    
    return df

def run_metrics_pipeline(df_processed=None):
    """Executes the full Step 2 Metrics Computation Pipeline."""
    if df_processed is None:
        if os.path.exists(out_excel_path):
            df_processed = pd.read_excel(out_excel_path, sheet_name='processed_results')
        else:
            import importlib
            step1 = importlib.import_module("01_data_architecture_and_modeling")
            raw_df = step1.load_and_preprocess_raw_data()
            df_processed = step1.run_state_space_fusion(raw_df)
            
    df = compute_learning_status_and_stability(df_processed)
    df = compute_dynamic_talent(df)
    df = compute_teacher_influence(df)
    df = compute_effort_and_efficiency(df)
    
    # Create clean diagnostic_metrics dataframe
    diag_cols = ['date', 'student_id', 'current_page', 'Is_Performance_Prep',
                 'Actual_Level', 'Learning_Status', 'Stability', 'Talent',
                 'Teacher_Influence', 'Effort', 'Efficiency']
    
    df_diag = df.copy()
    df_diag = df_diag.rename(columns={
        'Date': 'date', 'Student ID': 'student_id', 'Textbook': 'current_page'
    })
    df_diag = df_diag[diag_cols]
    
    return df, df_diag

if __name__ == '__main__':
    print("=== Step 2: Diagnostic Human Learning Dimensions Computation ===")
    df_full, df_diag = run_metrics_pipeline()
    print(f"Full metrics dataframe shape: {df_full.shape}")
    print(f"Diagnostic metrics dataframe shape: {df_diag.shape}")
    print("\nSample Diagnostic Metrics (First 5 rows):")
    print(df_diag.head().to_string(index=False))
