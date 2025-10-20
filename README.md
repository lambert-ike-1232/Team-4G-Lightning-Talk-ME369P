# Control Library — Code Snippets for Slides

## Slide 1: Import & Setup

```python
import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# All control functions are accessed via the ctrl module
```

---

## Slide 2: Function #1 — `ctrl.tf()`

### Title: **Define Systems with Transfer Functions**

```python
# Define the PLANT (system to be controlled)
num = [1]           # Numerator coefficients
den = [1, 1, 0]     # Denominator coefficients
G = ctrl.tf(num, den)
# Result: G(s) = 1 / (s² + s)

# Define the PID CONTROLLER
Kp, Ki, Kd = 5.0, 2.0, 0.5
C = ctrl.tf([Kd, Kp, Ki], [1, 0])
# Result: C(s) = (0.5s² + 5s + 2) / s
```

### Explanation Box:
> **`ctrl.tf(numerator, denominator)`**
> 
> Creates a linear system from polynomial coefficients in the Laplace domain.
> - **numerator**: List of coefficients for the numerator polynomial
> - **denominator**: List of coefficients for the denominator polynomial
> 
> **Why?** Represents physical systems mathematically so we can analyze them.

---

## Slide 3: Function #2 — `ctrl.feedback()`

### Title: **Create Closed-Loop Feedback Systems**

```python
# Connect controller and plant into a closed-loop system
T = ctrl.feedback(C * G, 1)
# Result: T(s) = (C·G) / (1 + C·G)

# The "1" means unity feedback (output fed back directly)
# This is the standard feedback configuration
```

### Explanation Box:
> **`ctrl.feedback(system, feedback_gain)`**
> 
> Closes the feedback loop: output is compared to reference, error drives controller.
> - **system**: The open-loop system (controller × plant)
> - **feedback_gain**: Usually 1 for unity feedback
> 
> **Why?** Implements automatic error correction — the core of feedback control!

---

## Slide 4: Function #3 — `ctrl.forced_response()`

### Title: **Simulate System Response Over Time**

```python
# Create time vector and reference signal
t = np.linspace(0, 30, 3000)  # 30 seconds, 3000 points
r = np.ones_like(t)            # Step input (reference)

# Simulate the closed-loop system response
t_out, y_out = ctrl.forced_response(T, T=t, U=r)
# t_out: Time points where system was evaluated
# y_out: System output at each time point
```

### Explanation Box:
> **`ctrl.forced_response(system, T, U)`**
> 
> Simulates system response to a given input signal over time.
> - **system**: The closed-loop system to simulate
> - **T**: Time vector (when to evaluate)
> - **U**: Input signal (reference trajectory)
> 
> **Returns:** Time array and output array
> 
> **Why?** Lets you verify your controller works before deploying!

---

## Slide 5: Complete Example — Step Response

```python
import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

# 1. Define plant
G = ctrl.tf([1], [1, 1, 0])

# 2. Define PID controller
C = ctrl.tf([0.5, 5.0, 2.0], [1, 0])

# 3. Create closed-loop system
T = ctrl.feedback(C * G, 1)

# 4. Simulate response to step input
t = np.linspace(0, 30, 3000)
r = np.ones_like(t)  # Step reference
t_out, y_out = ctrl.forced_response(T, T=t, U=r)

# 5. Plot results
plt.plot(t, r, 'k--', label='Reference')
plt.plot(t_out, y_out, 'r-', label='Output')
plt.xlabel('Time [s]')
plt.ylabel('Response')
plt.legend()
plt.grid(True)
plt.show()
```

---

## Slide 6: Complete Example — Ramp Response

```python
# Same setup as before...
G = ctrl.tf([1], [1, 1, 0])
C = ctrl.tf([0.5, 5.0, 2.0], [1, 0])
T = ctrl.feedback(C * G, 1)

# Different input: RAMP instead of step
t = np.linspace(0, 30, 3000)
r = t * 1  # Ramp input (increases linearly)

# Simulate and plot
t_out, y_out = ctrl.forced_response(T, T=t, U=r)
plt.plot(t, r, 'k--', label='Reference (ramp)')
plt.plot(t_out, y_out, 'r-', label='Output')
plt.xlabel('Time [s]')
plt.ylabel('Response')
plt.legend()
plt.grid(True)
plt.show()
```

---

## Slide 7: Complete Example — Sinusoidal Response

```python
# Same setup as before...
G = ctrl.tf([1], [1, 1, 0])
C = ctrl.tf([0.5, 5.0, 2.0], [1, 0])
T = ctrl.feedback(C * G, 1)

# Different input: SINUSOID instead of step
t = np.linspace(0, 30, 3000)
r = 0.5 * np.sin(0.8 * t)  # Sinusoidal input

# Simulate and plot
t_out, y_out = ctrl.forced_response(T, T=t, U=r)
plt.plot(t, r, 'k--', label='Reference (sine)')
plt.plot(t_out, y_out, 'r-', label='Output')
plt.xlabel('Time [s]')
plt.ylabel('Response')
plt.legend()
plt.grid(True)
plt.show()
```

---

## Slide 8: Summary — The Three Functions

| Function | Purpose | Example |
|----------|---------|---------|
| **`ctrl.tf(num, den)`** | Define a system | `G = ctrl.tf([1], [1, 1, 0])` |
| **`ctrl.feedback(sys, H)`** | Create feedback loop | `T = ctrl.feedback(C * G, 1)` |
| **`ctrl.forced_response(sys, T, U)`** | Simulate over time | `t_out, y_out = ctrl.forced_response(T, T=t, U=r)` |

---

## Slide 9: Key Takeaway

```
┌─────────────────────────────────────────────────────┐
│  These 3 functions = Complete control workflow      │
│                                                     │
│  1. ctrl.tf()              → Build the system       │
│  2. ctrl.feedback()        → Add feedback control   │
│  3. ctrl.forced_response() → Test and verify        │
│                                                     │
│  That's all you need to simulate a PID controller!  │
└─────────────────────────────────────────────────────┘
```

