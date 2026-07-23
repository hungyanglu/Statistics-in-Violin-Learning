# -*- coding: utf-8 -*-
"""
03_exploratory_data_analysis.py
===============================
Modular Step 3: Exploratory Data Analysis & Rendering Pipeline.
Generates all 4 EDA visual blocks and tables:
1. Yearly Macro-Trends & Dynamic Metric Pairs (Sub-Splits)
2. Accumulated Textbook Journey Timeline
3. 18 Independent Defect Probability Lifespans
4. Two-Month Interval Unified Cohort Problem Matrix (Probability (N=Count))
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

base_dir = r"c:\Users\X413F\Documents\2023spring\Statistics in Violin Learning(2026 revised version)\Original Data"
art_dir  = r"C:\Users\X413F\.gemini\antigravity\brain\9981a9e3-bb66-4b07-9f5c-463e4424414b"
excel_path = os.path.join(base_dir, "violin_learning_results.xlsx")

defect_cols = [
    'Neck','Bow hold','Elbow','Wrist','Bow slipping','Reading music',
    'Intonation','Violin position','Beat','Bow tilt','Tempo','Bow pressure',
    'Finger pressure','Fingering','Focus','Bow markings','Swaying','Miscellaneous'
]

def generate_analysis_1_macro_trends(df):
    """
    Analysis 1: Yearly Macro-Trends & Dynamic Metric Pairs using explicit sub-groups.
    Year 1: All active students
    Year 2 Subgroup A: Students 1-8 | Subgroup B: Students 9-14
    Year 3 Subgroup A: Students 1,3,4,5,6 | Subgroup B: Students 9,10,11,13,14
    """
    df = df.copy()
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%Y.%m.%d')
    
    y1_mask = (df['parsed_date'] >= '2017-09-01') & (df['parsed_date'] <= '2018-08-31')
    y2_mask = (df['parsed_date'] >= '2018-09-01') & (df['parsed_date'] <= '2019-08-31')
    y3_mask = (df['parsed_date'] >= '2019-09-01') & (df['parsed_date'] <= '2020-05-31')
    
    # Subgroup definitions
    y2_grp_a = [1, 2, 3, 4, 5, 6, 7, 8]
    y2_grp_b = [9, 10, 11, 12, 13, 14]
    y3_grp_a = [1, 3, 4, 5, 6]
    y3_grp_b = [9, 10, 11, 13, 14]
    
    plots_config = [
        ("Year 1 Macro-Trends (All Active Students)", df[y1_mask], "year1_macro_trends.png"),
        ("Year 2 - Subgroup A (Students 1-8)", df[y2_mask & df['Student ID'].isin(y2_grp_a)], "year2_subgroup_a_macro_trends.png"),
        ("Year 2 - Subgroup B (Students 9-14)", df[y2_mask & df['Student ID'].isin(y2_grp_b)], "year2_subgroup_b_macro_trends.png"),
        ("Year 3 - Subgroup A (Students 1,3,4,5,6)", df[y3_mask & df['Student ID'].isin(y3_grp_a)], "year3_subgroup_a_macro_trends.png"),
        ("Year 3 - Subgroup B (Students 9,10,11,13,14)", df[y3_mask & df['Student ID'].isin(y3_grp_b)], "year3_subgroup_b_macro_trends.png"),
    ]
    
    for title, sub_data, filename in plots_config:
        if len(sub_data) == 0: continue
        fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
        fig.suptitle(title, fontsize=14, fontweight='bold')
        
        metrics = [
            ('Actual_Level', 'Actual Level (Capability)', axes[0,0]),
            ('Textbook', 'Current Page (Textbook)', axes[0,1]),
            ('Learning_Status', 'Learning Status (Velocity)', axes[1,0]),
            ('Stability', 'Stability (Volatility)', axes[1,1])
        ]
        
        cmap = plt.cm.tab20
        unique_students = sorted(sub_data['Student ID'].unique())
        color_map = {sid: cmap(i / max(1, len(unique_students)-1)) for i, sid in enumerate(unique_students)}
        
        for metric_col, metric_label, ax in metrics:
            for sid in unique_students:
                sdf = sub_data[sub_data['Student ID'] == sid].sort_values('parsed_date')
                ax.plot(sdf['parsed_date'], sdf[metric_col], label=f'Student {sid}', color=color_map[sid], lw=1.5)
            ax.set_title(metric_label, fontsize=11)
            ax.grid(True, linestyle=':', alpha=0.6)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            
        axes[0,1].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        plt.tight_layout(rect=[0, 0, 0.9, 0.95])
        
        for pth in [os.path.join(base_dir, filename), os.path.join(art_dir, filename)]:
            fig.savefig(pth, dpi=300)
        plt.close()
        print(f"  [SAVED]: {filename}")

def generate_analysis_2_textbook_journey(df):
    """Analysis 2: Accumulated Textbook Journey Timeline Table (All sequential pages)."""
    df = df.copy()
    min_page = int(df['Textbook'].min())
    max_page = int(df['Textbook'].max())
    milestones = list(range(min_page, max_page + 1))
    records = []
    
    for page in milestones:
        reached = df[df['Textbook'] >= page].groupby('Student ID')['Class_Sequence_Number'].min()
        prac_means = df[df['Textbook'] >= page].groupby('Student ID')['Practice'].mean()
        
        if len(reached) > 0:
            std_val = round(reached.std(), 4) if len(reached) > 1 else 0.0
            var_val = round(reached.var(), 4) if len(reached) > 1 else 0.0
            records.append({
                'Target_Page_Milestone': f"Page {page}",
                'Active_Student_Count': len(reached),
                'Mean_Class_Sequence_Count': round(reached.mean(), 4),
                'Std_Dev': std_val,
                'Variance': var_val,
                'Avg_Practice_Hours_Per_Class': round(prac_means.mean(), 4)
            })
            
    df_miles = pd.DataFrame(records)
    csv_path = os.path.join(base_dir, "accumulated_textbook_milestones.csv")
    df_miles.to_csv(csv_path, index=False)
    df_miles.to_csv(os.path.join(art_dir, "accumulated_textbook_milestones.csv"), index=False)
    print(f"  [SAVED]: accumulated_textbook_milestones.csv ({len(df_miles)} total pages: Page {min_page} to Page {max_page})")
    return df_miles

def generate_analysis_3_defect_probability_lifespans(df):
    """Analysis 3: 18 Independent Defect Probability Lifespans Grid (18 subplots)."""
    df = df.copy()
    fig, axes = plt.subplots(6, 3, figsize=(16, 16), sharex=True, sharey=True)
    fig.suptitle('18 Independent Defect Probability Lifespans (Class Sequence 1 to 130)', fontsize=14, fontweight='bold')
    
    seq_nums = np.arange(1, 131)
    
    for i, col in enumerate(defect_cols):
        ax = axes[i // 3, i % 3]
        prob_series = df.groupby('Class_Sequence_Number')[col].apply(lambda x: (x > 0).mean())
        
        # Smooth curve
        probs = [prob_series.get(s, np.nan) for s in seq_nums]
        ax.plot(seq_nums, probs, color='darkred', lw=1.5)
        ax.set_title(col, fontsize=10, fontweight='bold')
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.set_ylim(-0.05, 1.05)
        if i // 3 == 5: ax.set_xlabel('Class Sequence Number')
        if i % 3 == 0: ax.set_ylabel('Probability')
        
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    for pth in [os.path.join(base_dir, "defect_probability_lifespans.png"), os.path.join(art_dir, "defect_probability_lifespans.png")]:
        fig.savefig(pth, dpi=300)
    plt.close()
    print("  [SAVED]: defect_probability_lifespans.png")

def generate_analysis_4_two_month_matrix(df):
    """
    Analysis 4: Two-Month Interval Unified Cohort Problem Matrix
    Cell text formatted exactly as: Probability (N=Count)
    """
    df = df.copy()
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%Y.%m.%d')
    entry_dates = df.groupby('Student ID')['parsed_date'].min()
    df['entry_date'] = df['Student ID'].map(entry_dates)
    df['elapsed_days'] = (df['parsed_date'] - df['entry_date']).dt.days
    
    # 2-month intervals (60 days per block)
    df['interval_block'] = (df['elapsed_days'] // 60) + 1
    max_block = int(df['interval_block'].max())
    
    AGE6 = [1, 2, 9, 11, 12, 13]
    AGE7 = [3, 4, 5, 6, 7, 8, 10, 14]
    df['Cohort'] = df['Student ID'].apply(lambda x: 'Age 6' if x in AGE6 else 'Age 7')
    
    # Generate interval columns dynamically for all blocks 1 to max_block (Months 1-2 to max)
    interval_labels = {
        blk: f"Months {(blk - 1) * 2 + 1}-{blk * 2}"
        for blk in range(1, max_block + 1)
    }
    
    rows = []
    for flaw in defect_cols:
        for cohort in ['Age 6', 'Age 7']:
            r = {'Defect_Category': flaw, 'Cohort': cohort}
            for blk, lbl in interval_labels.items():
                sub = df[(df['Cohort'] == cohort) & (df['interval_block'] == blk)]
                n_count = len(sub)
                if n_count > 0:
                    prob = (sub[flaw] > 0).mean()
                    r[lbl] = f"{prob:.4f} (N={n_count})"
                else:
                    r[lbl] = "NaN"
            rows.append(r)
            
    df_matrix = pd.DataFrame(rows)
    csv_path = os.path.join(base_dir, "two_month_defect_matrix.csv")
    df_matrix.to_csv(csv_path, index=False)
    df_matrix.to_csv(os.path.join(art_dir, "two_month_defect_matrix.csv"), index=False)
    print(f"  [SAVED]: two_month_defect_matrix.csv ({max_block} two-month blocks up to {interval_labels[max_block]})")
    return df_matrix

if __name__ == '__main__':
    print("=== Step 3: Exploratory Data Analysis & Rendering Pipeline ===")
    df = pd.read_excel(excel_path, sheet_name='processed_results')
    
    print("\nRunning Analysis 1: Yearly Macro-Trends...")
    generate_analysis_1_macro_trends(df)
    
    print("\nRunning Analysis 2: Textbook Journey Timeline...")
    df_miles = generate_analysis_2_textbook_journey(df)
    print(df_miles.head().to_string(index=False))
    
    print("\nRunning Analysis 3: 18 Defect Lifespans...")
    generate_analysis_3_defect_probability_lifespans(df)
    
    print("\nRunning Analysis 4: Two-Month Cohort Matrix...")
    df_mat = generate_analysis_4_two_month_matrix(df)
    print(df_mat.head(4).to_string(index=False))
