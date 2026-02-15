import streamlit as st
import base64
from repair_shops_data_and_ewaste import repair_page, ewaste_page
import streamlit.components.v1 as components
import html as html_module

st.set_page_config(
    page_title="Green Device Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@200..900&display=swap');

.stApp {
  background: linear-gradient(
    180deg,
    #e8f8f1 0%,
    #ccebdb 30%,
    #ecfdf5 75%,
    #ffffff 100%
  ) fixed !important;
}


/* Let gradient show through */
section.main > div {
    background: transparent !important;
}

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    letter-spacing: -0.02em;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.hero-sub {
    font-size: 1.2rem;
    opacity: 0.9;
}

.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid rgba(255,255,255,0.15);
}

.stButton > button {
    border-radius: 12px;
    padding: 0.75rem 1.25rem;
    font-weight: 600;
    transition: all 0.2s ease;
    border: 1px solid #16a34a;
    background: linear-gradient(135deg, #16a34a, #22c55e);
    color: white;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0px 10px 20px rgba(34,197,94,0.25);
}

.section {
    margin-top: 4rem;
    margin-bottom: 2rem;
}

.divider {
    margin: 3rem 0;
    border-bottom: 1px solid rgba(0,0,0,0.08);
}

.footer {
    opacity: 0.6;
    font-size: 0.85rem;
    text-align: center;
    margin-top: 4rem;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"


def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ============================================================
# ======================== HOME PAGE =========================
# ============================================================
if st.session_state.page == "home":

    # Try to load background image, gracefully handle if missing
    try:
        image_base64 = get_base64_image("del.jpg")
        hero_bg = f"url('data:image/jpeg;base64,{image_base64}') center/cover no-repeat"
    except Exception:
        hero_bg = "linear-gradient(135deg, #065f46 0%, #047857 30%, #059669 60%, #10b981 100%)"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

    .stApp {{
        background: #f0fdf4 !important;
    }}
    section.main > div {{
        background: transparent !important;
        padding: 0 !important;
    }}
    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* ── Navbar ── */
    .gdi-nav {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.9rem 3rem;
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-bottom: 1px solid rgba(0,0,0,0.06);
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }}
    .gdi-nav-brand {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-weight: 800;
        font-size: 1.15rem;
        color: #065f46;
        letter-spacing: -0.02em;
    }}
    .gdi-nav-brand span {{
        font-size: 1.4rem;
    }}
    .gdi-nav-links {{
        display: flex;
        align-items: center;
        gap: 2rem;
    }}
    .gdi-nav-links a {{
        font-size: 0.9rem;
        font-weight: 500;
        color: #334155;
        text-decoration: none;
        transition: color 0.2s;
    }}
    .gdi-nav-links a:hover {{
        color: #059669;
    }}

    /* ── Hero ── */
    .gdi-hero {{
        position: relative;
        width: 100%;
        min-height: 92vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: {hero_bg};
        overflow: hidden;
    }}
    .gdi-hero::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(
            180deg,
            rgba(0,30,20,0.55) 0%,
            rgba(0,40,25,0.45) 50%,
            rgba(0,50,30,0.60) 100%
        );
        z-index: 1;
    }}
    .gdi-hero-inner {{
        position: relative;
        z-index: 2;
        text-align: center;
        max-width: 820px;
        padding: 2rem;
    }}
    .gdi-hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 100px;
        padding: 0.45rem 1.2rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        color: #d1fae5;
        margin-bottom: 1.75rem;
        letter-spacing: 0.03em;
    }}
    .gdi-hero-badge .pulse {{
        width: 8px;
        height: 8px;
        background: #34d399;
        border-radius: 50%;
        animation: gdi-pulse 2s infinite;
    }}
    @keyframes gdi-pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.5; transform: scale(1.5); }}
    }}
    .gdi-hero h1 {{
        font-family: 'Inter', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        color: #ffffff;
        line-height: 1.08;
        letter-spacing: -0.03em;
        margin: 0 0 1rem 0;
    }}
    .gdi-hero h1 .green {{
        color: #6ee7b7;
    }}
    .gdi-hero-desc {{
        font-family: 'Inter', sans-serif;
        font-size: 1.15rem;
        color: rgba(255,255,255,0.8);
        line-height: 1.7;
        max-width: 600px;
        margin: 0 auto 2.5rem auto;
    }}
    .gdi-hero-actions {{
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }}
    .gdi-btn {{
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        padding: 0.85rem 2rem;
        border-radius: 14px;
        border: none;
        cursor: pointer;
        transition: all 0.25s ease;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }}
    .gdi-btn-primary {{
        background: #10b981;
        color: white;
        box-shadow: 0 8px 24px rgba(16,185,129,0.35);
    }}
    .gdi-btn-primary:hover {{
        background: #059669;
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(16,185,129,0.45);
    }}
    .gdi-btn-outline {{
        background: rgba(255,255,255,0.12);
        color: white;
        border: 1.5px solid rgba(255,255,255,0.35);
        backdrop-filter: blur(6px);
    }}
    .gdi-btn-outline:hover {{
        background: rgba(255,255,255,0.22);
        transform: translateY(-3px);
    }}
    .gdi-hero-stats {{
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-top: 3.5rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255,255,255,0.12);
    }}
    .gdi-hero-stat {{
        text-align: center;
    }}
    .gdi-hero-stat-val {{
        font-family: 'Inter', sans-serif;
        font-size: 1.6rem;
        font-weight: 800;
        color: #6ee7b7;
    }}
    .gdi-hero-stat-lbl {{
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        font-weight: 500;
        color: rgba(255,255,255,0.55);
        margin-top: 0.2rem;
        letter-spacing: 0.02em;
    }}

    /* ── Scroll Indicator ── */
    .gdi-scroll-hint {{
        position: absolute;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 3;
        text-align: center;
    }}
    .gdi-scroll-hint span {{
        display: block;
        width: 24px;
        height: 38px;
        border: 2px solid rgba(255,255,255,0.35);
        border-radius: 12px;
        margin: 0 auto 0.5rem;
        position: relative;
    }}
    .gdi-scroll-hint span::after {{
        content: '';
        width: 4px;
        height: 8px;
        background: rgba(255,255,255,0.6);
        border-radius: 2px;
        position: absolute;
        top: 6px;
        left: 50%;
        transform: translateX(-50%);
        animation: gdi-scroll-bob 1.8s ease-in-out infinite;
    }}
    @keyframes gdi-scroll-bob {{
        0%   {{ top: 6px; opacity: 1; }}
        50%  {{ top: 18px; opacity: 0.3; }}
        100% {{ top: 6px; opacity: 1; }}
    }}
    .gdi-scroll-hint p {{
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 500;
        color: rgba(255,255,255,0.4);
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    /* ── Content Sections ── */
    .gdi-section {{
        max-width: 1140px;
        margin: 0 auto;
        padding: 5rem 2rem;
    }}
    .gdi-section-header {{
        text-align: center;
        margin-bottom: 3.5rem;
    }}
    .gdi-section-tag {{
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        color: #059669;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.6rem;
        background: #ecfdf5;
        padding: 0.35rem 1rem;
        border-radius: 100px;
    }}
    .gdi-section-title {{
        font-family: 'Inter', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.025em;
        margin: 0.5rem 0;
        line-height: 1.2;
    }}
    .gdi-section-desc {{
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        color: #64748b;
        max-width: 560px;
        margin: 0 auto;
        line-height: 1.6;
    }}

    /* ── Feature Cards ── */
    .gdi-features {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
    }}
    .gdi-feature {{
        background: white;
        border-radius: 20px;
        padding: 2.2rem 1.8rem;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    .gdi-feature::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #10b981, #34d399);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    .gdi-feature:hover {{
        transform: translateY(-6px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        border-color: #d1fae5;
    }}
    .gdi-feature:hover::before {{
        opacity: 1;
    }}
    .gdi-feature-icon {{
        width: 56px;
        height: 56px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1.25rem;
    }}
    .gdi-feature-icon.green {{ background: #dcfce7; }}
    .gdi-feature-icon.blue {{ background: #dbeafe; }}
    .gdi-feature-icon.amber {{ background: #fef3c7; }}
    .gdi-feature h3 {{
        font-family: 'Inter', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 0.6rem 0;
    }}
    .gdi-feature p {{
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #64748b;
        line-height: 1.6;
        margin: 0;
    }}

    /* ── CTA Banner ── */
    .gdi-cta {{
        background: linear-gradient(135deg, #065f46 0%, #047857 40%, #059669 100%);
        border-radius: 24px;
        padding: 3.5rem 3rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 2rem;
        max-width: 1140px;
        margin: 0 auto 4rem auto;
        position: relative;
        overflow: hidden;
    }}
    .gdi-cta::before {{
        content: '';
        position: absolute;
        top: -40%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.08), transparent 70%);
        border-radius: 50%;
    }}
    .gdi-cta-text {{
        position: relative;
        z-index: 2;
        flex: 1;
    }}
    .gdi-cta-text h2 {{
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: white;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
    }}
    .gdi-cta-text p {{
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: rgba(255,255,255,0.8);
        margin: 0;
        line-height: 1.6;
    }}
    .gdi-cta-actions {{
        display: flex;
        gap: 1rem;
        position: relative;
        z-index: 2;
        flex-wrap: wrap;
    }}
    .gdi-btn-white {{
        background: white;
        color: #065f46;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        padding: 0.85rem 2rem;
        border-radius: 14px;
        border: none;
        cursor: pointer;
        transition: all 0.25s ease;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        text-decoration: none;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }}
    .gdi-btn-white:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }}
    .gdi-btn-ghost {{
        background: rgba(255,255,255,0.12);
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        padding: 0.85rem 2rem;
        border-radius: 14px;
        border: 1.5px solid rgba(255,255,255,0.3);
        cursor: pointer;
        transition: all 0.25s ease;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        text-decoration: none;
    }}
    .gdi-btn-ghost:hover {{
        background: rgba(255,255,255,0.22);
        transform: translateY(-3px);
    }}

    /* ── Footer ── */
    .gdi-footer {{
        text-align: center;
        padding: 2rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        color: #94a3b8;
        border-top: 1px solid #e5e7eb;
        max-width: 1140px;
        margin: 0 auto;
    }}

    /* ── Responsive ── */
    @media (max-width: 900px) {{
        .gdi-hero h1 {{ font-size: 2.6rem; }}
        .gdi-features {{ grid-template-columns: 1fr; }}
        .gdi-cta {{ flex-direction: column; text-align: center; padding: 2.5rem 1.5rem; }}
        .gdi-cta-actions {{ justify-content: center; }}
        .gdi-hero-stats {{ gap: 1.5rem; }}
        .gdi-nav {{ padding: 0.8rem 1.5rem; }}
    }}

    /* Hide default streamlit buttons styling for home page */
    .home-btn-row .stButton > button {{
        height: 52px !important;
        font-size: 0.95rem !important;
        border-radius: 14px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # ── Navbar ──
    st.markdown("""
    <div class="gdi-nav">
        <div class="gdi-nav-brand">
            <span>🌱</span> Green Device Intelligence
        </div>
        <div class="gdi-nav-links">
            <a href="#features">Features</a>
            <a href="#services">Services</a>
            <a href="#about">About</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero Section ──
    st.markdown(f"""
    <div class="gdi-hero">
        <div class="gdi-hero-inner">
            <div class="gdi-hero-badge">
                <div class="pulse"></div>
                Sustainable Tech Platform
            </div>
            <h1>Make Your Tech<br><span class="green">Greener & Smarter</span></h1>
            <div class="gdi-hero-desc">
                Track your device's environmental impact, find eco-friendly repair shops, 
                and join the movement towards sustainable technology.
            </div>
            <div class="gdi-hero-stats">
                <div class="gdi-hero-stat">
                    <div class="gdi-hero-stat-val">2.4K+</div>
                    <div class="gdi-hero-stat-lbl">Devices Tracked</div>
                </div>
                <div class="gdi-hero-stat">
                    <div class="gdi-hero-stat-val">180+</div>
                    <div class="gdi-hero-stat-lbl">Repair Partners</div>
                </div>
                <div class="gdi-hero-stat">
                    <div class="gdi-hero-stat-val">12T</div>
                    <div class="gdi-hero-stat-lbl">CO₂ Saved</div>
                </div>
                <div class="gdi-hero-stat">
                    <div class="gdi-hero-stat-val">98%</div>
                    <div class="gdi-hero-stat-lbl">Satisfaction</div>
                </div>
            </div>
        </div>
        <div class="gdi-scroll-hint">
            <span></span>
            <p>Scroll</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Auth Buttons Row ──
    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)
    
    col_spacer1, col_login, col_signup, col_spacer2 = st.columns([3, 1.5, 1.5, 3])
    with col_login:
        if st.button("🔐  Login", use_container_width=True, key="home_login"):
            st.session_state.page = "login"
            st.rerun()
    with col_signup:
        if st.button("✨  Sign Up", use_container_width=True, key="home_signup"):
            st.write("Signup coming soon!!")
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

    # ── Features Section ──
    st.markdown("""
    <div class="gdi-section" id="features">
        <div class="gdi-section-header">
            <div class="gdi-section-tag">Why Choose Us</div>
            <div class="gdi-section-title">Everything You Need for<br>Sustainable Tech</div>
            <div class="gdi-section-desc">
                From real-time device monitoring to eco-friendly repair options — 
                we provide the tools to reduce your digital carbon footprint.
            </div>
        </div>
        <div class="gdi-features">
            <div class="gdi-feature">
                <div class="gdi-feature-icon green">📊</div>
                <h3>Device Health Monitoring</h3>
                <p>Track CPU usage, RAM performance, battery temperature, and eco scores in real-time with beautiful dashboards.</p>
            </div>
            <div class="gdi-feature">
                <div class="gdi-feature-icon blue">🛠️</div>
                <h3>Eco-Friendly Repairs</h3>
                <p>Find verified local repair shops that prioritize sustainability. Extend your device lifespan instead of replacing.</p>
            </div>
            <div class="gdi-feature">
                <div class="gdi-feature-icon amber">♻️</div>
                <h3>E-Waste Management</h3>
                <p>Locate certified e-waste recycling centres near you. Dispose of old electronics responsibly and safely.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA Section with service buttons ──
    st.markdown("""
    <div class="gdi-cta" id="services">
        <div class="gdi-cta-text">
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
    <div class="gdi-footer">
        <p>© </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# ======================== LOGIN PAGE ========================
# ============================================================
elif st.session_state.page == "login":

    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif !important;
    }

    .stTextInput input {
        border-radius: 10px !important;
        border: 1.5px solid #e5e7eb !important;
        padding: 12px !important;
        font-size: 14px !important;
    }

    .stTextInput input:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
    }

    .stButton button {
        background: #059669 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 12px !important;
        border: none !important;
        width: 100% !important;
    }

    .stButton button:hover {
        background: #047857 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    col1, col2 = st.columns(2)

    # ── LEFT PANEL: use components.html() to bypass Markdown parser ──
    with col1:
        left_panel_html = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background: transparent; font-family: 'Inter', sans-serif; }
        </style>
        </head>
        <body>
        <div style="background: linear-gradient(160deg, #022c22, #064e3b, #047857, #059669);
                    padding: 40px; border-radius: 16px; min-height: 80vh; overflow: hidden; color: white;
                    font-family: 'Inter', sans-serif;">
                    

            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 30px;">
                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; font-size: 24px;">🌱</div>
                <div style="font-weight: 700; font-size: 16px;">Green Device Intelligence</div>
            </div>
                
            <div style="font-size: 36px; font-weight: 900; margin-bottom: 15px; line-height: 1.2;">
                Sustainable tech<br>starts <span style="color: #6ee7b7;">here.</span>
            </div>

            <p style="opacity: 0.9; margin-bottom: 30px; line-height: 1.6; font-size: 15px;">
                Monitor your device health, reduce e-waste, and make smarter choices for the planet.
            </p>

            <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 25px;">
                <div style="background: rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 20px; font-size: 12px;">
                    <span style="color: #34d399;">&#9679;</span> 2,400+ devices tracked
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 20px; font-size: 12px;">
                    <span style="color: #34d399;">&#9679;</span> 180+ repair partners
                </div>
            </div>

            <div style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
                        border-radius: 16px; padding: 20px; margin-top: 40px;">
                <p style="font-style: italic; margin-bottom: 15px; opacity: 0.9; font-size: 14px; line-height: 1.6;">
                    "GDI helped me extend my laptop's life by 3 years. The eco-score tracking is genuinely useful."
                </p>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="background: linear-gradient(135deg, #10b981, #34d399); width: 36px; height: 36px;
                                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                                font-weight: 700; font-size: 14px;">A</div>
                    <div>
                        <div style="font-weight: 600; font-size: 14px;">Alex Chen</div>
                        <div style="font-size: 12px; opacity: 0.6;">Software Engineer</div>
                    </div>
                    <div style="margin-left: auto; color: #fbbf24; font-size: 14px;">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                </div>
            </div>

        </div>
        </body>
        </html>
        """
        components.html(left_panel_html, height=900, scrolling=False)

    # ── RIGHT PANEL: login form (keep as-is, just fix indentation) ──
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

        # These small HTML snippets work fine in st.markdown
        # because they're short and simple
        st.markdown(
            '<div style="text-align: right; margin-bottom: 30px;">'
            '<a href="#" style="color: #059669; font-weight: 600; text-decoration: none; font-size: 14px;">'
            'New here? Create account →</a></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div style="background: #ecfdf5; width: 56px; height: 56px; border-radius: 14px; '
            'display: flex; align-items: center; justify-content: center; font-size: 28px; '
            'margin-bottom: 20px;">👋</div>'
            '<h2 style="font-size: 28px; font-weight: 800; margin-bottom: 8px; color: #0f172a;">Welcome back</h2>'
            '<p style="color: #64748b; margin-bottom: 30px;">Sign in to your account to continue your sustainability journey.</p>',
            unsafe_allow_html=True
        )

        email = st.text_input("Email address", placeholder="name@company.com", label_visibility="visible")
        password = st.text_input("Password", type="password", placeholder="Enter your password",
                                 label_visibility="visible")

        st.markdown(
            '<div style="display: flex; justify-content: space-between; font-size: 13px; '
            'color: #6b7280; margin: -10px 0 20px 0;">'
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
            '<div style="display: flex; align-items: center; gap: 10px; margin: 20px 0;">'
            '<div style="flex: 1; height: 1px; background: #e5e7eb;"></div>'
            '<span style="font-size: 12px; color: #9ca3af;">or continue with</span>'
            '<div style="flex: 1; height: 1px; background: #e5e7eb;"></div>'
            '</div>'
            '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">'
            '<a href="#" style="border: 1.5px solid #e5e7eb; padding: 10px; border-radius: 10px; '
            'text-align: center; text-decoration: none; color: #374151; font-weight: 600; '
            'font-size: 14px; background: white;">Google</a>'
            '<a href="#" style="border: 1.5px solid #e5e7eb; padding: 10px; border-radius: 10px; '
            'text-align: center; text-decoration: none; color: #374151; font-weight: 600; '
            'font-size: 14px; background: white;">Facebook</a>'
            '</div>'
            '<p style="text-align: center; font-size: 14px; color: #6b7280;">'
            'Don\'t have an account? <a href="#" style="color: #059669; font-weight: 600; text-decoration: none;">Sign up for free</a>'
            '</p>',
            unsafe_allow_html=True)

# ============================================================
# ======================== PROFILE PAGE ======================
# ============================================================
elif st.session_state.page == "profile":

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #d4f4e7 0%, #e8f8f1 40%, #f0fdf7 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if "device_data" not in st.session_state:
        st.session_state.device_data = {
            'device_name': 'Samsung Galaxy S23',
            'device_age': '2 years, 3 months',
            'green_points': 1250,
            'cpu_score': 87,
            'eco_score': 72,
            'ram_score': 65,
            'device_temp': 34,
            'battery_temps': {
                'hours': ['6 AM', '8 AM', '10 AM', '12 PM', '2 PM', '4 PM', '6 PM', '8 PM', '10 AM'],
                'temps': [27, 29, 32, 38, 42, 40, 35, 32, 28]
            },
            'daily_goals': [
                {'goal': 'Current Ram Usage', 'progress': 75, 'icon': '📱'},
                {'goal': 'Current device temp ', 'progress': 60, 'icon': '🌡️'},
                {'goal': 'Current CPU usage', 'progress': 90, 'icon': '🌿'},
                {'goal': 'Current eco score', 'progress': 45, 'icon': '🔋'},
                {'goal': 'Current ', 'progress': 82, 'icon': '⚡'}
            ]
        }

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    .profile-page-container #MainMenu {visibility: hidden;}
    .profile-page-container footer {visibility: hidden;}

    .block-container {
        padding-top: 0.5rem !important;
    }

    .profile-page-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem 3rem;
    }

    .page-title-inline {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.02em;
        text-align: center;
        line-height: 1.2;
    }

    .page-subtitle {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #64748b;
        margin-bottom: 2rem;
        margin-top: 0.25rem;
    }

    .back-btn-col button {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        color: #475569 !important;
        border-radius: 10px !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        height: 42px !important;
        margin-top: 0.5rem;
    }

    .back-btn-col button:hover {
        background: #f8fafc !important;
        transform: translateX(-3px) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12) !important;
    }

    .profile-header-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .profile-icon {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        position: relative;
    }

    .profile-icon::after {
        content: '✓';
        position: absolute;
        bottom: 2px;
        right: 2px;
        width: 24px;
        height: 24px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        color: #10b981;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .profile-details { flex: 1; }

    .device-name {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.75rem;
    }

    .device-badges {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 600;
    }

    .badge-age { background: #e0f2fe; color: #0369a1; }
    .badge-points { background: #fef3c7; color: #92400e; }
    .badge-temp { background: #dbeafe; color: #1e40af; }

    .logout-btn {
        background: #f1f5f9;
        border: none;
        padding: 0.65rem 1.5rem;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        font-weight: 600;
        color: #475569;
        cursor: pointer;
        transition: all 0.2s;
    }

    .logout-btn:hover { background: #e2e8f0; }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: all 0.2s;
    }

    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    }

    .stat-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 1.25rem;
    }

    .stat-icon.green { background: #dcfce7; }
    .stat-icon.blue { background: #dbeafe; }
    .stat-icon.teal { background: #ccfbf1; }
    .stat-icon.purple { background: #f3e8ff; }
    .stat-icon.orange { background: #fed7aa; }

    .stat-value {
        font-family: 'Inter', sans-serif;
        font-size: 1.75rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }

    .stat-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .battery-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        height: auto;
        overflow: visible;
    }

    .card-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1.25rem;
    }

    .card-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
    }

    .card-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #94a3b8;
    }

    .profile-page-wrapper .stExpander {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }

    .profile-page-wrapper .stTextInput input,
    .profile-page-wrapper .stNumberInput input {
        border-radius: 10px !important;
    }

    .profile-page-wrapper [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: transparent !important;
        padding: 0 !important;
        gap: 0 !important;
    }

    .profile-page-wrapper [data-testid="column"] > [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    @media (max-width: 1200px) {
        .stats-grid { grid-template-columns: repeat(3, 1fr); }
    }

    @media (max-width: 768px) {
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .profile-header-card { flex-direction: column; text-align: center; }
        .device-badges { justify-content: center; }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="profile-page-container profile-page-wrapper">', unsafe_allow_html=True)

    header_col1, header_col2, header_col3 = st.columns([1.5, 5, 1.5])

    with header_col1:
        st.markdown('<div class="back-btn-col">', unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_from_profile"):
            st.session_state.page = "home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with header_col2:
        st.markdown('<h1 class="page-title-inline">User Stats</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="page-subtitle">
        Your device health &amp; sustainability dashboard
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="profile-header-card">
        <div class="profile-icon">📱</div>
        <div class="profile-details">
            <div class="device-name">{html_module.escape(st.session_state.device_data['device_name'])}</div>
            <div class="device-badges">
                <span class="badge badge-age">📅 {html_module.escape(st.session_state.device_data['device_age'])}</span>
                <span class="badge badge-points">🏆 {st.session_state.device_data['green_points']} Green Points</span>
                <span class="badge badge-temp">🌡️ {st.session_state.device_data['device_temp']}°C</span>
            </div>
        </div>
        <button class="logout-btn" onclick="alert('Logout functionality')">Logout</button>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🖊️ Edit Device Info"):
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

    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon green">🏆</div>
            <div class="stat-value">{st.session_state.device_data['green_points']:,}</div>
            <div class="stat-label">Green Points</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon blue">⚙️</div>
            <div class="stat-value">{st.session_state.device_data['cpu_score']}/100</div>
            <div class="stat-label">CPU Score</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon teal">🌿</div>
            <div class="stat-value">{st.session_state.device_data['eco_score']}/100</div>
            <div class="stat-label">Eco Score</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon purple">💾</div>
            <div class="stat-value">{st.session_state.device_data['ram_score']}/100</div>
            <div class="stat-label">RAM Score</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon orange">🌡️</div>
            <div class="stat-value">{st.session_state.device_data['device_temp']}°C</div>
            <div class="stat-label">Device Temp</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bottom Grid: Goals and Battery
    col_goals, col_battery = st.columns([1, 1.5])

    # ── FIXED: Use components.html() instead of st.markdown() ──
    with col_goals:
        total_goals = len(st.session_state.device_data['daily_goals'])
        completed = sum(1 for g in st.session_state.device_data['daily_goals'] if g['progress'] >= 80)
        avg_progress = sum(g['progress'] for g in st.session_state.device_data['daily_goals']) // total_goals
        on_track = sum(1 for g in st.session_state.device_data['daily_goals'] if g['progress'] >= 50)

        # Build goal items
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
                    <div class="goal-percentage {progress_class}">{goal['progress']}%</div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill {progress_class}" style="width: {goal['progress']}%"></div>
                </div>
            </div>
            """

        # Complete self-contained HTML with inline CSS
        goals_full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Inter', sans-serif;
                background: transparent;
                margin: 0;
                padding: 0;
            }}
            .goals-card {{
                background: white;
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            }}
            .card-header {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 1.25rem;
            }}
            .card-title {{
                font-size: 1.1rem;
                font-weight: 700;
                color: #0f172a;
            }}
            .card-subtitle {{
                font-size: 0.8rem;
                color: #94a3b8;
            }}
            .goal-item {{
                margin-bottom: 1rem;
            }}
            .goal-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.5rem;
            }}
            .goal-text {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.875rem;
                font-weight: 500;
                color: #334155;
            }}
            .goal-percentage {{
                font-size: 0.875rem;
                font-weight: 700;
            }}
            .goal-percentage.high {{ color: #059669; }}
            .goal-percentage.medium {{ color: #f59e0b; }}
            .goal-percentage.low {{ color: #ef4444; }}
            .progress-bar {{
                width: 100%;
                height: 8px;
                background: #f1f5f9;
                border-radius: 10px;
                overflow: hidden;
            }}
            .progress-fill {{
                height: 100%;
                border-radius: 10px;
            }}
            .progress-fill.high {{ background: linear-gradient(90deg, #10b981, #059669); }}
            .progress-fill.medium {{ background: linear-gradient(90deg, #f59e0b, #d97706); }}
            .progress-fill.low {{ background: linear-gradient(90deg, #ef4444, #dc2626); }}
            .summary-stats {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
                margin-top: 1.5rem;
                padding-top: 1.5rem;
                border-top: 1px solid #f1f5f9;
            }}
            .summary-item {{
                text-align: center;
            }}
            .summary-icon {{
                font-size: 1.5rem;
                margin-bottom: 0.25rem;
            }}
            .summary-value {{
                font-size: 1.5rem;
                font-weight: 800;
                color: #0f172a;
            }}
            .summary-label {{
                font-size: 0.75rem;
                font-weight: 600;
                color: #94a3b8;
            }}
        </style>
        </head>
        <body>
            <div class="goals-card">
                <div class="card-header">
                    <span style="font-size: 1.5rem;">🎯</span>
                    <div>
                        <div class="card-title">Current Device Stats</div>
                    </div>
                </div>
                {goal_items_html}

            </div>
        </body>
        </html>
        """

        # Calculate height dynamically based on number of goals
        card_height = 80 + (65 * total_goals) + 130 + 48
        components.html(goals_full_html, height=card_height, scrolling=False)

    with col_battery:
        with st.container():
            st.markdown("""
            <div class="battery-card">
                <div class="card-header">
                    <span style="font-size: 1.5rem;">🔋</span>
                    <div>
                        <div class="card-title">Battery Temperature</div>
                        <div class="card-subtitle">Temperature variation throughout the day</div>
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
                line={'color': '#10b981'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[
                        alt.GradientStop(color='#d1fae5', offset=0),
                        alt.GradientStop(color='#6ee7b7', offset=1)
                    ],
                    x1=1, x2=1, y1=1, y2=0
                ),
                interpolate='monotone'
            ).encode(
                x=alt.X('Time:N', axis=alt.Axis(labelAngle=0, title=None)),
                y=alt.Y('Temperature:Q', scale=alt.Scale(domain=[20, 50]),
                        axis=alt.Axis(title='Temperature (°C)', tickCount=5)),
                tooltip=['Time', 'Temperature']
            ).properties(
                height=280
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
            <div style="display: flex; justify-content: space-around; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #f1f5f9;">
                <div style="text-align: center;">
                    <span style="color: #10b981; font-weight: 600;">● Min: {min_temp}°C</span>
                </div>
                <div style="text-align: center;">
                    <span style="color: #f59e0b; font-weight: 600;">● Avg: {avg_temp}°C</span>
                </div>
                <div style="text-align: center;">
                    <span style="color: #ef4444; font-weight: 600;">● Max: {max_temp}°C</span>
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# ======================= REPAIR PAGE ========================
# ============================================================
elif st.session_state.page == "repair":

    # Back button styling for repair page
    st.markdown("""
    <style>

    /* Remove top spacing from the main container */
    [data-testid="stAppViewContainer"] > .main {
        padding-top: 0rem !important;
    }

    /* True viewport-fixed button */
    .repair-back-btn {
        position: fixed !important;
        top: 12px !important;
        left: 16px !important;
        z-index: 999999 !important;
    }

    /* Remove all internal spacing */
    .repair-back-btn * {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Style button */
    .repair-back-btn button {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        color: #475569 !important;
        border-radius: 10px !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        height: 40px !important;
        padding: 0 18px !important;
    }

    .repair-back-btn button:hover {
        background: #f8fafc !important;
        transform: translateX(-3px) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="repair-back-btn">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_from_repair"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    repair_page()

elif st.session_state.page == "ewaste":
    ewaste_page()
