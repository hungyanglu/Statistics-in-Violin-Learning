# Chapter 1: Data Architecture and State-Space Modeling

## I. Data Architecture and State-Space Modeling

### 1. Feature & Target Spaces & Data Preprocessing
The feature space, target space, and temporal preprocessing transformations across the dataset ($N = 1,213$ observations across 14 students) are defined as follows:

- **$\mathbf{X}_{\text{features}}$**: The input matrix includes the 18 technical/musical defect columns (normalized between $0.0$ and $1.0$: `Neck`, `Bow hold`, `Elbow`, `Wrist`, `Bow slipping`, `Reading music`, `Intonation`, `Violin position`, `Beat`, `Bow tilt`, `Tempo`, `Bow pressure`, `Finger pressure`, `Fingering`, `Focus`, `Bow markings`, `Swaying`, `Miscellaneous`), weekly `Practice` time, `current_page`, and lesson `date`.
- **$\mathbf{Y}_{\text{target}}$**: Progression velocity target $`\text{page\_delta}`$ ($`\Delta x_t = \text{current\_page}_t - \text{current\_page}_{t-1}`$), representing raw page progression velocity.
- **Practice Time Delta**: Localized delta steps calculated per lesson (unit: half hour).
- **Class Date Intervals**: Elapsed time delta ($`\text{interval\_weeks}`$) computed between consecutive class records per student.

---

### 2. Left-Censored Class Timeline Offsets & Known Performance Window Override

- **Timeline Anchors**: Initialize each student's starting tracking anchor ($A_0$):
  - If $`\text{student\_id} == 3`$: $A_0 = 8$ (First tracked data points begin at Class 8)
  - If $`\text{student\_id} == 6`$: $A_0 = 19$ (First tracked data points begin at Class 19)
  - For all other students: $A_0 = 1$

- **Hardcoded Historical Concert Window**: Enforce a programming override where $`\text{Is\_Performance\_Prep} = \text{True}`$ for $`\text{student\_id} \in [3, 4, 5, 6]`$ if the session date falls within the calendar window [`2017-09-08` $\le \text{date} \le$ `2017-11-17`].

---

### 3. Prior Knowledge Identification Engine (Post-Concert Filtered Detection)
For Age 7 starters (including Student 7), calculate their static prior knowledge baseline by evaluating tracking records. For Students 3, 4, 5, and 6, do not evaluate data during the hardcoded performance window; apply the dual-condition detection algorithm strictly on observations where $\text{date} > \text{'2017-11-17'}$:

- **Condition 1 (Cohort-Referenced)**: Run a continuous two-sample t-test comparing the student's cumulative defects against the average defect baseline of Age 6 beginners. Find where the student's defects are no longer significantly lower ($p > 0.05$) for 3 consecutive weeks.
- **Condition 2 (Self-Referenced)**: Run a moving Z-score analysis on the student's own defects against their rolling 3-week mean. Find where defects spike significantly ($Z > 1.96$).

**Execution**: The first class $t^*$ meeting either condition defines $`\text{Prior\_Knowledge\_Page}`$ as the raw textbook page value at that class.
- **For Age 7 Starters**: $`\text{Prior\_Knowledge\_Bonus}_i = \text{Prior\_Knowledge\_Page}`$ (Fixed constant parameter applied uniformly across the entire timeline from Class 1. It does NOT decay over time to prevent artificial trajectory drops).
- **For Age 6 Beginners**: $`\text{Prior\_Knowledge\_Bonus}_i = 0.0`$.

---

### 4. SPC Structural Break Engine (Multi-Concert Tracking States)
Outside of the hardcoded historical window defined in Section I.2, track performance periods using a moving Welch's Two-Sample t-Test (allowing unequal variances):

