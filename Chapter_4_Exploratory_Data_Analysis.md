# Chapter 4: Exploratory Data Analysis (EDA)

This chapter presents the four core empirical exploratory data analyses across student academic years, textbook timelines, defect probability lifespans, and bi-monthly problem matrices.

---

## 1. Analysis 1: Yearly Macro-Trends & Dynamic Metric Pairs (Sub-Splits)
To prevent visual clutter across the 14-student cohort, longitudinal multi-line rendering is executed using dynamic student sub-grouping masks across academic year time blocks:

1. **Year 1 Block** ('2017-09-01' to '2018-08-31'):
   * Single cohort chart tracking `Actual_Level`, `current_page`, `Learning_Status`, and `Stability` across all active students.
   * Saved plot: [year1_macro_trends.png](file:///c:/Users/X413F/Documents/2023spring/Statistics%20in%20Violin%20Learning%282026%20revised%20version%29/Original%20Data/year1_macro_trends.png).

2. **Year 2 Block** ('2018-09-01' to '2019-08-31'):
   * **Subgroup A** (Students 1, 2, 3, 4, 5, 6, 7, 8): Saved plot [year2_subgroup_a_macro_trends.png](file:///c:/Users/X413F/Documents/2023spring/Statistics%20in%20Violin%20Learning%282026%20revised%20version%29/Original%20Data/year2_subgroup_a_macro_trends.png).
   * **Subgroup B** (Students 9, 10, 11, 12, 13, 14): Saved plot [year2_subgroup_b_macro_trends.png](file:///c:/Users/X413F/Documents/2023spring/Statistics%20in%20Violin%20Learning%282026%20revised%20version%29/Original%20Data/year2_subgroup_b_macro_trends.png).

3. **Year 3 Block** ('2019-09-01' to '2020-05-31'):
   * **Subgroup A** (Students 1, 3, 4, 5, 6): Saved plot [year3_subgroup_a_macro_trends.png](file:///c:/Users/X413F/Documents/2023spring/Statistics%20in%20Violin%20Learning%282026%20revised%20version%29/Original%20Data/year3_subgroup_a_macro_trends.png).
   * **Subgroup B** (Students 9, 10, 11, 13, 14): Saved plot [year3_subgroup_b_macro_trends.png](file:///c:/Users/X413F/Documents/2023spring/Statistics%20in%20Violin%20Learning%282026%20revised%20version%29/Original%20Data/year3_subgroup_b_macro_trends.png).

---

## 2. Analysis 2: Accumulated Textbook Journey Timeline
Tracks class sequence counts required to reach key Shinozaki textbook page milestones.

| Target Page Milestone | Active Student Count ($N$) | Mean Class Sequence Count | Std Dev | Variance | Avg Practice Delta (hrs/class) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Page 4** | 14 | 1.4286 | 1.0894 | 1.1868 | 1.6429 |
| **Page 5** | 14 | 2.2143 | 1.4769 | 2.1813 | 1.7143 |
| **Page 10** | 14 | 7.5000 | 2.8488 | 8.1154 | 1.8214 |
| **Page 15** | 14 | 15.7857 | 4.3182 | 18.6467 | 1.9000 |
| **Page 20** | 13 | 24.0769 | 6.1299 | 37.5769 | 1.9538 |
| **Page 25** | 12 | 32.4167 | 7.8913 | 62.2652 | 2.0250 |
| **Page 30** | 11 | 40.7273 | 9.4243 | 88.8182 | 2.1000 |

* Saved Table CSV: `accumulated_textbook_milestones.csv`.

---

## 3. Analysis 3: 18 Independent Defect Probability Lifespans
Evaluates rolling defect occurrence probabilities across lesson sequence numbers ($t = 1$ to $130$) across the 18 flaw categories.
* **Early-Stage High Defect Saturation**: `Bow hold`, `Wrist`, `Violin position`, `Neck` show peak occurrence ($p > 0.45$) during initial lesson sequence steps ($t \le 20$).
* **Late-Stage Technical Flaws**: `Intonation`, `Reading music`, `Tempo`, `Beat` remain active through advanced pages ($t > 60$).
* Saved Grid Plot (18 subplots): [defect_probability_lifespans.png](file:///c:/Users/X413F/Documents/2023spring/Statistics%20in%20Violin%20Learning%282026%20revised%20version%29/Original%20Data/defect_probability_lifespans.png).

---

## 4. Analysis 4: Two-Month Interval Unified Cohort Problem Matrix
Pivots defect occurrence probabilities paired with exact observation counts formatted as `Probability (N=Count)` across 2-month timeline intervals, split by age cohort (**Age 6** vs. **Age 7**).

| Defect Category | Cohort | Months 1-2 | Months 3-4 | Months 5-6 | Months 7-8 | Months 9-10 | Months 11-12 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Neck** | Age 6 | 0.4583 (N=48) | 0.3125 (N=48) | 0.2500 (N=44) | 0.1818 (N=44) | 0.1250 (N=40) | 0.0833 (N=36) |
|  | Age 7 | 0.3889 (N=64) | 0.2656 (N=64) | 0.2031 (N=64) | 0.1562 (N=64) | 0.1094 (N=64) | 0.0625 (N=64) |
| **Bow hold** | Age 6 | 0.5208 (N=48) | 0.3958 (N=48) | 0.3182 (N=44) | 0.2273 (N=44) | 0.1750 (N=40) | 0.1111 (N=36) |
|  | Age 7 | 0.4375 (N=64) | 0.3281 (N=64) | 0.2500 (N=64) | 0.1875 (N=64) | 0.1406 (N=64) | 0.0938 (N=64) |
| **Wrist** | Age 6 | 0.4167 (N=48) | 0.2917 (N=48) | 0.2045 (N=44) | 0.1364 (N=44) | 0.0750 (N=40) | 0.0278 (N=36) |
|  | Age 7 | 0.3438 (N=64) | 0.2344 (N=64) | 0.1719 (N=64) | 0.1094 (N=64) | 0.0625 (N=64) | 0.0156 (N=64) |

* Saved Matrix CSV: `two_month_defect_matrix.csv`.
