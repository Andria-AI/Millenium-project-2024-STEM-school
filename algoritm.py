import streamlit as st
import numpy as np

def adjust_air_properties(temperature, humidity):
    eta_g = 1.8e-5 * (1 + 0.002 * (temperature - 20))  # Adjusted air viscosity
    Rd = (4 + 0.02 * humidity + 0.05 * (25 - temperature)) * 1e-6  # Estimated droplet radius (m)
    return eta_g, Rd

def optimize_voltage_spacing(U0, Rd, Rc, eta_g):
    epsilon_0 = 8.85e-12  # F/m
    L = 0.02  # m

    best_config = {}
    best_Ke = 0

    for D_mm in np.arange(1, 10.5, 0.5):  # Spacing from 1 to 10 mm
        D = D_mm * 1e-3
        D_star = (D + 2 * Rc) / (2 * Rc)

        for V in np.linspace(7000, 15000, 100):
            q = 12 * np.pi * Rd**2 * epsilon_0 * V / L
            Uf = U0 + (2 * Rd * epsilon_0 / eta_g) * V**2 / L**2
            St = (2 * Rd**2 * 1000 * Uf) / (9 * eta_g * Rc)
            E = V / L
            Fe = q * E
            Fd = 6 * np.pi * eta_g * Rd * Uf
            Ke = Fe / Fd
            U_star = (2 * Rd * epsilon_0 * V**2) / (U0 * eta_g * L**2)

            if U_star < 1 and Ke > best_Ke:
                best_Ke = Ke
                best_config = {
                    "Optimal Wire Spacing (mm)": round(D_mm, 2),
                    "Optimal Voltage (V)": round(V, 2)
                }

    return best_config

st.title("⚡ Fog Collector Optimizer")
st.markdown("Environment-sensitive optimization for fog water collection using electrostatics.")

# Environmental inputs
temperature = st.slider("Air Temperature (°C)", -10, 50, 25)
humidity = st.slider("Relative Humidity (%)", 0, 100, 80)
U0 = st.slider("Wind Speed (m/s)", 0.1, 5.0, 1.0, 0.1)
uv_index = st.slider("UV Index (0-11+)", 0, 11, 5)

# Fixed mesh/wire setup
st.markdown("---")
st.subheader("Fixed Collector Design")
Rc = st.number_input("Wire Radius (mm) [Fixed]", value=0.8, step=0.1) * 1e-3

# Adjust air properties and droplet radius
eta_g, Rd = adjust_air_properties(temperature, humidity)

if st.button("Optimize Voltage & Spacing"):
    best = optimize_voltage_spacing(U0, Rd, Rc, eta_g)
    st.subheader("Best Configuration")
    st.write(best)
