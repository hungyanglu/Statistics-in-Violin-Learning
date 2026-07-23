# Chapter 2: Diagnostic Human Learning Dimensions

The pipeline extracts six orthogonal diagnostic learning dimensions sequentially per student timeline to quantify latent psychometric behavior.

---

## 1. Learning Status (True Velocity State $v_{i,t}$)
* **Theoretical Foundation**: Dynamic Linear Modeling (DLM) & Kalman Filtering Theory.
* **Mathematical Execution**: Fit a discrete-time Local Linear Trend (LLT) state-space model onto the student's longitudinal $\text{Actual\_Level}_{i,t}$ curve. The state equation splits capability into level $\theta_{i,t}$ and velocity $v_{i,t}$:
  $$\begin{bmatrix} \theta_{i,t} \\ v_{i,t} \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} \theta_{i,t-1} \\ v_{i,t-1} \end{bmatrix} + \begin{bmatrix} w_{1,t} \\ w_{2,t} \end{bmatrix}, \quad \mathbf{w}_t \sim \mathcal{N}(\mathbf{0}, \mathbf{W})$$
* **Formula**: $\text{Learning\_Status}_{i,t} = v_{i,t}$
* **Pedagogical Meaning**: Represents true instantaneous skill velocity (pages/class), stripped of observation noise.

---

## 2. Stability (Prediction Error Volatility $\sigma_{w,i,t}$)
* **Theoretical Foundation**: Stochastic Volatility Modeling & Bayesian Predictive Error Analysis.
* **Mathematical Execution**: Compute the moving standard deviation of one-step-ahead prediction residuals $\epsilon_{i,t} = \text{Actual\_Level}_{i,t} - \hat{\mathbb{E}}[\text{Actual\_Level}_{i,t} \mid \mathbf{X}_{i,t-1}]$ over a rolling 3-week window:
* **Formula**:
  $$\text{Stability}_{i,t} = \sigma_{w, i, t} = \sqrt{\frac{1}{3}\sum_{\tau=t-2}^{t} \left(\epsilon_{i,\tau} - \bar{\epsilon}_{i,t}\right)^2}$$
* **Pedagogical Meaning**: Quantifies lesson-to-lesson preparation consistency. Low volatility indicates disciplined home preparation; high volatility signals erratic practice habits.

---

## 3. Talent (Gaussian Normalized Dynamic Capacity $\text{Talent}_{i,t}$)
* **Theoretical Foundation**: Latent Trait Psychometrics & Parametric Growth Curve Modeling.
* **Mathematical Execution**: Model talent as a dynamic parameter discovered chronologically over time. At step $t$, compute running intrinsic capacity $\Lambda_{i,t}$ based on cumulative defect resistivity:
  $$\Lambda_{i,t} = \gamma \cdot \left(1.0 - \frac{1}{t}\sum_{\tau=1}^{t} \text{Defect\_Density}_{i,\tau}\right)$$
  where $\text{Defect\_Density}_{i,\tau} = \frac{1}{18}\sum_{p=1}^{18} D_{i,\tau,p}$ and $\gamma = 0.2776$.
* **Population Z-Score Normalization**: To eliminate ceiling saturation and match downstream regression scales, normalize $\Lambda_{i,t}$ across active cohort observations at step $t$:
  $$\text{Talent}_{i,t} = \frac{\Lambda_{i,t} - \mu_{\mathbf{\Lambda}, t}}{\sigma_{\mathbf{\Lambda}, t}}$$
* **Pedagogical Meaning**: Tracks evolving technical defect resistance relative to peers, stabilizing onto a personal capacity anchor.

---

## 4. Teacher Influence (Causal Instruction Absorption Elasticity $\beta_{\text{teacher}}$)
* **Theoretical Foundation**: Instrumental Variable Causal Inference & Cross-Correlation Elasticity.
* **Mathematical Execution**: Compute the rolling regression slope ($\beta$) tracking co-movement between teacher instruction injections at $t-1$ (`special_points_lagged`) and defect corrections at $t$:
  $$\beta_{\text{teacher}, i, t} = \frac{\text{Cov}(\text{Defect\_Density}_{i,t}, \text{special\_points}_{i,t-1})}{\text{Var}(\text{special\_points}_{i,t-1}) + 1\times 10^{-6}}$$
  using a rolling 5-week window, normalized globally into Z-scores.
* **Pedagogical Meaning**: Measures how effectively a student absorbs and implements teacher corrections during home practice.

---

## 5. Effort (Latent Residual Drive $\Omega_{i,t}$)
* **Theoretical Foundation**: Structural Equation Modeling & Econometric Production Frontier Residuals.
* **Mathematical Execution**: Fit a cohort-wide expectation model mapping expected level change to Talent and teacher push:
  $$\hat{\Delta}\text{Actual\_Level}_{i,t} = \beta_1 \cdot \text{Talent}_{i,t} + \beta_2 \cdot \left(\text{Teacher\_Influence}_{i,t} \cdot \text{special\_points}_{i,t-1}\right)$$
* **Formula**:
  $$\text{Effort\_Raw}_{i,t} = \Delta\text{Actual\_Level}_{i,t} - \hat{\Delta}\text{Actual\_Level}_{i,t}$$
  normalized globally into standard Z-scores ($\Omega_{i,t}$).
* **Pedagogical Meaning**: Captures unobserved personal exertion and willpower exceeding baseline capacity expectations.

---

## 6. Efficiency (Quality-Adjusted Output ROI $\Theta_{i,t}$)
* **Theoretical Foundation**: Microeconomic Production Frontier Modeling & Resource Allocation Theory.
* **Mathematical Execution**: Model efficiency as output capability return per unit of exertion weighted by error saturation:
* **Formula**:
  $$\text{Efficiency\_Raw}_{i,t} = \frac{\max(0, \Delta\text{Actual\_Level}_{i,t})}{\max(0.1, \text{Effort\_Raw}_{i,t}) \cdot (1.0 + \text{Defect\_Density}_{i,t})}$$
  normalized globally into standard Z-scores ($\Theta_{i,t}$).
* **Pedagogical Meaning**: Quantifies practice quality. High efficiency indicates smart, focused practice; low efficiency indicates mindless, error-prone grinding.
