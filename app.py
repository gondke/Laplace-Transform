import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# App Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="s-Plane Navigator",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555555;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🕹️ s-Plane Navigator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive learning platform for Laplace Transforms, Complex Geometry, and Pole-Zero dynamics.</div><br>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar Navigation
# -----------------------------------------------------------------------------
st.sidebar.title("Navigation & Controls")
mode = st.sidebar.radio(
    "Choose Learning Module:",
    [
        "1. Interactive s-Plane & Time Domain",
        "2. Inverse Laplace Matching Quiz",
        "3. 3D Surface Plot of |H(s)|"
    ]
)

st.sidebar.divider()
st.sidebar.info("💡 **Tip:** Adjust parameters in Module 1 to see how pole movement directly dictates time-domain stability.")

# -----------------------------------------------------------------------------
# MODULE 1: Interactive s-Plane & Time Domain Signal
# -----------------------------------------------------------------------------
if mode == "1. Interactive s-Plane & Time Domain":
    st.subheader("Module 1: Pole Geometry on the Complex $s$-Plane ($s = \\sigma + j\\omega$)")
    st.write(
        "Observe how pole placement affects the attenuation factor ($\\sigma$) and natural frequency ($\\omega$) "
        "of the resulting time-domain signal $f(t) = e^{\\sigma t} \\cos(\\omega t)$."
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Controls")
        sigma = st.slider("Real Part (σ) - Controls Growth/Decay", -5.0, 5.0, -1.0, 0.1)
        omega = st.slider("Imaginary Part (ω) - Controls Oscillation Frequency", 0.0, 20.0, 5.0, 0.5)

        # Plot 2D Complex s-Plane
        fig_s = go.Figure()

        # Stability border (jω axis)
        fig_s.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="jω Boundary")
        fig_s.add_hline(y=0, line_dash="dash", line_color="gray")

        # Conjugate Poles
        fig_s.add_trace(go.Scatter(
            x=[sigma, sigma],
            y=[omega, -omega],
            mode='markers+text',
            marker=dict(symbol='x', size=14, color='red', line=dict(width=3)),
            text=["Pole 1 (σ + jω)", "Pole 2 (σ - jω)"],
            textposition="top right",
            name="Poles"
        ))

        fig_s.update_layout(
            title="Complex s-Plane",
            xaxis_title="Real Axis (σ)",
            yaxis_title="Imaginary Axis (jω)",
            xaxis=dict(range=[-6, 6]),
            yaxis=dict(range=[-22, 22]),
            height=400
        )
        st.plotly_chart(fig_s, use_container_width=True)

    with col2:
        st.markdown("### Generated Time Signal $f(t)$")
        t = np.linspace(0, 5, 600)
        f_t = np.exp(sigma * t) * np.cos(omega * t)

        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(
            x=t,
            y=f_t,
            mode='lines',
            name='f(t)',
            line=dict(color='#1f77b4', width=2.5)
        ))

        y_max = max(2.0, np.max(np.abs(f_t))) if sigma <= 0 else np.max(np.abs(f_t))
        fig_t.update_layout(
            title="Time-Domain Response: $f(t) = e^{\\sigma t} \\cos(\\omega t)$",
            xaxis_title="Time (t in seconds)",
            yaxis_title="Amplitude f(t)",
            yaxis=dict(range=[-y_max, y_max]),
            height=400
        )
        st.plotly_chart(fig_t, use_container_width=True)

    # System Diagnostics
    if sigma > 0:
        st.error("⚠️ **Unstable System:** Poles lie in the Right-Half Plane (RHP). The time signal exponentially diverges to $\\infty$.")
    elif sigma == 0:
        st.warning("🔴 **Marginally Stable System:** Poles lie on the $j\\omega$-axis. The signal oscillates continuously without decaying.")
    else:
        st.success("✅ **Stable System:** Poles lie in the Left-Half Plane (LHP). The signal exponentially decays to 0.")