- **Distribution I (Historical Baseline)**: At each week $t$, compute the personalized mean ($\mu$) and standard deviation ($\sigma$) of $`\text{page\_delta}`$ using all observations spanning from week 1 up to week $t$.
- **Distribution II (Evaluation Window)**: Compute the moving average of $`\text{page\_delta}`$ over an isolated 3-week evaluation block spanning from week $t-2$ to week $t$.
- **Regime Entry Boundary**: Switch $`\text{Is\_Performance\_Prep} = \text{True}`$ strictly when the textbook deceleration p-value drops below 0.05 ($p < 0.05$). At the exact lesson of entry, capture the current value of $`\text{Performance\_Bonus}`$ as the $`\text{Base\_Asset\_Entry}`$ for this specific performance window. Reset the localized special points counter for this window to zero. When $\text{True}$, freeze all textbook velocity decay structural penalties.
- **Regime Exit Boundary**: Revert $`\text{Is\_Performance\_Prep} = \text{False}`$ strictly when the deceleration p-value returns to a non-significant state ($p \ge 0.05$). Track the raw textbook page where this exit occurs as $`P_{\text{exit}}`$, and the peak accumulated bonus value achieved at that exact class as $`\text{Peak\_Bonus}`$.

---

### 5. Latent Metric Formulations

- **Mastery Penalty Vector**:
  $`$\text{Mastery\_Bonus}_{i,t} = W_p \times \left( \frac{\sum_{p=1}^{18} \text{Problem}_{i,t,p}}{18.0} \right) \quad [\text{Expected Range: } W_p \text{ to } 0]$`$

- **Recursive Multi-Stage Performance Asset Engine**: To cleanly process multiple independent performance periods across a student's timeline without resetting historical gains or losing scale parameters, implement recursive state-dependent logic:
  - **If $`\text{Is\_Performance\_Prep} == \text{True}`$**: Track cumulative special points earned strictly *since the entry boundary of the current performance period* ($`\text{Window\_Points}`$). Calculate growth via the localized logistic curve layered directly on top of their entry baseline:
    $`$\text{Performance\_Bonus}_{i,t} = \text{Base\_Asset\_Entry} + \left( \frac{10.0}{1.0 + e^{-k \times \text{Window\_Points}}} - 5.0 \right)$`$
  - **If $`\text{Is\_Performance\_Prep} == \text{False}`$**: Gently dissipate the peak performance asset over the page distance traveled since the most recent concert exit boundary:
    $`$\text{Performance\_Bonus}_{i,t} = \text{Peak\_Bonus} \times e^{-\delta \times \max(0, \, \text{current\_page}_{i,t} - P_{\text{exit}})}$`$
    (Where $\delta$ is a positive page assimilation parameter optimized via Optuna. This ensures that the gained asset holds at entry, decays predictably during normal study, and serves as the precise starting floor for any subsequent performance periods).

---

### 6. Vacation & Absence Handling Engine

- **Short Absences ($\le 2$ weeks)**: Freeze decay state; exclude rows from the Optuna variance loss calculation.
- **Long Vacations ($> 2$ weeks)**: Model skill de-conditioning exponentially via decay parameter lambda ($\lambda$). Upon the first 3 weeks of return, multiply $`\text{Mastery\_Bonus}`$ by a rust multiplier: $`(1.0 + 0.1 \times \text{interval\_weeks})`$.

---

### 7. Master State Fusion Equation (Adaptive Baseline Convergence Framework)
Synthesize the final hidden ability metric using cohort-specific structural definitions. To reflect behavioral adaptivity where the clean latent line naturally and smoothly bends closer to the raw textbook line as advanced material is uncovered, apply a soft-start exponential progress parameter gamma ($\gamma$) optimized via Optuna to the raw progression components:

- **For Age 6 Beginners**:
  $`$\text{Actual\_Level}_{i,t} = \text{current\_page}_{i,t} + \left(e^{-\lambda \times \Delta t_{\text{absent}}}\right) \times \text{Mastery\_Bonus}_{i,t} + \text{Performance\_Bonus}_{i,t}$`$

- **For Student 3**:
  $`$\text{Delta\_Page} = \text{current\_page}_{i,t} - 10.0$`$
  
  $`$\text{Adaptive\_Progress} = \text{Delta\_Page} \times \left(1.0 - e^{-\gamma \times \text{Delta\_Page}}\right)$`$
  
  $`$\text{Actual\_Level}_{i,t} = \text{Adaptive\_Progress} + \left(e^{-\lambda \times \Delta t_{\text{absent}}}\right) \times \text{Mastery\_Bonus}_{i,t} + \text{Performance\_Bonus}_{i,t} + \text{Prior\_Knowledge\_Bonus}_i$`$

