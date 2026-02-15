import streamlit as st
import base64
from repair_shops_data import repair_page, ewaste_page
import streamlit.components.v1 as components
import html as html_module
import requests
import time

st.set_page_config(
    page_title="Green Device Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ════════════════════════════════════════════════════════════
# ═══════════════════ GLOBAL STYLES ═════════════════════════
# ════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap');

/* ── Reset & Base ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] { background: transparent !important; height: 0 !important; }

html, body, [class*="css"], .stMarkdown, .stButton > button, input, textarea, select, label, p, span, div {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background: #f8fdf9 !important;
}

section.main > div {
    background: transparent !important;
}

.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem;
    max-width: 100% !important;
}

/* ── Global Button Styling ── */
.stButton > button {
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    font-size: 0.88rem;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1.5px solid #16a34a;
    background: linear-gradient(135deg, #16a34a, #22c55e);
    color: white;
    letter-spacing: -0.01em;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(22, 163, 74, 0.3);
    background: linear-gradient(135deg, #15803d, #16a34a);
}

/* ── Text Input Styling ── */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #d1d5db !important;
    padding: 0.7rem 1rem !important;
    font-size: 0.9rem !important;
    background: #ffffff !important;
    transition: all 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.12) !important;
}

/* ── Number Input Styling ── */
.stNumberInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #d1d5db !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #c6ecd0; border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: #86dba0; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"


def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ════════════════════════════════════════════════════════════
# ═══════════════════ HOME PAGE ═════════════════════════════
# ════════════════════════════════════════════════════════════
if st.session_state.page == "home":

    try:
        image_base64 = get_base64_image("del.jpg")
        hero_bg = f"url('data:image/jpeg;base64,{image_base64}') center/cover no-repeat"
    except Exception:
        hero_bg = "linear-gradient(135deg, #052e16 0%, #064e3b 35%, #047857 65%, #059669 100%)"

    st.markdown(f"""
    <style>
    .stApp {{
        background: #f0faf3 !important;
    }}

    /* ── Floating Navbar ── */
    .nav-wrapper {{
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 99999;
        padding: 0.7rem 2rem;
        background: rgba(255,255,255,0.88);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-bottom: 1px solid rgba(22, 163, 74, 0.08);
        transition: all 0.3s ease;
    }}
    .nav-inner {{
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .nav-brand {{
        display: flex;
        align-items: center;
        gap: 0.55rem;
        font-weight: 800;
        font-size: 1.05rem;
        color: #064e3b;
        letter-spacing: -0.025em;
    }}
    .nav-brand-icon {{
        width: 34px; height: 34px;
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }}
    .nav-links {{
        display: flex;
        align-items: center;
        gap: 2.2rem;
    }}
    .nav-links a {{
        font-size: 0.85rem;
        font-weight: 600;
        color: #475569;
        text-decoration: none;
        transition: color 0.2s;
        position: relative;
    }}
    .nav-links a::after {{
        content: '';
        position: absolute;
        bottom: -4px; left: 0;
        width: 0; height: 2px;
        background: #10b981;
        border-radius: 2px;
        transition: width 0.25s ease;
    }}
    .nav-links a:hover {{ color: #059669; }}
    .nav-links a:hover::after {{ width: 100%; }}

    /* ── Hero Section ── */
    .hero {{
        position: relative;
        width: 100%;
        min-height: 94vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: {hero_bg};
        overflow: hidden;
    }}
    .hero::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(
            170deg,
            rgba(2,46,22,0.7) 0%,
            rgba(4,78,59,0.55) 40%,
            rgba(5,150,105,0.45) 100%
        );
        z-index: 1;
    }}
    /* Subtle animated gradient orbs */
    .hero::after {{
        content: "";
        position: absolute;
        top: -20%; right: -15%;
        width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(52,211,153,0.15), transparent 70%);
        border-radius: 50%;
        z-index: 1;
        animation: hero-float 8s ease-in-out infinite;
    }}
    @keyframes hero-float {{
        0%, 100% {{ transform: translate(0, 0); }}
        50% {{ transform: translate(-30px, 20px); }}
    }}

    .hero-content {{
        position: relative;
        z-index: 2;
        text-align: center;
        max-width: 780px;
        padding: 2rem;
    }}
    .hero-pill {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 100px;
        padding: 0.4rem 1.1rem;
        font-size: 0.78rem;
        font-weight: 600;
        color: #bbf7d0;
        margin-bottom: 2rem;
        letter-spacing: 0.04em;
    }}
    .hero-pill .dot {{
        width: 7px; height: 7px;
        background: #4ade80;
        border-radius: 50%;
        animation: pulse-dot 2s ease-in-out infinite;
    }}
    @keyframes pulse-dot {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(1.6); }}
    }}

    .hero h1 {{
        font-size: 3.8rem;
        font-weight: 900;
        color: #ffffff;
        line-height: 1.06;
        letter-spacing: -0.035em;
        margin: 0 0 1.2rem 0;
    }}
    .hero h1 .accent {{
        background: linear-gradient(135deg, #6ee7b7, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .hero-desc {{
        font-size: 1.1rem;
        color: rgba(255,255,255,0.75);
        line-height: 1.75;
        max-width: 560px;
        margin: 0 auto 2.5rem auto;
    }}

    /* ── Stats Strip ── */
    .hero-stats {{
        display: flex;
        justify-content: center;
        gap: 3.5rem;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }}
    .hero-stat {{ text-align: center; }}
    .hero-stat-num {{
        font-size: 1.6rem;
        font-weight: 800;
        color: #6ee7b7;
        letter-spacing: -0.02em;
    }}
    .hero-stat-lbl {{
        font-size: 0.72rem;
        font-weight: 500;
        color: rgba(255,255,255,0.45);
        margin-top: 0.15rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}

    /* ── Scroll Indicator ── */
    .scroll-hint {{
        position: absolute;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 3;
        text-align: center;
    }}
    .scroll-hint .mouse {{
        display: block;
        width: 22px; height: 36px;
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 11px;
        margin: 0 auto 0.4rem;
        position: relative;
    }}
    .scroll-hint .mouse::after {{
        content: '';
        width: 3px; height: 7px;
        background: rgba(255,255,255,0.5);
        border-radius: 2px;
        position: absolute;
        top: 6px; left: 50%;
        transform: translateX(-50%);
        animation: scroll-bob 1.6s ease-in-out infinite;
    }}
    @keyframes scroll-bob {{
        0%   {{ top: 6px; opacity: 1; }}
        50%  {{ top: 16px; opacity: 0.2; }}
        100% {{ top: 6px; opacity: 1; }}
    }}
    .scroll-hint p {{
        font-size: 0.65rem;
        font-weight: 600;
        color: rgba(255,255,255,0.3);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin: 0;
    }}

    /* ── Content Sections ── */
    .content-section {{
        max-width: 1100px;
        margin: 0 auto;
        padding: 5rem 2rem;
    }}
    .section-eyebrow {{
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        color: #059669;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        background: #ecfdf5;
        padding: 0.3rem 0.9rem;
        border-radius: 100px;
        margin-bottom: 0.75rem;
        border: 1px solid #d1fae5;
    }}
    .section-heading {{
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.03em;
        margin: 0.4rem 0 0.5rem;
        line-height: 1.2;
    }}
    .section-sub {{
        font-size: 1rem;
        color: #64748b;
        max-width: 520px;
        line-height: 1.65;
    }}
    .section-header {{
        text-align: center;
        margin-bottom: 3rem;
    }}
    .section-header .section-sub {{
        margin: 0.5rem auto 0;
    }}

    /* ── Feature Cards Grid ── */
    .features-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.25rem;
    }}
    .feature-card {{
        background: #ffffff;
        border-radius: 16px;
        padding: 2rem 1.6rem;
        border: 1px solid #e8f5e9;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    .feature-card::after {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10b981, #6ee7b7);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 16px 40px rgba(5, 150, 105, 0.1);
        border-color: #a7f3d0;
    }}
    .feature-card:hover::after {{ opacity: 1; }}
    .feature-icon-wrap {{
        width: 52px; height: 52px;
        border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem;
        margin-bottom: 1.1rem;
    }}
    .feature-icon-wrap.fc-green {{ background: #dcfce7; }}
    .feature-icon-wrap.fc-blue {{ background: #dbeafe; }}
    .feature-icon-wrap.fc-amber {{ background: #fef3c7; }}
    .feature-card h3 {{
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 0.5rem;
        letter-spacing: -0.01em;
    }}
    .feature-card p {{
        font-size: 0.88rem;
        color: #64748b;
        line-height: 1.6;
        margin: 0;
    }}

    /* ── CTA Banner ── */
    .cta-banner {{
        background: linear-gradient(135deg, #052e16 0%, #064e3b 40%, #047857 100%);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 2rem;
        max-width: 1100px;
        margin: 0 auto 3rem;
        position: relative;
        overflow: hidden;
    }}
    .cta-banner::before {{
        content: '';
        position: absolute;
        top: -60%; right: -5%;
        width: 350px; height: 350px;
        background: radial-gradient(circle, rgba(110,231,183,0.12), transparent 70%);
        border-radius: 50%;
    }}
    .cta-banner::after {{
        content: '';
        position: absolute;
        bottom: -40%; left: 10%;
        width: 250px; height: 250px;
        background: radial-gradient(circle, rgba(52,211,153,0.08), transparent 70%);
        border-radius: 50%;
    }}
    .cta-text {{ position: relative; z-index: 2; flex: 1; }}
    .cta-text h2 {{
        font-size: 1.65rem;
        font-weight: 800;
        color: white;
        margin: 0 0 0.4rem;
        letter-spacing: -0.02em;
    }}
    .cta-text p {{
        font-size: 0.95rem;
        color: rgba(255,255,255,0.7);
        margin: 0;
        line-height: 1.6;
    }}

    /* ── Footer ── */
    .site-footer {{
        text-align: center;
        padding: 2rem;
        font-size: 0.8rem;
        color: #94a3b8;
        border-top: 1px solid #e2e8f0;
        max-width: 1100px;
        margin: 0 auto;
    }}

    /* ── Auth Buttons Area ── */
    .auth-section {{
        text-align: center;
        padding: 3rem 2rem 1rem;
    }}
    .auth-section h2 {{
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0 0 0.3rem;
        letter-spacing: -0.02em;
    }}
    .auth-section p {{
        color: #64748b;
        font-size: 0.95rem;
    }}

    /* ── Responsive ── */
    @media (max-width: 900px) {{
        .hero h1 {{ font-size: 2.5rem; }}
        .features-grid {{ grid-template-columns: 1fr; }}
        .cta-banner {{ flex-direction: column; text-align: center; padding: 2rem 1.5rem; }}
        .hero-stats {{ gap: 1.5rem; }}
        .nav-wrapper {{ padding: 0.6rem 1rem; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    # ── Navbar ──
    st.markdown("""
    <div class="nav-wrapper">
        <div class="nav-inner">
            <div class="nav-brand">
                <div class="nav-brand-icon">🌱</div>
                Green Device Intelligence
            </div>
            <div class="nav-links">
                <a href="#features">Features</a>
                <a href="#services">Services</a>
                <a href="#about">About</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero Section ──
    st.markdown(f"""
    <div class="hero">
        <div class="hero-content">
            <h1>Make Your Tech<br><span class="accent">Greener & Smarter</span></h1>
            <div class="hero-desc">
                Track your device's environmental impact, find eco-friendly repair shops,
                and join the movement towards sustainable technology.
            </div>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="hero-stat-num">2.4K+</div>
                    <div class="hero-stat-lbl">Devices Tracked</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-num">180+</div>
                    <div class="hero-stat-lbl">Repair Partners</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-num">12T</div>
                    <div class="hero-stat-lbl">CO₂ Saved</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-num">98%</div>
                    <div class="hero-stat-lbl">Satisfaction</div>
                </div>
            </div>
        </div>
        <div class="scroll-hint">
            <span class="mouse"></span>
            <p>Scroll</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Auth Buttons ──
    st.markdown("""
    <div class="auth-section">
        <h2>Sustainability Starts Here!</h2>
        <p>Sign in to track your device health and eco impact</p>
    </div>
    """, unsafe_allow_html=True)

    col_spacer1, col_login, col_signup, col_spacer2 = st.columns([3, 1.5, 1.5, 3])
    with col_login:
        if st.button("🔐  Login", use_container_width=True, key="home_login"):
            st.session_state.page = "login"
            st.rerun()
    with col_signup:
        if st.button("✨  Sign Up", use_container_width=True, key="home_signup"):
            st.write("Not available yet")

    # ── Features Section ──
    st.markdown("""
    <div class="content-section" id="features">
        <div class="section-header">
            <div class="section-eyebrow">Why Choose Us</div>
            <div class="section-heading">Everything You Need for<br>Sustainable Tech</div>
            <div class="section-sub">
                From real-time device monitoring to eco-friendly repair options —
                we provide the tools to reduce your digital carbon footprint.
            </div>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon-wrap fc-green">📊</div>
                <h3>Device Health Monitoring</h3>
                <p>Track CPU usage, RAM performance, battery temperature, and eco scores in real-time with beautiful dashboards.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon-wrap fc-blue">🛠️</div>
                <h3>Eco-Friendly Repairs</h3>
                <p>Find verified local repair shops that prioritize sustainability. Extend your device lifespan instead of replacing.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon-wrap fc-amber">♻️</div>
                <h3>E-Waste Management</h3>
                <p>Locate certified e-waste recycling centres near you. Dispose of old electronics responsibly and safely.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA Banner ──
    st.markdown("""
    <div class="cta-banner" id="services">
        <div class="cta-text">
            <h2>Ready to Explore Our Services?</h2>
            <p>Find repair shops, manage e-waste, and start building a more sustainable relationship with your technology.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_repair, col_ewaste, col_s2 = st.columns([3, 1.5, 1.5, 3])
    with col_repair:
        if st.button("🛠️  Repair Shops", use_container_width=True, key="home_repair"):
            st.session_state.page = "repair"
            st.rerun()
    with col_ewaste:
        if st.button("♻️  E-Waste", use_container_width=True, key="home_ewaste"):
            st.session_state.page = "ewaste"
            st.rerun()

    # ── Footer ──
    st.markdown("""
    <div class="site-footer">
        <p>©🌍</p>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# ═══════════════════ LOGIN PAGE ════════════════════════════
# ════════════════════════════════════════════════════════════
elif st.session_state.page == "login":

    st.markdown("""
    <style>
    .stApp {
        background: #f0faf3 !important;
    }
    .block-container {
        padding-top: 0.5rem !important;
        max-width: 100% !important;
    }

    /* Login button override */
    .login-form-area .stButton button {
        background: linear-gradient(135deg, #059669, #10b981) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.75rem !important;
        border: none !important;
        font-size: 0.95rem !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.25) !important;
    }
    .login-form-area .stButton button:hover {
        background: linear-gradient(135deg, #047857, #059669) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.35) !important;
    }

    /* Back button override */
    .login-back-btn .stButton button {
        background: white !important;
        color: #475569 !important;
        border: 1.5px solid #e2e8f0 !important;
        font-size: 0.85rem !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    }
    .login-back-btn .stButton button:hover {
        background: #f8fafc !important;
        transform: translateX(-3px) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }

    .stTextInput input {
        border-radius: 12px !important;
        border: 1.5px solid #d1d5db !important;
        padding: 0.8rem 1rem !important;
        font-size: 0.9rem !important;
        background: #fafffe !important;
    }
    .stTextInput input:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-back-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ── LEFT PANEL ──
    with col1:
        left_panel_html = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background: transparent; font-family: 'Plus Jakarta Sans', sans-serif; }
        </style>
        </head>
        <body>
        <div style="background: linear-gradient(155deg, #022c22 0%, #064e3b 35%, #047857 70%, #059669 100%);
                    padding: 44px; border-radius: 20px; min-height: 82vh; overflow: hidden; color: white;
                    font-family: 'Plus Jakarta Sans', sans-serif; position: relative;">

            <!-- Decorative orb -->
            <div style="position: absolute; top: -80px; right: -60px; width: 220px; height: 220px;
                        background: radial-gradient(circle, rgba(110,231,183,0.15), transparent 70%);
                        border-radius: 50%;"></div>
            <div style="position: absolute; bottom: -50px; left: -40px; width: 180px; height: 180px;
                        background: radial-gradient(circle, rgba(52,211,153,0.1), transparent 70%);
                        border-radius: 50%;"></div>

            <div style="position: relative; z-index: 2;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 36px;">
                    <div style="background: rgba(255,255,255,0.12); padding: 10px; border-radius: 12px; font-size: 22px;
                                backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.1);">🌱</div>
                    <div style="font-weight: 700; font-size: 15px; letter-spacing: -0.02em;">Green Device Intelligence</div>
                </div>

                <div style="font-size: 34px; font-weight: 900; margin-bottom: 14px; line-height: 1.15; letter-spacing: -0.03em;">
                    Sustainable tech<br>starts <span style="background: linear-gradient(135deg, #6ee7b7, #34d399);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">here.</span>
                </div>

                <p style="opacity: 0.85; margin-bottom: 32px; line-height: 1.7; font-size: 14px; max-width: 340px;">
                    Monitor your device health, reduce e-waste, and make smarter choices for the planet.
                </p>

                <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 30px;">
                    <div style="background: rgba(255,255,255,0.08); backdrop-filter: blur(6px);
                                padding: 7px 14px; border-radius: 100px; font-size: 12px; font-weight: 500;
                                border: 1px solid rgba(255,255,255,0.08);">
                        <span style="color: #4ade80;">&#9679;</span> 2,400+ devices tracked
                    </div>
                    <div style="background: rgba(255,255,255,0.08); backdrop-filter: blur(6px);
                                padding: 7px 14px; border-radius: 100px; font-size: 12px; font-weight: 500;
                                border: 1px solid rgba(255,255,255,0.08);">
                        <span style="color: #4ade80;">&#9679;</span> 180+ repair partners
                    </div>
                </div>

                <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08);
                            border-radius: 16px; padding: 22px; margin-top: 36px; backdrop-filter: blur(6px);">
                    <p style="font-style: italic; margin-bottom: 16px; opacity: 0.9; font-size: 13.5px; line-height: 1.65;">
                        "GDI helped me extend my laptop's life by 3 years. The eco-score tracking is genuinely useful."
                    </p>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="background: linear-gradient(135deg, #10b981, #34d399); width: 34px; height: 34px;
                                    border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                    font-weight: 700; font-size: 13px;">A</div>
                        <div>
                            <div style="font-weight: 600; font-size: 13px;">Alex Chen</div>
                            <div style="font-size: 11px; opacity: 0.5;">Software Engineer</div>
                        </div>
                        <div style="margin-left: auto; color: #fbbf24; font-size: 13px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                    </div>
                </div>
            </div>
        </div>
        </body>
        </html>
        """
        components.html(left_panel_html, height=900, scrolling=False)

    # ── RIGHT PANEL ──
    with col2:
        st.markdown('<div class="login-form-area">', unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            '<div style="text-align: right; margin-bottom: 28px;">'
            '<a href="#" style="color: #059669; font-weight: 600; text-decoration: none; font-size: 13px;'
            ' letter-spacing: -0.01em;">New here? Create account →</a></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div style="background: linear-gradient(135deg, #ecfdf5, #d1fae5); width: 54px; height: 54px; border-radius: 14px; '
            'display: flex; align-items: center; justify-content: center; font-size: 26px; '
            'margin-bottom: 18px; border: 1px solid #a7f3d0;">👋</div>'
            '<h2 style="font-size: 26px; font-weight: 800; margin-bottom: 6px; color: #0f172a; letter-spacing: -0.03em;">Welcome back</h2>'
            '<p style="color: #64748b; margin-bottom: 28px; font-size: 0.92rem; line-height: 1.5;">Sign in to your account to continue your sustainability journey.</p>',
            unsafe_allow_html=True
        )

        email = st.text_input("Email address", placeholder="name@company.com", label_visibility="visible")
        password = st.text_input("Password", type="password", placeholder="Enter your password",
                                 label_visibility="visible")

        st.markdown(
            '<div style="display: flex; justify-content: space-between; font-size: 12.5px; '
            'color: #6b7280; margin: -8px 0 18px 0;">'
            '<span>Remember me</span>'
            '<a href="#" style="color: #059669; font-weight: 600; text-decoration: none;">Forgot password?</a>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button("Sign in →", use_container_width=True):
            if email == "admin" and password == "1234":
                st.success("✓ Login successful!")
                st.session_state.page = "profile"
                st.rerun()
            else:
                st.error("⚠ Invalid credentials")

        st.markdown(
            '<div style="display: flex; align-items: center; gap: 10px; margin: 22px 0;">'
            '<div style="flex: 1; height: 1px; background: #e5e7eb;"></div>'
            '<span style="font-size: 11.5px; color: #9ca3af; font-weight: 500;">or continue with</span>'
            '<div style="flex: 1; height: 1px; background: #e5e7eb;"></div>'
            '</div>'
            '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 22px;">'
            '<a href="#" style="border: 1.5px solid #e5e7eb; padding: 10px; border-radius: 12px; '
            'text-align: center; text-decoration: none; color: #374151; font-weight: 600; '
            'font-size: 13.5px; background: white; transition: all 0.2s;">Google</a>'
            '<a href="#" style="border: 1.5px solid #e5e7eb; padding: 10px; border-radius: 12px; '
            'text-align: center; text-decoration: none; color: #374151; font-weight: 600; '
            'font-size: 13.5px; background: white; transition: all 0.2s;">Facebook</a>'
            '</div>'
            '<p style="text-align: center; font-size: 13.5px; color: #6b7280;">'
            'Don\'t have an account? <a href="#" style="color: #059669; font-weight: 600; text-decoration: none;">Sign up for free</a>'
            '</p>',
            unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# ═══════════════════ PROFILE PAGE ══════════════════════════
# ════════════════════════════════════════════════════════════
elif st.session_state.page == "profile":

    N8N_FETCH_URL = "https://n8n.srv1090925.hstgr.cloud/webhook/greenloop-fetch"


    def fetch_device_data():
        try:
            response = requests.get(N8N_FETCH_URL)
            if response.status_code == 200:
                devices = response.json()
                d = devices[0]

                return {
                    "device_name": "samsung s23",
                    "device_age": "Auto Synced",
                    "green_points": int(d["greenScore"]),
                    "cpu_score": int(d["cpuUsage"]),
                    "eco_score": 70,  # keep numeric
                    "ram_score": int(d["ramUsagePercent"]),
                    "device_temp": int(d["mobileBatteryTemp"]),
                    "battery_temps": {
                        "hours": ["Live"],
                        "temps": [int(d["mobileBatteryTemp"])]
                    },
                    "daily_goals": [
                        {"goal": "Current CPU %", "progress": int(d["cpuUsage"]), "icon": "📱"},
                        {"goal": "Current RAM %", "progress": int(d["ramUsagePercent"]), "icon": "💾"},
                        {"goal": "Current Mobile Battery %", "progress": int(d["mobileBatteryLevel"]), "icon": "🔋"},
                    ]
                }
        except Exception as e:
            st.error(f"API Fetch Failed: {e}")
            return None


    if "last_fetch" not in st.session_state:
        st.session_state.last_fetch = 0

    if time.time() - st.session_state.last_fetch > 10:
        new_data = fetch_device_data()
        if new_data:
            st.session_state.device_data = new_data
            st.session_state.last_fetch = time.time()

    if "device_data" not in st.session_state:
        data = fetch_device_data()
        if data:
            st.session_state.device_data = data
        else:
            st.session_state.device_data = {}

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #edf9f0 0%, #f0fdf4 50%, #f8fdf9 100%) !important;
    }
    .block-container {
        padding-top: 1rem !important;
        max-width: 1240px !important;
        margin: 0 auto;
    }

    /* ── Profile Header Card ── */
    .profile-header {
        background: white;
        border-radius: 18px;
        padding: 1.75rem 2rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04);
        display: flex;
        align-items: center;
        gap: 1.5rem;
        border: 1px solid #e8f5e9;
    }
    .profile-avatar {
        width: 72px; height: 72px;
        border-radius: 50%;
        background: linear-gradient(135deg, #10b981, #059669);
        display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25);
        flex-shrink: 0;
        position: relative;
    }
    .profile-avatar::after {
        content: '✓';
        position: absolute;
        bottom: 0; right: 0;
        width: 22px; height: 22px;
        background: white;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.65rem;
        color: #10b981;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        font-weight: 700;
    }
    .profile-info { flex: 1; }
    .profile-device-name {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .profile-badges {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
    }
    .pbadge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.4rem 0.85rem;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .pbadge-sync { background: #dbeafe; color: #1e40af; }
    .pbadge-pts { background: #fef3c7; color: #92400e; }
    .pbadge-temp { background: #e0f2fe; color: #0369a1; }

    .logout-chip {
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        padding: 0.5rem 1.2rem;
        border-radius: 10px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #475569;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
    }
    .logout-chip:hover { background: #e2e8f0; }

    /* ── Stats Grid ── */
    .stats-row {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        margin-bottom: 1.25rem;
    }
    .stat-tile {
        background: white;
        border-radius: 14px;
        padding: 1.3rem 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03), 0 4px 14px rgba(0,0,0,0.04);
        text-align: center;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid #f0f0f0;
    }
    .stat-tile:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 24px rgba(5, 150, 105, 0.1);
        border-color: #d1fae5;
    }
    .stat-tile-icon {
        width: 42px; height: 42px;
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 0.8rem;
        font-size: 1.15rem;
    }
    .sti-green { background: #dcfce7; }
    .sti-blue { background: #dbeafe; }
    .sti-teal { background: #ccfbf1; }
    .sti-purple { background: #f3e8ff; }
    .sti-orange { background: #ffedd5; }
    .stat-tile-val {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.02em;
        margin-bottom: 0.15rem;
    }
    .stat-tile-lbl {
        font-size: 0.7rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    /* ── Battery Card ── */
    .batt-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03), 0 4px 14px rgba(0,0,0,0.04);
        border: 1px solid #f0f0f0;
    }
    .card-hdr {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    .card-hdr-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.01em;
    }
    .card-hdr-sub {
        font-size: 0.78rem;
        color: #94a3b8;
    }

    /* ── Back Button ── */
    .prof-back .stButton button {
        background: white !important;
        border: 1.5px solid #e2e8f0 !important;
        color: #475569 !important;
        border-radius: 10px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
        height: 40px !important;
    }
    .prof-back .stButton button:hover {
        background: #f8fafc !important;
        transform: translateX(-3px) !important;
    }

    /* ── Title ── */
    .page-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        text-align: center;
        letter-spacing: -0.03em;
        margin: 0.5rem 0 0.15rem;
    }
    .page-sub {
        text-align: center;
        font-size: 0.92rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }

    /* ── Expander ── */
    .stExpander {
        border: 1px solid #e8f5e9 !important;
        border-radius: 14px !important;
        background: white !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03) !important;
        margin-bottom: 1.25rem !important;
    }

    /* ── Responsive ── */
    @media (max-width: 1200px) {
        .stats-row { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 768px) {
        .stats-row { grid-template-columns: repeat(2, 1fr); }
        .profile-header { flex-direction: column; text-align: center; }
        .profile-badges { justify-content: center; }
    }
    </style>
    """, unsafe_allow_html=True)

    # Header row
    header_col1, header_col2, header_col3 = st.columns([1.5, 5, 1.5])
    with header_col1:
        st.markdown('<div class="prof-back">', unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_from_profile"):
            st.session_state.page = "home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with header_col2:
        st.markdown('<div class="page-title">📊 User Stats</div>', unsafe_allow_html=True)

    st.markdown('<div class="page-sub">Your device health & sustainability dashboard</div>', unsafe_allow_html=True)

    if not st.session_state.get("device_data"):
        st.warning("⚠️ Device data not available. Trying to reconnect...")
        st.stop()

    # Profile header card
    st.markdown(f"""
    <div class="profile-header">
        <div class="profile-avatar">📱</div>
        <div class="profile-info">
            <div class="profile-device-name">{html_module.escape(st.session_state.device_data['device_name'])}</div>
            <div class="profile-badges">
                <span class="pbadge pbadge-sync">📅 {html_module.escape(st.session_state.device_data['device_age'])}</span>
                <span class="pbadge pbadge-pts">🏆 {st.session_state.device_data['green_points']} Green Points</span>
                <span class="pbadge pbadge-temp">🌡️ {st.session_state.device_data['device_temp']}°C</span>
            </div>
        </div>
        <a class="logout-chip" href="#" onclick="alert('Logout functionality')">Logout</a>
    </div>
    """, unsafe_allow_html=True)

    # Edit Device Info
    with st.expander(" "):
        col1, col2, col3 = st.columns(3)
        with col1:
            device_name = st.text_input("Device Name", value=st.session_state.device_data['device_name'])
            cpu_score = st.number_input("CPU Score", min_value=0, max_value=100,
                                        value=st.session_state.device_data['cpu_score'])
        with col2:
            device_age = st.text_input("Device Age", value=st.session_state.device_data['device_age'])
            eco_score = st.number_input("Eco Score", min_value=0, max_value=100,
                                        value=st.session_state.device_data['eco_score'])
        with col3:
            green_points = st.number_input("Green Points", min_value=0,
                                           value=st.session_state.device_data['green_points'])
            ram_score = st.number_input("RAM Score", min_value=0, max_value=100,
                                        value=st.session_state.device_data['ram_score'])

        device_temp = st.number_input("Device Temperature (°C)", min_value=0, max_value=100,
                                      value=st.session_state.device_data['device_temp'])

        st.markdown("**Battery Temperature Data**")
        temp_col1, temp_col2 = st.columns(2)
        with temp_col1:
            hours_input = st.text_input("Hours (comma-separated)",
                                        value=", ".join(st.session_state.device_data['battery_temps']['hours']))
        with temp_col2:
            temps_input = st.text_input("Temperatures (comma-separated)", value=", ".join(
                map(str, st.session_state.device_data['battery_temps']['temps'])))

        st.markdown("**Daily Goals**")
        goals_list = []
        for i, goal in enumerate(st.session_state.device_data['daily_goals']):
            goal_col1, goal_col2, goal_col3 = st.columns([2, 1, 1])
            with goal_col1:
                goal_text = st.text_input(f"Goal {i + 1}", value=goal['goal'], key=f"goal_{i}")
            with goal_col2:
                goal_icon = st.text_input(f"Icon {i + 1}", value=goal['icon'], key=f"icon_{i}")
            with goal_col3:
                goal_progress = st.number_input(f"Progress", min_value=0, max_value=100, value=goal['progress'],
                                                key=f"progress_{i}")
            goals_list.append({'goal': goal_text, 'progress': goal_progress, 'icon': goal_icon})

        if st.button("💾 Save Changes", use_container_width=True):
            st.session_state.device_data['device_name'] = device_name
            st.session_state.device_data['device_age'] = device_age
            st.session_state.device_data['green_points'] = green_points
            st.session_state.device_data['cpu_score'] = cpu_score
            st.session_state.device_data['eco_score'] = eco_score
            st.session_state.device_data['ram_score'] = ram_score
            st.session_state.device_data['device_temp'] = device_temp
            st.session_state.device_data['battery_temps']['hours'] = [h.strip() for h in hours_input.split(',')]
            st.session_state.device_data['battery_temps']['temps'] = [float(t.strip()) for t in temps_input.split(',')]
            st.session_state.device_data['daily_goals'] = goals_list
            st.success("✅ Device data updated successfully!")
            st.rerun()

    # Stats grid
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-tile">
            <div class="stat-tile-icon sti-green">🏆</div>
            <div class="stat-tile-val">{st.session_state.device_data['green_points']:,}</div>
            <div class="stat-tile-lbl">Green Points</div>
        </div>
        <div class="stat-tile">
            <div class="stat-tile-icon sti-blue">⚙️</div>
            <div class="stat-tile-val">{st.session_state.device_data['cpu_score']}/100</div>
            <div class="stat-tile-lbl">CPU Score</div>
        </div>
        <div class="stat-tile">
            <div class="stat-tile-icon sti-teal">🌿</div>
            <div class="stat-tile-val">{st.session_state.device_data['eco_score']}/100</div>
            <div class="stat-tile-lbl">Eco Score</div>
        </div>
        <div class="stat-tile">
            <div class="stat-tile-icon sti-purple">💾</div>
            <div class="stat-tile-val">{st.session_state.device_data['ram_score']}/100</div>
            <div class="stat-tile-lbl">RAM Score</div>
        </div>
        <div class="stat-tile">
            <div class="stat-tile-icon sti-orange">🌡️</div>
            <div class="stat-tile-val">{st.session_state.device_data['device_temp']}°C</div>
            <div class="stat-tile-lbl">Device Temp</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bottom Grid: Goals and Battery
    col_goals, col_battery = st.columns([1, 1.5])

    with col_goals:
        total_goals = len(st.session_state.device_data['daily_goals'])
        completed = sum(1 for g in st.session_state.device_data['daily_goals'] if g['progress'] >= 80)
        avg_progress = sum(g['progress'] for g in st.session_state.device_data['daily_goals']) // total_goals
        on_track = sum(1 for g in st.session_state.device_data['daily_goals'] if g['progress'] >= 50)

        goal_items_html = ""
        for goal in st.session_state.device_data['daily_goals']:
            progress_class = 'high' if goal['progress'] >= 70 else ('medium' if goal['progress'] >= 40 else 'low')
            safe_text = html_module.escape(goal['goal'])
            goal_items_html += f"""
            <div class="goal-item">
                <div class="goal-header">
                    <div class="goal-text">
                        <span>{goal['icon']}</span>
                        <span>{safe_text}</span>
                    </div>
                    <div class="goal-pct {progress_class}">{goal['progress']}%</div>
                </div>
                <div class="progress-track">
                    <div class="progress-bar {progress_class}" style="width: {goal['progress']}%"></div>
                </div>
            </div>
            """

        goals_full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                background: transparent;
            }}
            .goals-card {{
                background: white;
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 1px 4px rgba(0,0,0,0.03), 0 4px 14px rgba(0,0,0,0.04);
                border: 1px solid #f0f0f0;
            }}
            .goals-hdr {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 1.25rem;
            }}
            .goals-hdr-icon {{
                font-size: 1.4rem;
            }}
            .goals-hdr-title {{
                font-size: 1.05rem;
                font-weight: 700;
                color: #0f172a;
                letter-spacing: -0.01em;
            }}
            .goal-item {{
                margin-bottom: 1rem;
            }}
            .goal-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.4rem;
            }}
            .goal-text {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.85rem;
                font-weight: 500;
                color: #334155;
            }}
            .goal-pct {{
                font-size: 0.85rem;
                font-weight: 700;
            }}
            .goal-pct.high {{ color: #059669; }}
            .goal-pct.medium {{ color: #d97706; }}
            .goal-pct.low {{ color: #dc2626; }}
            .progress-track {{
                width: 100%;
                height: 7px;
                background: #f1f5f9;
                border-radius: 10px;
                overflow: hidden;
            }}
            .progress-bar {{
                height: 100%;
                border-radius: 10px;
                transition: width 0.6s ease;
            }}
            .progress-bar.high {{ background: linear-gradient(90deg, #10b981, #34d399); }}
            .progress-bar.medium {{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }}
            .progress-bar.low {{ background: linear-gradient(90deg, #ef4444, #f87171); }}
        </style>
        </head>
        <body>
            <div class="goals-card">
                <div class="goals-hdr">
                    <span class="goals-hdr-icon">🎯</span>
                    <span class="goals-hdr-title">Current Device Stats</span>
                </div>
                {goal_items_html}
            </div>
        </body>
        </html>
        """

        card_height = 80 + (58 * total_goals) + 48
        components.html(goals_full_html, height=card_height, scrolling=False)

    with col_battery:
        with st.container():
            st.markdown("""
            <div class="batt-card">
                <div class="card-hdr">
                    <span style="font-size: 1.4rem;">🔋</span>
                    <div>
                        <div class="card-hdr-title">Battery Temperature</div>
                        <div class="card-hdr-sub">Temperature variation throughout the day</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            import pandas as pd
            import altair as alt

            battery_df = pd.DataFrame({
                'Time': st.session_state.device_data['battery_temps']['hours'],
                'Temperature': st.session_state.device_data['battery_temps']['temps']
            })

            chart = alt.Chart(battery_df).mark_area(
                line={'color': '#10b981', 'strokeWidth': 2},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[
                        alt.GradientStop(color='rgba(209, 250, 229, 0.4)', offset=0),
                        alt.GradientStop(color='rgba(110, 231, 183, 0.8)', offset=1)
                    ],
                    x1=1, x2=1, y1=1, y2=0
                ),
                interpolate='monotone'
            ).encode(
                x=alt.X('Time:N', axis=alt.Axis(labelAngle=0, title=None,
                         labelFont='Plus Jakarta Sans', labelFontWeight=500)),
                y=alt.Y('Temperature:Q', scale=alt.Scale(domain=[20, 50]),
                         axis=alt.Axis(title='Temperature (°C)', tickCount=5,
                         titleFont='Plus Jakarta Sans', labelFont='Plus Jakarta Sans')),
                tooltip=['Time', 'Temperature']
            ).properties(
                height=260
            ).configure_view(
                strokeWidth=0
            ).configure_axis(
                grid=True,
                gridColor='#f1f5f9',
                domainColor='#e2e8f0'
            )

            st.altair_chart(chart, use_container_width=True)

            min_temp = min(st.session_state.device_data['battery_temps']['temps'])
            max_temp = max(st.session_state.device_data['battery_temps']['temps'])
            avg_temp = sum(st.session_state.device_data['battery_temps']['temps']) // len(
                st.session_state.device_data['battery_temps']['temps'])

            st.markdown(f"""
            <div style="display: flex; justify-content: space-around; margin-top: 0.75rem; padding-top: 0.75rem;
                        border-top: 1px solid #f1f5f9;">
                <div style="text-align: center;">
                    <span style="color: #10b981; font-weight: 600; font-size: 0.88rem;">● Min: {min_temp}°C</span>
                </div>
                <div style="text-align: center;">
                    <span style="color: #f59e0b; font-weight: 600; font-size: 0.88rem;">● Avg: {avg_temp}°C</span>
                </div>
                <div style="text-align: center;">
                    <span style="color: #ef4444; font-weight: 600; font-size: 0.88rem;">● Max: {max_temp}°C</span>
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# ═══════════════════ REPAIR PAGE ═══════════════════════════
# ════════════════════════════════════════════════════════════
elif st.session_state.page == "repair":

    st.markdown("""
    <style>
    .stApp {
        background: #f0faf3 !important;
    }

    /* Floating back button */
    .repair-back-wrap {
        position: fixed !important;
        top: 12px !important;
        left: 16px !important;
        z-index: 999999 !important;
    }
    .repair-back-wrap * {
        margin: 0 !important;
        padding: 0 !important;
    }
    .repair-back-wrap button {
        background: white !important;
        border: 1.5px solid #e2e8f0 !important;
        color: #475569 !important;
        border-radius: 10px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        height: 38px !important;
        padding: 0 16px !important;
    }
    .repair-back-wrap button:hover {
        background: #f8fafc !important;
        transform: translateX(-3px) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="repair-back-wrap">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_from_repair"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    repair_page()


# ════════════════════════════════════════════════════════════
# ═══════════════════ E-WASTE PAGE ══════════════════════════
# ════════════════════════════════════════════════════════════
elif st.session_state.page == "ewaste":
    ewaste_page()
