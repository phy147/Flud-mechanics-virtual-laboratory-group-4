import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from gtts import gTTS
import os

# --- Helper Functions ---
def generate_audio(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

def plot_velocity_graph(velocity_range, pressure_diff):
    fig, ax = plt.subplots()
    ax.plot(velocity_range, pressure_diff, color='blue', linewidth=2)
    ax.set_xlabel("Velocity (m/s)")
    ax.set_ylabel("Pressure Difference (Pa)")
    ax.set_title("Velocity vs Pressure Difference")
    st.pyplot(fig)

def show_table(data_dict):
    st.table(data_dict)

# --- Module: Pitot Tube ---
def pitot_tube_module():
    st.subheader("Pitot Tube Flow Measurement")

    rho = st.slider("Fluid Density (kg/m³)", 800, 1200, 1000)
    pressure_diff = st.slider("Pressure Difference (Pa)", 0, 1000, 100)

    velocity = (2 * pressure_diff / rho) ** 0.5
    st.success(f"Calculated Velocity: {velocity:.2f} m/s")

    # Table
    show_table({
        "Fluid Density (kg/m³)": rho,
        "Pressure Difference (Pa)": pressure_diff,
        "Velocity (m/s)": f"{velocity:.2f}"
    })

    # Graph
    v_range = np.linspace(0.1, 10, 50)
    p_diff_range = 0.5 * rho * v_range**2
    plot_velocity_graph(v_range, p_diff_range)

    # Narration
    if st.checkbox("Enable Narration"):
        narration = f"With a fluid density of {rho} and pressure difference of {pressure_diff}, the calculated velocity is {velocity:.2f} meters per second."
        audio_file = generate_audio(narration, "pitot.mp3")
        st.audio(audio_file, format='audio/mp3')

# --- Module: Reynolds Number Visualization ---
def reynolds_module():
    st.subheader("Reynolds Number Flow Visualization")

    rho = st.slider("Fluid Density (kg/m³)", 800, 1200, 1000)
    velocity = st.slider("Velocity (m/s)", 0, 10, 1)
    diameter = st.slider("Pipe Diameter (m)", 0.01, 0.1, 0.05)
    mu = st.slider("Dynamic Viscosity (Pa·s)", 0.001, 0.01, 0.001)

    reynolds = (rho * velocity * diameter) / mu

    if reynolds < 2300:
        flow_type = "Laminar"
        color = "green"
    elif reynolds < 4000:
        flow_type = "Transitional"
        color = "orange"
    else:
        flow_type = "Turbulent"
        color = "red"

    st.success(f"Reynolds Number: {reynolds:.0f} — Flow is {flow_type}")

    # Table
    show_table({
        "Density (kg/m³)": rho,
        "Velocity (m/s)": velocity,
        "Diameter (m)": diameter,
        "Viscosity (Pa·s)": mu,
        "Reynolds Number": f"{reynolds:.0f}",
        "Flow Type": flow_type
    })

    # Visualization (Bar chart like color block)
    fig, ax = plt.subplots()
    ax.barh(["Flow Type"], [1], color=color)
    ax.set_xlim([0, 1])
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title(f"Flow Type: {flow_type}")
    st.pyplot(fig)

    # Narration
    if st.checkbox("Enable Narration"):
        narration = f"With velocity {velocity} meters per second and viscosity {mu}, the Reynolds number is {reynolds:.0f}. This indicates {flow_type} flow."
        audio_file = generate_audio(narration, "reynolds.mp3")
        st.audio(audio_file, format='audio/mp3')

# --- Main App ---
st.title("Virtual Fluid Mechanics Lab")
module = st.radio("Choose an Experiment:", ("Pitot Tube Flow Measurement", "Reynolds Number Flow Visualization"))

if module == "Pitot Tube Flow Measurement":
    pitot_tube_module()
elif module == "Reynolds Number Flow Visualization":
    reynolds_module()