- **For Student 6**:
  $`$\text{Delta\_Page} = \text{current\_page}_{i,t} - 18.0$`$
  
  $`$\text{Adaptive\_Progress} = \text{Delta\_Page} \times \left(1.0 - e^{-\gamma \times \text{Delta\_Page}}\right)$`$
  
  $`$\text{Actual\_Level}_{i,t} = \text{Adaptive\_Progress} + \left(e^{-\lambda \times \Delta t_{\text{absent}}}\right) \times \text{Mastery\_Bonus}_{i,t} + \text{Performance\_Bonus}_{i,t} + \text{Prior\_Knowledge\_Bonus}_i$`$

- **For Age 7 Starters (except students 3 and 6)**:
  $`$\text{Delta\_Page} = \text{current\_page}_{i,t} - 3.0$`$
  
  $`$\text{Adaptive\_Progress} = \text{Delta\_Page} \times \left(1.0 - e^{-\gamma \times \text{Delta\_Page}}\right)$`$
  
  $`$\text{Actual\_Level}_{i,t} = \text{Adaptive\_Progress} + \left(e^{-\lambda \times \Delta t_{\text{absent}}}\right) \times \text{Mastery\_Bonus}_{i,t} + \text{Performance\_Bonus}_{i,t} + \text{Prior\_Knowledge\_Bonus}_i$`$

---

## II. Time-Series State-Space Estimation
Split the data into an 80% within-subject proportional chronological training set and a 20% test set. Pass the converted $`\text{Actual\_Level}`$ trajectory into:

1. **Kalman Filter (DLM)**: Local Linear Trend Model tracking true underlying capability velocity against measurement noise.
2. **VARMAX(1,0)**: Measure cross-lagged feedback loops between $`\Delta \text{Actual\_Level}_{t-1}`$ and next week's practice motivation parameters.

---

## III. Bayesian Optimization Framework
Wrap the entire pipeline inside an Optuna objective function to optimize structural variables across 100 trials:

- **$W_p$ (Mastery Bounded Weight)**: Continuous negative scale from $-10.0$ to $-1.0$.
- **$k$ (Sigmoid Growth Velocity)**: Continuous scale from $0.005$ to $0.150$.
- **$\lambda$ (Skill Decay Rate)**: Continuous scale from $0.01$ to $0.10$.
- **$\gamma$ (Adaptive Progress Scale)**: Continuous scale from $0.01$ to $0.30$.
- **$\delta$ (Performance Asset Assimilation Decay)**: Continuous scale from $0.05$ to $0.50$.

**Minimize the Composite Trajectory Loss**:
$`$\text{Loss} = \left( 10 \times \sum \max(0, -\Delta \text{Actual\_Level}_{i,t}) \right) + \text{Var}(\Delta \text{Actual\_Level})$`$

### 100-Trial Optuna Optimization Best Results

- **Best Composite Trajectory Loss**: `184.2234`
- **Sampler**: Tree-structured Parzen Estimator (TPE, 100 trials)

| Hyperparameter | Symbol | Specified Search Range | Optimal Parameter Value | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Mastery Bounded Weight** | $W_p$ | `[-10.0, -1.0]` | **`-1.0015`** | Defect penalty scaling factor |
| **Sigmoid Growth Velocity** | $k$ | `[0.005, 0.150]` | **`0.0309`** | Performance asset accumulation rate |
| **Skill Rust Decay Rate** | $\lambda$ | `[0.01, 0.10]` | **`0.0475`** | Absence exponential decay parameter |
| **Adaptive Progress Scale** | $\gamma$ | `[0.01, 0.30]` | **`0.0530`** | Convergence rate to raw textbook line |
| **Performance Asset Assimilation** | $\delta$ | `[0.05, 0.50]` | **`0.3427`** | Post-concert asset dissipation decay |
