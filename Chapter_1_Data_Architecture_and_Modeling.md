# Chapter 1: Data Architecture and State-Space Modeling

## 1. Feature Space & Longitudinal Target Definition
The dataset captures $N = 1,213$ weekly lesson observations across 14 violin students over a 3-year tracking window (September 2017 to May 2020). The raw tracking space comprises 60 longitudinal variables, categorized into:

1. **Observed Performance Features**:
   * `Class Number`: Continuous integer index of total lesson sequence per student ($t = 1, 2, \dots, T_i$).
   * `Date`: Observation date formatted as `YYYY.MM.DD`.
   * `Age`: Student starting age (Age 6 vs. Age 7 starters).
   * `Practice`: Self-reported weekly home practice hours ($\Delta \text{Practice\_Time}_{i,t}$).
   * `Textbook`: Current page location in the Shinozaki Violin Method ($	ext{Current\_Page}_{i,t}$).
   * `Is_Performance_Prep`: Boolean flag indicating active concert preparation periods.

2. **18 Flaw Category Indicators** ($\mathbf{D}_{i,t} \in \{0.0, 0.5, 1.0\}^{18}$):
   `Neck`, `Bow hold`, `Elbow`, `Wrist`, `Bow slipping`, `Reading music`, `Intonation`, `Violin position`, `Beat`, `Bow tilt`, `Tempo`, `Bow pressure`, `Finger pressure`, `Fingering`, `Focus`, `Bow markings`, `Swaying`, `Miscellaneous`.

3. **Target Latent State** ($	heta_{i,t} = \text{Actual\_Level}_{i,t}$):
   The true, unobservable musical capability level of student $i$ at time step $t$.

---

## 2. Left-Censored Class Timeline Offsets & Known Performance Window Override
Students enter the studio at different ages and prior skill levels, resulting in left-censored tracking timelines:
* **True Beginners** (e.g., Student 1, Student 2, Student 9): Enter at Class 1, Page 4 (Shinozaki Volume 1), with zero prior knowledge bonus.
* **Advanced Starters** (e.g., Student 3, Student 4, Student 5, Student 6): Enter with prior violin experience. Left-censoring is handled by assigning constant baseline skill offsets:
  $$\text{Baseline\_Offset}_i = \begin{cases} 
  -10.0 & \text{for Student 3} \\
  -18.0 & \text{for Student 6} \\
  -3.0 & \text{for other Age 7 advanced starters}
  \end{cases}$$

---

## 3. Prior Knowledge Identification Engine (Post-Concert Filtered Detection)
For students entering with pre-existing skills, raw textbook progression rapidly saturates. The engine isolates true prior knowledge post-concert preparation windows by computing a continuous Welch's t-test and moving Z-score:

$$t_{\text{prior}} = \frac{\bar{X}_{\text{post}} - \bar{X}_{\text{pre}}}{\sqrt{\frac{s_{\text{post}}^2}{n_{\text{post}}} + \frac{s_{\text{pre}}^2}{n_{\text{pre}}}}}$$

When $p_{\text{prior}} < 0.05$, a fixed prior knowledge page bonus ($Prior\_Knowledge\_Bonus_i$) is detected and applied uniformly from Class 1 onward, preventing artificial skill spikes.

---

## 4. SPC Structural Break Engine (Multi-Concert Tracking States)
Concert preparation introduces structural breaks in learning dynamics. The SPC Engine monitors lesson points using rolling Welch's t-tests:

$$\text{SPC\_p\_value}_{i,t} = \text{Welch\_Test}(\text{Points}_{t-3:t}, \text{Points}_{t-6:t-3})$$

When $\text{SPC\_p\_value}_{i,t} < 0.05$, the system triggers a structural break:
1. **Entry Reset**: Captures $Base\_Asset\_Entry_{i,t} = \text{Actual\_Level}_{i,t-1}$ and resets cumulative performance window points $\text{Window\_Points}_{i,t} = 0.0$.
2. **Exit Capture**: Upon exiting prep, records exit page $P_{\text{exit}}$ and peak performance bonus $Peak\_Bonus_i$.

---

## 5. Recursive Performance Asset Engine
Skill accumulation during concert prep follows a Sigmoid Growth Model:

$$\text{Performance\_Bonus}_{i,t} = Base\_Asset\_Entry + \left(\frac{10.0}{1.0 + e^{-k \cdot \text{Window\_Points}_{i,t}}} - 5.0\right)$$

Outside performance prep, the bonus decays exponentially as a function of distance from the exit page $P_{\text{exit}}$:

$$\text{Performance\_Bonus}_{i,t} = Peak\_Bonus \cdot e^{-\delta \cdot \max(0, \text{Textbook}_{i,t} - P_{\text{exit}})}$$

where $k = 0.1133$ (sigmoid growth rate) and $\delta = 0.0886$ (page-distance decay rate).

---

## 6. Vacation & Absence Handling Engine
When lesson intervals exceed standard 1-week gaps (e.g., summer vacation or illness where $\Delta t > 1 \text{ week}$), skill rust accumulates via an exponential decay multiplier:

$$\text{Rust\_Multiplier}_{i,t} = e^{-\lambda \cdot (\Delta t - 1)}$$

where $\lambda = 0.0340$. The unobserved capability curve decays proportionally:

$$\text{Decayed\_Level}_{i,t} = \text{Actual\_Level}_{i,t-1} \cdot \text{Rust\_Multiplier}_{i,t}$$

---

## 7. Master State Fusion Equation
The master fused capability trajectory ($	heta_{i,t} = \text{Actual\_Level}_{i,t}$) combines textbook progression, technical defect penalties, performance assets, and rust multipliers into a unified equation:

$$\text{Actual\_Level}_{i,t} = \left[ \text{Textbook}_{i,t} + \mathbf{W}_p^T \mathbf{D}_{i,t} + \text{Performance\_Bonus}_{i,t} + \text{Prior\_Knowledge\_Bonus}_i \right] \cdot \text{Rust\_Multiplier}_{i,t} + \text{Baseline\_Offset}_i$$

where $\mathbf{W}_p$ is the vector of defect weights ($\mathcal{W}_p = -1.0027$).

---

## 8. Bayesian Optimization Framework (Optuna Parameter Estimation)
To estimate global hyperparameters without over-fitting, the pipeline employs a Bayesian Optimization framework powered by Optuna (Tree-structured Parzen Estimator, TPE). The objective function maximizes the log-likelihood of the state-space Kalman filter across all 14 student timelines:

$$\max_{k, \lambda, \delta, \mathcal{W}_p} \mathcal{L}(\mathbf{Y} \mid k, \lambda, \delta, \mathcal{W}_p) = -\frac{1}{2}\sum_{i=1}^{14}\sum_{t=1}^{T_i} \left[ \ln(2\pi F_{i,t}) + \frac{\epsilon_{i,t}^2}{F_{i,t}} \right]$$

### Optimized Global Hyperparameters:
* **$\mathcal{W}_p$ (Mastery Flaw Weight)**: `-1.0027`
* **$k$ (Sigmoid Growth Rate)**: `0.1133`
* **$\lambda$ (Absence Rust Decay)**: `0.0340`
* **$\delta$ (Post-Concert Decay Rate)**: `0.0886`