# -----------------------------------------------------------------------------
# MODULE 2: Inverse Laplace Matching Quiz
# -----------------------------------------------------------------------------
elif mode == "2. Inverse Laplace Matching Quiz":
    st.subheader("Module 2: Inverse Laplace Transform Practice")
    st.write("Match the Laplace Domain function $F(s)$ to its corresponding Time-Domain function $f(t) = \\mathcal{L}^{-1}\\{F(s)\\}$.")

    questions = [
        {
            "F_s": "\\frac{s}{s^2 + 16}",
            "options": ["cos(4t)", "sin(4t)", "e^{-4t}", "t cos(4t)"],
            "correct": "cos(4t)",
            "explanation": "\\mathcal{L}\\{\\cos(\\omega t)\\} = \\frac{s}{s^2 + \\omega^2}. \\text{ Here, } \\omega = 4."
        },
        {
            "F_s": "\\frac{5}{s + 2}",
            "options": ["5 e^{2t}", "5 e^{-2t}", "5 \\sin(2t)", "\\frac{5}{2}t"],
            "correct": "5 e^{-2t}",
            "explanation": "\\mathcal{L}\\{e^{-at}\\} = \\frac{1}{s + a}. \\text{ Multiplying by constant 5 gives } 5e^{-2t}."
        },
        {
            "F_s": "\\frac{4}{(s + 3)^2 + 16}",
            "options": ["e^{-3t}\\sin(4t)", "e^{3t}\\cos(4t)", "e^{-3t}\\cos(4t)", "\\sin(4t)"],
            "correct": "e^{-3t}\\sin(4t)",
            "explanation": "Using the First Frequency Shift Theorem: \\mathcal{L}\\{e^{-at}\\sin(\\omega t)\\} = \\frac{\\omega}{(s+a)^2 + \\omega^2}."
        }
    ]

    for idx, q in enumerate(questions):
        st.markdown(f"#### Question {idx+1}:")
        st.latex(f"F(s) = {q['F_s']}")
        
        user_choice = st.radio(
            f"Select $f(t)$ for Q{idx+1}:", 
            q["options"], 
            key=f"q_{idx}"
        )

        if st.button(f"Verify Answer Q{idx+1}", key=f"btn_{idx}"):
            if user_choice == q["correct"]:
                st.success("🎉 Correct!")
            else:
                st.error(f"❌ Incorrect. The correct answer is **{q['correct']}**.")
            
            st.latex(f"\\text{{Step-by-step: }} {q['explanation']}")
        st.divider()

# -----------------------------------------------------------------------------
# MODULE 3: 3D Surface Plot of |H(s)|
# -----------------------------------------------------------------------------
elif mode == "3. 3D Surface Plot of |H(s)|":
    st.subheader("Module 3: 3D Transfer Function Magnitude Surface $|H(s)|$")
    st.write(
        "Visualize the magnitude response $|H(s)|$ of a second-order system "
        "$H(s) = \\frac{1}{s^2 + 2\\zeta\\omega_n s + \\omega_n^2}$ mapped across the entire complex $s$-plane."
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        zeta = st.slider("Damping Ratio (ζ)", 0.05, 1.5, 0.2, 0.05)
        wn = st.slider("Natural Frequency (ω_n)", 1.0, 10.0, 3.0, 0.5)

    # Grid evaluation
    sigma_vals = np.linspace(-4, 2, 100)
    omega_vals = np.linspace(-10, 10, 100)
    Sigma, Omega = np.meshgrid(sigma_vals, omega_vals)

    # Complex s
    S = Sigma + 1j * Omega
    
    # Transfer Function H(s)
    H_s = 1.0 / (S**2 + 2 * zeta * wn * S + wn**2)
    Magnitude = np.abs(H_s)
    
    # Cap magnitude for clear visualization
    Magnitude = np.clip(Magnitude, 0, 10)

    fig_3d = go.Figure(data=[go.Surface(
        z=Magnitude,
        x=Sigma,
        y=Omega,
        colorscale='Viridis',
        colorbar_title='|H(s)|'
    )])

    fig_3d.update_layout(
        title="Surface Topology of |H(s)| (Poles appear as infinite peaks)",
        scene=dict(
            xaxis_title='Real Axis (σ)',
            yaxis_title='Imaginary Axis (jω)',
            zaxis_title='Magnitude |H(s)|'
        ),
        height=600
    )

    st.plotly_chart(fig_3d, use_container_width=True)
