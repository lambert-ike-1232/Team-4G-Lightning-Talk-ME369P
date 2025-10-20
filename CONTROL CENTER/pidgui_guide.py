"""
Complete PID Controller Simulator
Demonstrates the Python Control Systems Library (control package)
Shows how ctrl.tf(), ctrl.feedback(), and ctrl.forced_response() work together
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# --- Define the reference profile ---
ref_profile = {
    0: 1.0,
    3: 0.5,
    6: 1.5,
    10: -0.5,
    15: 2.0,
    20: -3,
    25: 0 
}

# --- Simulation function for STEP response ---
def simulate_pid_step(Kp, Ki, Kd):
    # Step 1: Define the plant using ctrl.tf()
    # ctrl.tf() creates a transfer function from numerator and denominator coefficients
    # This represents the plant (system to be controlled) in the Laplace domain
    # G(s) = 1 / (s² + s)
    num = [1]
    den = [1, 1, 0]
    G = ctrl.tf(num, den)
    Ctype = "step"
    
    # Step 2: Define the PID controller using ctrl.tf()
    # ctrl.tf() creates the PID controller transfer function
    # C(s) = (Kd·s² + Kp·s + Ki) / s
    C = ctrl.tf([Kd, Kp, Ki], [1, 0])
    
    # Step 3: Create closed-loop system using ctrl.feedback()
    # ctrl.feedback() connects the controller and plant into a closed-loop system
    # It implements: T(s) = (C·G) / (1 + C·G)
    # The "1" means unity feedback (output is fed back directly to compare with reference)
    # This creates the feedback loop where errors are automatically corrected
    T = ctrl.feedback(C * G, 1)
    
    # Create time vector and reference signal
    t_end = 30
    t = np.linspace(0, t_end, 3000)
    r = np.zeros_like(t)
    
    # Build the step reference profile
    crnt_key = 0
    counter = 0
    for val in t:
        for item in ref_profile:
            if val > item:
                crnt_key = item
        r[counter] = ref_profile[crnt_key]
        counter += 1

    # Step 4: Simulate system response using ctrl.forced_response()
    # ctrl.forced_response() simulates how the closed-loop system responds over time
    # Parameters:
    #   T: the closed-loop system (from ctrl.feedback)
    #   T: time vector (when to evaluate the response)
    #   U: input signal (the reference trajectory we want to track)
    # Returns:
    #   t_out: time points where the system was evaluated
    #   y_out: the system's output at each time point
    t_out, y_out = ctrl.forced_response(T, T=t, U=r)

    # Plot the result
    plt.figure(figsize=(9, 5))
    plt.plot(t, r, 'k--', linewidth=2, label='Reference (r)')
    plt.plot(t_out, y_out, linewidth=2, label='Output (y)', color="red")
    plt.title(f'PID Control Response to {Ctype}\nKp={Kp}, Ki={Ki}, Kd={Kd}', fontsize=12)
    plt.xlabel('Time [s]')
    plt.ylabel('Response')
    plt.grid(True, alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()

# --- Simulation function for RAMP response ---
def simulate_pid_ramp(Kp, Ki, Kd):
    Ctype = "ramp"
    
    # Step 1: Define the plant using ctrl.tf()
    num = [1]
    den = [1, 1, 0]
    G = ctrl.tf(num, den)
    
    # Step 2: Define the PID controller using ctrl.tf()
    C = ctrl.tf([Kd, Kp, Ki], [1, 0])
    
    # Step 3: Create closed-loop system using ctrl.feedback()
    T = ctrl.feedback(C * G, 1)
    
    # Create time vector and ramp reference signal
    t_end = 30
    t = np.linspace(0, t_end, 3000)
    r = t * 1  # Ramp input (linearly increasing)

    # Step 4: Simulate system response using ctrl.forced_response()
    t_out, y_out = ctrl.forced_response(T, T=t, U=r)

    # Plot the result
    plt.figure(figsize=(9, 5))
    plt.plot(t, r, 'k--', linewidth=2, label='Reference (r)')
    plt.plot(t_out, y_out, linewidth=2, label='Output (y)', color="red")
    plt.title(f'PID Control Response to {Ctype}\nKp={Kp}, Ki={Ki}, Kd={Kd}', fontsize=12)
    plt.xlabel('Time [s]')
    plt.ylabel('Response')
    plt.grid(True, alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
# --- Simulation function for SINUSOIDAL response ---
def simulate_pid_sin(Kp, Ki, Kd):
    Ctype = "sin"
    
    # Step 1: Define the plant using ctrl.tf()
    num = [1]
    den = [1, 1, 0]
    G = ctrl.tf(num, den)
    
    # Step 2: Define the PID controller using ctrl.tf()
    C = ctrl.tf([Kd, Kp, Ki], [1, 0])
    
    # Step 3: Create closed-loop system using ctrl.feedback()
    T = ctrl.feedback(C * G, 1)
    
    # Create time vector and sinusoidal reference signal
    t_end = 30
    t = np.linspace(0, t_end, 3000)
    r = 0.5 * np.sin(0.8 * t)  # Sinusoidal input

    # Step 4: Simulate system response using ctrl.forced_response()
    t_out, y_out = ctrl.forced_response(T, T=t, U=r)

    # Plot the result
    plt.figure(figsize=(9, 5))
    plt.plot(t, r, 'k--', linewidth=2, label='Reference (r)')
    plt.plot(t_out, y_out, linewidth=2, label='Output (y)', color="red")
    plt.title(f'PID Control Response to {Ctype}\nKp={Kp}, Ki={Ki}, Kd={Kd}', fontsize=12)
    plt.xlabel('Time [s]')
    plt.ylabel('Response')
    plt.grid(True, alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()

# --- GUI setup ---
root = tk.Tk()
root.title("PID Controller Simulator")
root.geometry("300x300")
root.resizable(False, False)
root.configure(bg="#222")

title = tk.Label(
    root, 
    text="PID Control Simulator", 
    font=("Arial", 14, "bold"), 
    fg="white", 
    bg="#222"
)
title.pack(pady=10)

# --- Input fields ---
frame = tk.Frame(root, bg="#222")
frame.pack(pady=5)

# Kp
kp_label = tk.Label(frame, text="Kp:", fg="#4ECDC4", bg="#222", font=("Arial", 12, "bold"))
kp_label.grid(row=0, column=0, padx=10, pady=5)
kp_entry = ttk.Entry(frame, width=10)
kp_entry.insert(0, "5.0")
kp_entry.grid(row=0, column=1, pady=5)

# Ki
ki_label = tk.Label(frame, text="Ki:", fg="#F5C518", bg="#222", font=("Arial", 12, "bold"))
ki_label.grid(row=1, column=0, padx=10, pady=5)
ki_entry = ttk.Entry(frame, width=10)
ki_entry.insert(0, "2.0")
ki_entry.grid(row=1, column=1, pady=5)

# Kd
kd_label = tk.Label(frame, text="Kd:", fg="#FF6B6B", bg="#222", font=("Arial", 12, "bold"))
kd_label.grid(row=2, column=0, padx=10, pady=5)
kd_entry = ttk.Entry(frame, width=10)
kd_entry.insert(0, "0.5")
kd_entry.grid(row=2, column=1, pady=5)

# --- Input Type Selection ---
input_type_label = tk.Label(
    frame, 
    text="Input Type:", 
    fg="#1E90FF", 
    bg="#222", 
    font=("Arial", 12, "bold")
)
input_type_label.grid(row=3, column=0, padx=10, pady=10)

input_type = tk.StringVar(value="Step")

input_dropdown = ttk.Combobox(
    frame,
    textvariable=input_type,
    values=["Step", "Ramp", "Sinusoidal"],
    state="readonly",
    width=9
)
input_dropdown.grid(row=3, column=1, pady=10)

# --- Generate Button ---
def on_generate():
    try:
        Kp = float(kp_entry.get())
        Ki = float(ki_entry.get())
        Kd = float(kd_entry.get())
        if input_type.get().lower() == "step":  
            simulate_pid_step(Kp, Ki, Kd)
        elif input_type.get().lower() == "ramp":
            simulate_pid_ramp(Kp, Ki, Kd)
        elif input_type.get().lower() == "sinusoidal":
            simulate_pid_sin(Kp, Ki, Kd)
    except ValueError:
        tk.messagebox.showerror("Input Error", "Please enter valid numeric values for Kp, Ki, and Kd.")

generate_button = tk.Button(root, text="Generate Plot", bg="#28a745", fg="white",
                            font=("Arial", 12, "bold"), relief="raised",
                            activebackground="#218838", activeforeground="white",
                            command=on_generate)
generate_button.pack(pady=20, ipadx=10, ipady=4)

root.mainloop()

