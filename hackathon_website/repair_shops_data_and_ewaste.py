import streamlit as st
import requests
import time
from streamlit_js_eval import streamlit_js_eval
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ── */
    .stApp {
        background: linear-gradient(160deg, #f8fafc 0%, #f0fdf4 50%, #f8fafc 100%);
    }
    html, body, .stApp, .stMarkdown, .stMarkdown p, .stMarkdown span {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Hide Streamlit defaults ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: transparent;
    }

    iframe[title="streamlit_js_eval.streamlit_js_eval"] {
        height: 0px !important;
        border: none !important;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    /* ── Hero ── */
    .hero {
        background: linear-gradient(135deg, #10b981 0%, #059669 50%, #14b8a6 100%);
        border-radius: 20px;
        padding: 2.5rem 2rem 2.5rem;
        text-align: center;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 20px 60px rgba(16, 185, 129, 0.25);
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -60%;
        right: -30%;
        width: 80%;
        height: 160%;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero .badge {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 0.82rem;
        font-weight: 500;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.18);
        position: relative;
    }
    .hero h1 {
        font-family: 'Inter', sans-serif !important;
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        color: white !important;
        position: relative;
        letter-spacing: -0.02em;
    }
    .hero p {
        font-size: 1.05rem;
        opacity: 0.9;
        font-weight: 400;
        margin: 0;
        position: relative;
    }

    /* ── Info Alert ── */
    .alert-info {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #bfdbfe;
        border-left: 4px solid #3b82f6;
        border-radius: 14px;
        padding: 1rem 1.25rem;
        color: #1e40af;
        font-weight: 500;
        font-size: 0.92rem;
        display: flex;
        align-items: center;
        gap: 10px;
        line-height: 1.5;
    }

    /* ── Location Card ── */
    .loc-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .loc-card.success { border-left: 4px solid #22c55e; }
    .loc-card.waiting { border-left: 4px solid #f59e0b; }

    .loc-icon {
        width: 46px;
        height: 46px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        flex-shrink: 0;
    }
    .loc-icon.green  { background: #f0fdf4; }
    .loc-icon.yellow { background: #fffbeb; }

    .loc-label {
        font-size: 0.75rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .loc-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        letter-spacing: 1.5px;
    }
    .loc-sub {
        font-size: 0.88rem;
        color: #64748b;
    }
    .loc-badge {
        margin-left: auto;
        background: #22c55e;
        color: white;
        padding: 5px 14px;
        border-radius: 50px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    /* ── Features Row ── */
    .features-row {
        display: flex;
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    @media (max-width: 640px) {
        .features-row { flex-direction: column; }
    }
    .feature-card {
        flex: 1;
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    .feature-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    .feature-card .f-icon { font-size: 1.5rem; margin-bottom: 0.4rem; }
    .feature-card .f-title {
        font-weight: 600; font-size: 0.88rem; color: #1e293b;
    }
    .feature-card .f-desc {
        font-size: 0.78rem; color: #94a3b8; margin-top: 2px;
    }

    /* ── Button Override ── */
    .stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.85rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        width: 100% !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.01em;
    }
    .stButton > button:hover {
        box-shadow: 0 12px 35px rgba(16, 185, 129, 0.45) !important;
        transform: translateY(-1px);
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ── Results Header ── */
    .results-hdr {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .results-hdr h2 {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        flex: 1;
    }
    .count-badge {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 4px 14px;
        border-radius: 50px;
        font-size: 0.78rem;
        font-weight: 600;
    }

    /* ── Shop Card ── */
    .shop-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #10b981;
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.25s ease;
    }
    .shop-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        transform: translateY(-2px);
        border-left-color: #059669;
    }
    .shop-name {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .shop-addr {
        color: #64748b;
        font-size: 0.88rem;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    .shop-meta {
        margin-top: 6px;
        color: #475569;
        font-size: 0.84rem;
    }
    .maps-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-top: 12px;
        padding: 10px 24px;
        background: linear-gradient(135deg, #10b981, #059669);
        color: white !important;
        border-radius: 10px;
        text-decoration: none;
        font-size: 0.88rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.25);
    }
    .maps-btn:hover {
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        color: white !important;
        text-decoration: none;
        transform: translateY(-1px);
    }

    /* ── Alerts ── */
    .alert-warn {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
        border-radius: 14px;
        padding: 1rem 1.25rem;
        color: #92400e;
        font-weight: 500;
        font-size: 0.92rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .alert-err {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #fecaca;
        border-left: 4px solid #ef4444;
        border-radius: 14px;
        padding: 1rem 1.25rem;
        color: #991b1b;
        font-weight: 500;
        font-size: 0.92rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* ── Divider ── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 0.75rem 0;
    }

    /* ── Footer ── */
    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: #94a3b8;
        font-size: 0.82rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }

    /* ── Streamlit widget overrides ── */
    .stSpinner > div > div {
        border-top-color: #10b981 !important;
    }
    div[data-testid="stNotification"] {
        border-radius: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def repair_page():
    st.set_page_config(
        page_title="RepairFinder — Locate Repair Shops Near You",
        page_icon="🔧",
        layout="centered"
    )

    inject_custom_css()

    # ── Hero Section ──
    st.markdown("""
    <div class="hero">
        <div class="badge">📍 Location-based search</div>
        <h1>🔧 RepairFinder</h1>
        <p>Discover trusted mobile &amp; electronics repair shops near you — instantly</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Info Banner ──
    st.markdown("""
    <div class="alert-info">
        <span style="font-size:1.2rem;">🛡️</span>
        <span>We request your location to show nearby results. Click <strong>Allow</strong> when prompted. Your location is never stored or shared.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # Reverse Geocode (CACHED)
    # ──────────────────────────────────────────
    @st.cache_data(show_spinner=False)
    def get_address_from_coords(lat, lon):
        try:
            geolocator = Nominatim(user_agent="streamlit_location_app")
            location = geolocator.reverse((lat, lon), language="en", timeout=10)

            if location and "address" in location.raw:
                address = location.raw["address"]
                return {
                    "pincode": address.get("postcode"),
                    "city": address.get("city") or address.get("town") or address.get("village"),
                    "state": address.get("state"),
                    "country": address.get("country")
                }
        except (GeocoderTimedOut, GeocoderServiceError):
            return None
        return None

    # ──────────────────────────────────────────
    # Ask browser for location (ONLY ONCE)
    # ──────────────────────────────────────────
    if "user_location" not in st.session_state:
        location = streamlit_js_eval(
            js_expressions="""
            new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(
                    (pos) => resolve({
                        lat: pos.coords.latitude,
                        lon: pos.coords.longitude
                    }),
                    (err) => resolve(null)
                );
            })
            """,
            key="get_location",
            want_output=True
        )

        if location:
            st.session_state["user_location"] = location

    # ──────────────────────────────────────────
    # Reverse geocode & show location status
    # ──────────────────────────────────────────
    pincode = ""

    if "user_location" in st.session_state:
        coords = st.session_state["user_location"]
        lat = coords["lat"]
        lon = coords["lon"]

        address_data = get_address_from_coords(lat, lon)

        if address_data:
            st.session_state["user_address"] = address_data
            pincode = address_data["pincode"]
            city = address_data.get("city", "")
            state = address_data.get("state", "")

            st.markdown(f"""
            <div class="loc-card success">
                <div class="loc-icon green">✅</div>
                <div>
                    <div class="loc-label">Location Detected</div>
                    <div class="loc-value">{pincode}</div>
                    <div class="loc-sub">{city}{', ' + state if state else ''}</div>
                </div>
                <div class="loc-badge">GPS Active</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="loc-card waiting">
            <div class="loc-icon yellow">⏳</div>
            <div>
                <div class="loc-label">Waiting for Location</div>
                <div class="loc-sub">Please allow location access in your browser</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Feature Cards ──
    st.markdown("""
    <div class="features-row">
        <div class="feature-card">
            <div class="f-icon">📍</div>
            <div class="f-title">GPS Powered</div>
            <div class="f-desc">Auto-detect your area</div>
        </div>
        <div class="feature-card">
            <div class="f-icon">🛡️</div>
            <div class="f-title">Privacy First</div>
            <div class="f-desc">Location never stored</div>
        </div>
        <div class="feature-card">
            <div class="f-icon">⚡</div>
            <div class="f-title">Instant Results</div>
            <div class="f-desc">Real-time shop data</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # Search
    # ──────────────────────────────────────────
    if st.button("🔍  Search Nearby Repair Shops"):

        if not pincode:
            st.markdown("""
            <div class="alert-warn">
                <span>⚠️</span>
                <span>Location not detected yet. Please allow location access and try again.</span>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        geocode_url = (
            f"https://nominatim.openstreetmap.org/search"
            f"?postalcode={pincode}"
            f"&country=India"
            f"&format=json"
        )

        headers = {"User-Agent": "repair-app"}
        geo_response = requests.get(geocode_url, headers=headers).json()

        if not geo_response:
            st.markdown("""
            <div class="alert-err">
                <span>❌</span>
                <span>Invalid PIN code. Unable to search this area.</span>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        lat = geo_response[0]["lat"]
        lon = geo_response[0]["lon"]

        overpass_url = "https://overpass-api.de/api/interpreter"

        query = f"""
        [out:json];
        (
          node["shop"="mobile_phone"](around:3000,{lat},{lon});
          node["shop"="electronics"](around:3000,{lat},{lon});
          node["shop"="computer"](around:3000,{lat},{lon});
          node["shop"="appliance"](around:3000,{lat},{lon});
        );
        out;
        """

        with st.spinner("Searching for repair shops nearby..."):
            response = requests.post(overpass_url, data=query, timeout=30)

        if response.status_code != 200:
            st.markdown("""
            <div class="alert-err">
                <span>❌</span>
                <span>Service is busy. Please try again in a few seconds.</span>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        data = response.json()

        repair_keywords = ["repair", "service", "mobile", "iphone", "laptop", "computer", "electronics"]
        brand_exclusions = ["airtel", "vodafone", "jio", "lg", "vivo", "oppo", "realme"]

        reverse_cache = {}

        # Filter results
        filtered_places = []
        for place in data.get("elements", []):
            tags = place.get("tags", {})
            name = tags.get("name", "").strip()
            name_lower = name.lower()
            if not name:
                continue
            if not any(word in name_lower for word in repair_keywords):
                continue
            if any(brand in name_lower for brand in brand_exclusions):
                continue
            filtered_places.append(place)

        # Results Header
        st.markdown(f"""
        <div class="results-hdr">
            <span style="font-size:1.4rem;">📍</span>
            <h2>Repair Shops Near You</h2>
            <span class="count-badge">{len(filtered_places)} found</span>
        </div>
        """, unsafe_allow_html=True)

        if not filtered_places:
            st.markdown("""
            <div class="alert-warn">
                <span>😕</span>
                <span>No matching repair shops found in your area.</span>
            </div>
            """, unsafe_allow_html=True)
            return

        for place in filtered_places:
            tags = place["tags"]
            name = tags.get("name", "").strip()

            address_parts = [
                tags.get("addr:housenumber", ""),
                tags.get("addr:street", ""),
                tags.get("addr:suburb", ""),
                tags.get("addr:city", ""),
                tags.get("addr:postcode", ""),
            ]

            address = ", ".join(part for part in address_parts if part)

            lat_place = place.get("lat")
            lon_place = place.get("lon")

            if not address and lat_place and lon_place:
                coords_key = f"{lat_place},{lon_place}"

                if coords_key in reverse_cache:
                    address = reverse_cache[coords_key]
                else:
                    reverse_url = (
                        f"https://nominatim.openstreetmap.org/reverse"
                        f"?lat={lat_place}&lon={lon_place}&format=json"
                    )

                    reverse_response = requests.get(
                        reverse_url,
                        headers={"User-Agent": "repair-app"}
                    ).json()

                    address = reverse_response.get("display_name", "Address not available")
                    reverse_cache[coords_key] = address
                    time.sleep(1)

            # Create map link (only if coordinates are available)
            maps_link = f"https://www.google.com/maps?q={lat_place},{lon_place}" if lat_place and lon_place else ""

            # Build complete shop card HTML in one block
            if maps_link:
                shop_card_html = f"""
            <div class="shop-card">
                <div class="shop-name">{name}</div>
                <div class="shop-addr">📍 {address if address else 'Address not available'}</div>
                <a href="{maps_link}" target="_blank" class="maps-btn">📍 Open in Maps</a>
            </div>
            """
            else:
                shop_card_html = f"""
            <div class="shop-card">
                <div class="shop-name">{name}</div>
                <div class="shop-addr">📍 {address if address else 'Address not available'}</div>
            </div>
            """

            st.markdown(shop_card_html, unsafe_allow_html=True)
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div class="app-footer">
            Built with ❤️ using Streamlit · Data from OpenStreetMap
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    repair_page()


def ewaste_page():
    st.set_page_config(
        page_title="E-Waste Center Finder — Locate E-Waste Centers Near You",
        page_icon="♻️",
        layout="centered"
    )

    inject_custom_css()

    # ── Hero Section ──
    st.markdown("""
    <div class="hero">
        <h1>♻️ E-Waste Center Finder</h1>
        <p>Discover certified electronic waste recycling centers near you — dispose responsibly</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Info Banner ──
    st.markdown("""
    <div class="alert-info">
        <span style="font-size:1.2rem;">🛡️</span>
        <span>We request your location to show nearby results. Click <strong>Allow</strong> when prompted. Your location is never stored or shared.</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # Reverse Geocode (CACHED)
    # ──────────────────────────────────────────
    @st.cache_data(show_spinner=False)
    def get_address_from_coords(lat, lon):
        try:
            geolocator = Nominatim(user_agent="streamlit_location_app")
            location = geolocator.reverse((lat, lon), language="en", timeout=10)

            if location and "address" in location.raw:
                address = location.raw["address"]
                return {
                    "pincode": address.get("postcode"),
                    "city": address.get("city") or address.get("town") or address.get("village"),
                    "state": address.get("state"),
                    "country": address.get("country")
                }
        except (GeocoderTimedOut, GeocoderServiceError):
            return None
        return None

    # ──────────────────────────────────────────
    # Ask browser for location (ONLY ONCE)
    # ──────────────────────────────────────────
    if "user_location_ewaste" not in st.session_state:
        location = streamlit_js_eval(
            js_expressions="""
            new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(
                    (pos) => resolve({
                        lat: pos.coords.latitude,
                        lon: pos.coords.longitude
                    }),
                    (err) => resolve(null)
                );
            })
            """,
            key="get_location_ewaste",
            want_output=True
        )

        if location:
            st.session_state["user_location_ewaste"] = location

    # ──────────────────────────────────────────
    # Reverse geocode & show location status
    # ──────────────────────────────────────────
    pincode = ""

    if "user_location_ewaste" in st.session_state:
        coords = st.session_state["user_location_ewaste"]
        lat = coords["lat"]
        lon = coords["lon"]

        address_data = get_address_from_coords(lat, lon)

        if address_data:
            st.session_state["user_address_ewaste"] = address_data
            pincode = address_data["pincode"]
            city = address_data.get("city", "")
            state = address_data.get("state", "")

            st.markdown(f"""
            <div class="loc-card success">
                <div class="loc-icon green">✅</div>
                <div>
                    <div class="loc-label">Location Detected</div>
                    <div class="loc-value">{pincode}</div>
                    <div class="loc-sub">{city}{', ' + state if state else ''}</div>
                </div>
                <div class="loc-badge">GPS Active</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="loc-card waiting">
            <div class="loc-icon yellow">⏳</div>
            <div>
                <div class="loc-label">Waiting for Location</div>
                <div class="loc-sub">Please allow location access in your browser</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Feature Cards ──
    st.markdown("""
    <div class="features-row">
        <div class="feature-card">
            <div class="f-icon">🏢</div>
            <div class="f-title">Certified Centers</div>
            <div class="f-desc">Authorized recyclers</div>
        </div>
        <div class="feature-card">
            <div class="f-icon">♻️</div>
            <div class="f-title">Eco-Friendly</div>
            <div class="f-desc">Proper disposal</div>
        </div>
        <div class="feature-card">
            <div class="f-icon">📍</div>
            <div class="f-title">20km Radius</div>
            <div class="f-desc">Extended search area</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ──────────────────────────────────────────
    # Search
    # ──────────────────────────────────────────
    if st.button("🔍  Find E-Waste Centers Nearby"):

        if not pincode:
            st.markdown("""
            <div class="alert-warn">
                <span>⚠️</span>
                <span>Location not detected yet. Please allow location access and try again.</span>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        geocode_url = (
            f"https://nominatim.openstreetmap.org/search"
            f"?postalcode={pincode}"
            f"&country=India"
            f"&format=json"
        )

        headers = {"User-Agent": "ewaste-app"}
        geo_response = requests.get(geocode_url, headers=headers).json()

        if not geo_response:
            st.markdown("""
            <div class="alert-err">
                <span>❌</span>
                <span>Invalid PIN code. Unable to search this area.</span>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        lat = geo_response[0]["lat"]
        lon = geo_response[0]["lon"]

        overpass_url = "https://overpass-api.de/api/interpreter"

        # More targeted query for e-waste centers
        query = f"""
        [out:json];
        (
          node["amenity"="recycling"]["recycling:electronic_waste"="yes"](around:20000,{lat},{lon});
          way["amenity"="recycling"]["recycling:electronic_waste"="yes"](around:20000,{lat},{lon});
          node["amenity"="waste_transfer_station"](around:20000,{lat},{lon});
          way["amenity"="waste_transfer_station"](around:20000,{lat},{lon});
          node["amenity"="civic_amenity_site"](around:20000,{lat},{lon});
          way["amenity"="civic_amenity_site"](around:20000,{lat},{lon});
        );
        out center;
        """

        with st.spinner("Searching for e-waste centers nearby..."):
            response = requests.post(overpass_url, data=query, timeout=30)

        if response.status_code != 200:
            st.markdown("""
            <div class="alert-err">
                <span>❌</span>
                <span>Service is busy. Please try again in a few seconds.</span>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

        data = response.json()

        # Known e-waste companies and organizations in India
        known_ewaste_companies = [
            "saahas", "e-parisaraa", "attero", "exigo", "greenscape",
            "eco", "cerebra", "环保", "तत्सम", "municipal", "corporation",
            "bbmp", "nagar", "panchayat", "government", "civic"
        ]

        # Strong e-waste keywords
        strong_ewaste_keywords = [
            "e-waste", "ewaste", "e waste", "electronic waste",
            "electronics recycling", "weee", "pcb recycling",
            "collection center", "drop center", "take back",
            "recycling center", "recycling facility"
        ]

        # Exclude personal/individual names patterns
        exclude_patterns = [
            "shop", "'s shop", "stores", "store", "mart", "traders",
            "enterprises", "agency", "agencies"
        ]

        reverse_cache = {}

        # Filter results with strict criteria
        filtered_places = []
        for place in data.get("elements", []):
            tags = place.get("tags", {})
            name = tags.get("name", "").strip()

            # Skip if no name
            if not name:
                continue

            name_lower = name.lower()

            # EXCLUSION FILTERS (reject these immediately)
            # 1. Exclude single-word names (likely personal shops)
            word_count = len(name.split())
            if word_count <= 1:
                continue

            # 2. Exclude names with personal shop patterns
            if any(pattern in name_lower for pattern in exclude_patterns):
                # Unless it also has strong e-waste keywords
                if not any(keyword in name_lower for keyword in strong_ewaste_keywords):
                    continue

            # 3. Exclude names that look like personal names (contains common suffixes)
            personal_name_indicators = ["'s", "kumar", "raj", "reddy", "rao", "sharma", "singh"]
            has_personal_indicator = any(indicator in name_lower for indicator in personal_name_indicators)

            if has_personal_indicator:
                # Only keep if it has strong e-waste keywords
                if not any(keyword in name_lower for keyword in strong_ewaste_keywords):
                    continue

            # INCLUSION FILTERS (must match at least one)
            # 1. Has explicit e-waste tag
            has_ewaste_tag = tags.get("recycling:electronic_waste") == "yes"

            # 2. Has strong e-waste keywords
            has_strong_keyword = any(keyword in name_lower for keyword in strong_ewaste_keywords)

            # 3. Is a known e-waste company/organization
            is_known_company = any(company in name_lower for company in known_ewaste_companies)

            # 4. Is a civic/municipal facility
            is_civic = tags.get("amenity") in ["waste_transfer_station", "civic_amenity_site"]
            is_municipal = any(
                term in name_lower for term in ["municipal", "corporation", "bbmp", "civic", "government"])

            # Accept if passes any strong criteria
            if has_ewaste_tag or has_strong_keyword or (is_known_company and word_count >= 2) or (
                    is_civic or is_municipal):
                filtered_places.append(place)

        # Results Header
        st.markdown(f"""
        <div class="results-hdr">
            <span style="font-size:1.4rem;">♻️</span>
            <h2>E-Waste Centers Near You</h2>
            <span class="count-badge">{len(filtered_places)} found</span>
        </div>
        """, unsafe_allow_html=True)

        if not filtered_places:
            st.markdown("""
            <div class="alert-warn">
                <span>😕</span>
                <span>No certified e-waste centers found in your area.</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background: white; border-radius: 12px; padding: 1.5rem; margin-top: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                <h3 style="color: #0f172a; margin-top: 0;">💡 Alternative Options:</h3>
                <ul style="color: #475569; line-height: 1.8;">
                    <li><strong>Contact BBMP/Local Municipality:</strong> Call your local municipal corporation for authorized e-waste collection points</li>
                    <li><strong>Brand Take-Back Programs:</strong> Many electronics brands (Apple, Samsung, Dell, HP) offer e-waste pickup services</li>
                    <li><strong>Known E-Waste Companies in Bangalore:</strong>
                        <ul>
                            <li>Saahas Zero Waste - <a href="https://saahaszerowaste.com" target="_blank" style="color: #10b981;">saahaszerowaste.com</a></li>
                            <li>E-Parisaraa Pvt Ltd - Authorized e-waste recycler</li>
                            <li>Cerebra Integrated Technologies</li>
                        </ul>
                    </li>
                    <li><strong>Check CPCB Website:</strong> Central Pollution Control Board maintains a list of authorized e-waste dismantlers</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            return

        # Info banner about verification
        st.markdown("""
        <div class="alert-info">
            <span style="font-size:1.2rem;">ℹ️</span>
            <span><strong>Important:</strong> Please verify that the center is authorized and currently operational before visiting. Call ahead to confirm they accept your type of electronics.</span>
        </div>
        """, unsafe_allow_html=True)

        for place in filtered_places:
            tags = place["tags"]
            name = tags.get("name", "E-Waste Recycling Center").strip()

            address_parts = [
                tags.get("addr:housenumber", ""),
                tags.get("addr:street", ""),
                tags.get("addr:suburb", ""),
                tags.get("addr:city", ""),
                tags.get("addr:postcode", ""),
            ]

            address = ", ".join(part for part in address_parts if part)

            # Handle both nodes and ways (ways have center coordinates)
            if place["type"] == "way":
                lat_place = place.get("center", {}).get("lat")
                lon_place = place.get("center", {}).get("lon")
            else:
                lat_place = place.get("lat")
                lon_place = place.get("lon")

            if not address and lat_place and lon_place:
                coords_key = f"{lat_place},{lon_place}"

                if coords_key in reverse_cache:
                    address = reverse_cache[coords_key]
                else:
                    reverse_url = (
                        f"https://nominatim.openstreetmap.org/reverse"
                        f"?lat={lat_place}&lon={lon_place}&format=json"
                    )

                    reverse_response = requests.get(
                        reverse_url,
                        headers={"User-Agent": "ewaste-app"}
                    ).json()

                    address = reverse_response.get("display_name", "Address not available")
                    reverse_cache[coords_key] = address
                    time.sleep(1)

            # Create map link (only if coordinates are available)
            maps_link = f"https://www.google.com/maps?q={lat_place},{lon_place}" if lat_place and lon_place else ""

            # Build complete shop card HTML in one block
            if maps_link:
                center_card_html = f"""
            <div class="shop-card">
                <div class="shop-name">{name}</div>
                <div class="shop-addr">📍 {address if address else 'Address not available'}</div>
                <a href="{maps_link}" target="_blank" class="maps-btn">📍 Open in Maps</a>
            </div>
            """
            else:
                center_card_html = f"""
            <div class="shop-card">
                <div class="shop-name">{name}</div>
                <div class="shop-addr">📍 {address if address else 'Address not available'}</div>
            </div>
            """

            st.markdown(center_card_html, unsafe_allow_html=True)
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div class="app-footer">
            Built with ❤️ using Streamlit · Data from OpenStreetMap
        </div>
        """, unsafe_allow_html=True)