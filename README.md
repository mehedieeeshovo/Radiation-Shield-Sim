# ShieldPy: Multilayer Radiation Attenuation Simulator

A high-fidelity engineering simulation tool built in Python to evaluate the shielding effectiveness of advanced composite materials against Gamma radiation.

##  Overview
ShieldPy allows engineers to model multilayered shields using high-attenuability composites. Unlike basic calculators, this tool accounts for **Compton Scattering** via Build-up factors and provides industry-standard metrics like HVL and TVL.

##  Key Features
* **Multilayer Modeling:** Configure up to 5 layers of custom materials (Tungsten-Polymer, Borated Polyethylene, etc.).
* **Physics Engine:** Implements the Beer-Lambert Law: $I = I_0 \cdot B \cdot e^{-\mu x}$.
* **Engineering Metrics:** Calculates **Half-Value Layer (HVL)** and **Tenth-Value Layer (TVL)** for every material.
* **Interactive Visualization:** Real-time decay curves and shielding efficiency percentages.
* **Mass Analysis:** Provides area-density calculations ($g/cm^2$) for weight-sensitive applications (aerospace/medical).

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Interface:** [Streamlit](https://streamlit.io/)
* **Data Analysis:** Pandas, NumPy
* **Visuals:** Plotly Interactive Graphs

## 📖 How to Run Locally
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/ShieldPy.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the app: `streamlit run app.py`

---
*Developed for education purpose in Nuclear Engineering and Radiation Protection analysis.*
