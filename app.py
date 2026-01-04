import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- ENHANCED DATASET ---
# Added 'Z' (Atomic Number) to estimate scattering (Build-up)
MATERIALS = {
    "Tungsten-Polymer": {"density": 11.0, "mu_rho": 0.066, "Z": 74},
    "Borated Polyethylene": {"density": 0.95, "mu_rho": 0.082, "Z": 6},
    "Lead (Pure)": {"density": 11.34, "mu_rho": 0.071, "Z": 82},
    "Bismuth-Composite": {"density": 9.78, "mu_rho": 0.075, "Z": 83},
    "Standard Concrete": {"density": 2.35, "mu_rho": 0.064, "Z": 11}
}

st.set_page_config(page_title="ShieldPy Pro", layout="wide")

st.title(" ShieldPy: Advanced Shielding Simulator")
st.sidebar.header("Simulation Settings")

# --- IMPROVEMENT: BUILD-UP FACTOR TOGGLE ---
use_buildup = st.sidebar.checkbox("Account for Scattered Radiation (Build-up Factor)", value=True)
i_0 = st.sidebar.number_input("Initial Intensity ($I_0$)", value=1000.0)

num_layers = st.sidebar.slider("Number of Layers", 1, 5, 2)
layers = []
for i in range(num_layers):
    col_m, col_t = st.sidebar.columns(2)
    with col_m:
        mat = st.selectbox(f"Layer {i+1}", list(MATERIALS.keys()), key=f"m{i}")
    with col_t:
        thick = st.number_input(f"Thickness (cm)", 0.1, 50.0, 2.0, key=f"t{i}")
    layers.append({"name": mat, "thickness": thick})

# --- CALCULATION ENGINE ---
current_i = i_0
total_x = 0
plot_data = [{"x": 0, "y": i_0}]
results = []

for layer in layers:
    m = MATERIALS[layer['name']]
    mu = m['mu_rho'] * m['density']
    
    # Simple Build-up Approximation: B = 1 + (mu * x)
    # This accounts for photons that scatter but still reach the detector
    mfp = mu * layer['thickness'] # Mean Free Path
    B = (1 + mfp) if use_buildup else 1
    
    new_i = current_i * B * np.exp(-mfp)
    
    total_x += layer['thickness']
    plot_data.append({"x": total_x, "y": new_i})
    
    results.append({
        "Material": layer['name'],
        "HVL (cm)": round(np.log(2)/mu, 2),
        "Exit Intensity": round(new_i, 2),
        "Efficiency": f"{round((1 - new_i/current_i)*100, 1)}%"
    })
    current_i = new_i

# --- DASHBOARD LAYOUT ---
c1, c2 = st.columns([1, 1.2])

with c1:
    st.subheader("Shielding Analytics")
    st.dataframe(pd.DataFrame(results), use_container_width=True)
    st.metric("Final Transmitted Radiation", f"{round(current_i, 2)} units")
    
    # IMPROVEMENT: Engineering Alert
    if current_i > (0.01 * i_0):
        st.warning(" High transmission! Consider increasing thickness or adding high-Z layers.")
    else:
        st.success(" Effective Shielding: Radiation reduced by >99%")

with c2:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[p['x'] for p in plot_data], y=[p['y'] for p in plot_data], 
                             mode='lines+markers', fill='tozeroy', line_color='#ff4b4b'))
    fig.update_layout(title="Intensity Attenuation Profile", xaxis_title="Thickness (cm)", yaxis_title="Intensity")
    st.plotly_chart(fig, use_container_width=True)
