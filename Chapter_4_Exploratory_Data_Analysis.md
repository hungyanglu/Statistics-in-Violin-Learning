# Chapter 4: Exploratory Data Analysis (EDA)

This chapter presents the four core empirical exploratory data analyses across student academic years, textbook timelines, defect probability lifespans, and bi-monthly problem matrices.

---

## 1. Analysis 1: Yearly Macro-Trends & Dynamic Metric Pairs (Sub-Splits)
To prevent visual clutter across the 14-student cohort, longitudinal multi-line rendering is executed using dynamic student sub-grouping masks across academic year time blocks:

1. **Year 1 Block** ('2017-09-01' to '2018-08-31'):
* Saved plot: [year1_macro_trends.png]

Across the 2017/9–2018/8 academic year, textbook pages and actual level show a continuous overall upward trend. Both metrics rise steadily during the initial months, briefly plateau horizontally during the winter performance preparation period when regular textbook page-turning pauses, and then resume a rapid linear growth phase in the spring before settling into a milder growth slope in July and August as material difficulty increases.

Except for Student 3, whose learning status gradually increases to a steady value, the cohort generally starts at an early high point, decreases over the first two months during the initial adjustment period, and then steadily rises back up to a stable level.

Student stability follows two primary pathways: the first starts at a high initial volatility level and gradually decays over time, while the second begins near zero, rises to a mid-term peak during the learning adjustment phase, and then steadily decreases toward a low, consistent baseline.

2. **Year 2 Block** ('2018-09-01' to '2019-08-31'):
* **Subgroup A** (Students 1, 2, 3, 4, 5, 6, 7, 8): Saved plot [year2_subgroup_a_macro_trends.png]

Across the 2018/9–2019/8 academic year, textbook pages and actual level maintain a general upward trajectory. Both curves rise steadily in the autumn, enter a temporary horizontal plateau during the performance preparation period, where regular page-turning pauses, and then resume steady growth through the spring before moderating in the summer as technical difficulty increases.

The cohort generally starts the year with moderate to high learning status, experiences a sharp dip toward zero during the winter performance preparation window when page progress stalls, and then rebounds back to a stable level in the spring.

Performance volatility fluctuates early in the academic year before settling into a low, consistent baseline for continuing students through the spring.

* **Subgroup B** (Students 9, 10, 11, 12, 13, 14): Saved plot [year2_subgroup_b_macro_trends.png]

Across the 2018/9–2019/8 academic year, textbook pages and actual level show a continuous overall upward trend. Both metrics climb steadily through the autumn, enter a temporary horizontal plateau during the performance preparation period when regular page-turning pauses, and then resume linear growth.

The cohort generally starts the year with moderate to high learning status, experiences a temporary dip toward zero during the winter performance preparation window when regular page assignments pause, and subsequently rebounds back to a stable level.

Like student 1-6 last year, student stability primarily follows two pathways: one starts with high initial volatility that gradually decays over time, while the other starts low, climbs to a peak during the mid-term adjustment phase, and then steadily decreases toward a consistent low baseline.

2. **Year 3 Block** ('2019-09-01' to '2020-05-31'):
* **Subgroup A** (Students 1, 3, 4, 5, 6): Saved plot [year3_subgroup_a_macro_trends.png]
  
Student 5 consistently demonstrates the strongest overall capability, while Student 6 remains at the lowest tier before data concludes early (due to vacation), with Students 1, 3, and 4 catching up by the end of the term. Concurrently, textbook progression steadily advances for most individuals, though one student experiences a prolonged mid-year plateau before resuming progress.

Learning velocity fluctuates considerably across the timeline, characterized by a noticeable collective dip near the beginning of spring 2020 followed by a dramatic acceleration and peak for several students toward the final months.

Volatility reveals persistent behavioral and performance instability throughout the academic year, highlighted by severe disruption spikes during late autumn 2019 and frequent, wide oscillations during the spring months.

* **Subgroup B** (Students 9, 10, 11, 13, 14): Saved plot [year3_subgroup_b_macro_trends.png]

Student 10 consistently leads the subgroup with the highest overall capability and textbook progression, while Student 14 remains at the lowest tier throughout the academic year. Concurrently, the other participants show steady, parallel upward trajectories in both capability and material coverage without sudden plateaus.

Learning velocity diverges notably across the group, with Student 10 and Student 14 maintaining the highest and most active rates of progression. Meanwhile, the remaining students display steady, tightly clustered, and largely flat velocity trends over time.

Volatility indicates varying degrees of consistency, highlighted by a massive initial disruption spike for Student 14 at the start of the term and intermittent, moderate fluctuations across the other members during the winter and spring months.

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
* Saved Grid Plot (18 subplots): [defect_probability_lifespans.png].

Here are the brief descriptions for each problem:

* Neck: Defect probability rises noticeably around the middle of the class sequence, reaching peaks near 0.6 before dropping sharply to zero toward the end.

* Bow hold: Probability starts elevated near 0.8 at the beginning of the sequence and then quickly drops, remaining low and sporadic for the rest of the timeline.

* Elbow: The probability stays consistently low and volatile, fluctuating mostly under 0.4 across the entire class sequence.

* Wrist: Defect probability is highest at the very beginning of the sequence before dropping to near-zero for the majority of the timeline with only minor bumps.

* Bow slipping: Probability exhibits high volatility throughout the first half and middle sections, eventually decreasing and dropping to zero toward the final classes.

* Reading music: Defect probability remains consistently high and fluctuates frequently between 0.3 and 1.0 across the entire class sequence.

* Intonation: Probability shows a steady upward trend over the sequence, reaching maximum values of 1.0 in the latter half before declining near the end.

* Violin position: Defect probability stays relatively low and constrained mostly below 0.4 across the entire sequence.

* Beat: Probability remains low and flat for most of the sequence, with a sharp spike appearing near the final classes.

* Bow tilt: Defect probability stays low throughout the entire sequence, rarely exceeding 0.3 with several flat periods.

* Tempo: Probability remains low for the majority of the sequence, showing moderate increases toward the later classes.

* Bow pressure: Defect probability stays mostly low and sporadic, with a few isolated spikes occurring near the end of the sequence.

* Finger pressure: Probability remains mostly near zero for the entire sequence, culminating in a sudden, sharp spike to 1.0 on the final classes.

* Fingering: Defect probability increases progressively as the sequence advances, peaking significantly toward the final classes.

* Focus: Probability stays low overall with a prominent peak reaching around 0.6 in the middle section of the sequence.

* Bow markings: Probability is zero for the first third of the sequence, then rises significantly with high fluctuations and peaks reaching 1.0.

* Swaying: Defect probability remains almost entirely at zero across the entire class sequence, with only a few minor blips.

* Miscellaneous: Probability stays consistently low throughout the sequence, ending with a sharp spike to 1.0 near the final class numbers.
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
