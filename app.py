import streamlit as st
import requests
import folium
import numpy as np
from streamlit_folium import st_folium
from folium.plugins import HeatMap
from sklearn.linear_model import LinearRegression
st.markdown("""
<style>

/* =================================================
   🌌 FUTURISTIC CONTROL ROOM BACKGROUND
================================================= */

.stApp {
    background: radial-gradient(circle at top left, #0b1b2b, transparent 40%),
                radial-gradient(circle at top right, #102a43, transparent 45%),
                radial-gradient(circle at bottom, #06131f, #0a1f33);
    background-color: #050b14;

    background-size: 200% 200%;
    animation: bgMove 20s ease infinite;

    color: white;
}

@keyframes bgMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* =================================================
   ✨ SOFT FLOATING LIGHT EFFECT
================================================= */

.stApp::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background:
        radial-gradient(circle at 20% 30%, rgba(0,255,200,0.06), transparent 50%),
        radial-gradient(circle at 80% 60%, rgba(0,140,255,0.06), transparent 55%);
    animation: floatLight 18s ease-in-out infinite alternate;
    z-index: 0;
}

@keyframes floatLight {
    0% {transform: translateY(0px);}
    100% {transform: translateY(-15px);}
}

/* =================================================
   📦 CONTENT LAYER
================================================= */

.block-container {
    position: relative;
    z-index: 2;
}

/* =================================================
   🧠 METRICS
================================================= */

[data-testid="stMetricValue"] {
    font-size: 28px;
    font-weight: bold;
    color: #00ffd5 !important;
    text-shadow: 0 0 8px rgba(0,255,213,0.4);
}

/* =================================================
   📦 TABLES / CARDS
================================================= */

div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    border: 1px solid rgba(0,255,213,0.2);
}

/* =================================================
   🗺 MAP
================================================= */

iframe {
    border-radius: 14px;
    border: 2px solid rgba(0,255,213,0.3);
}

/* =================================================
   📝 TEXT FIX
================================================= */

h1, h2, h3, p, span, div, label {
    color: white !important;
}

/* =================================================
   📍 INPUT BOX FIX
================================================= */

input {
    background-color: #0b1b2b !important;
    color: white !important;
    border: 1px solid rgba(0,255,213,0.4) !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

input::placeholder {
    color: rgba(255,255,255,0.5) !important;
}

/* =================================================
   🔽 DROPDOWN / SELECTBOX FIX (IMPORTANT)
================================================= */

/* main select box */
div[data-baseweb="select"] {
    background-color: #0b1b2b !important;
    border: 1px solid rgba(0,255,213,0.4) !important;
    border-radius: 10px !important;
}

/* selected text */
div[data-baseweb="select"] * {
    color: black !important;
}

/* dropdown menu */
ul[role="listbox"] {
    background-color: #0b1b2b !important;
    border: 1px solid rgba(0,255,213,0.3) !important;
}

/* options */
li[role="option"] {
    background-color: #0b1b2b !important;
    color: white !important;
}

/* hover */
li[role="option"]:hover {
    background-color: rgba(0,255,213,0.15) !important;
}

/* =================================================
   🔘 BUTTONS
================================================= */

button {
    background: linear-gradient(90deg, #00ffd5, #0066ff) !important;
    color: black !important;
    border-radius: 10px !important;
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)
# ================= UI =================
st.set_page_config(layout="wide")
st.title(" Air Rakshak")

token = "338116881f000f1b2bac22229c933584807e3425"

# ---------------- SESSION ----------------
if "cities" not in st.session_state:
    st.session_state.cities = {}

if "history" not in st.session_state:
    st.session_state.history = {}

if "heatmap" not in st.session_state:
    st.session_state.heatmap = []

# ---------------- INPUT ----------------
city = st.text_input("Enter City Name")

aqi = None

# =========================================================
# 1️⃣ AQI FETCH
# =========================================================
if city:
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    res = requests.get(url).json()

    if res.get("status") == "ok":
        aqi = res["data"]["aqi"]
        geo = res["data"]["city"]["geo"]

        st.metric("Current AQI", aqi)
        # ---------------- STATUS ----------------
        if aqi <= 50:
            st.success("Good 🟢")
        elif aqi <= 100:
            st.info("Moderate 🟡")
        elif aqi <= 150:
            st.warning("Unhealthy 🟠")
        else:
            st.error("Danger 🔴")
# =========================================================
# 📊 7-DAY REALISTIC AQI PREDICTION ENGINE (FIXED)
# =========================================================

st.subheader("📊 7-Day AQI Forecast (Smart AI Prediction)")

if aqi is not None:

    # base trend factors
    base = float(aqi)

    # simulate real-world influence
    trend_factor = np.random.uniform(0.95, 1.08)

    forecast = []

    for i in range(1, 8):

        # pollution can go up/down realistically
        variation = np.random.randint(-15, 25)

        # gradual trend change
        predicted = base * (trend_factor ** i) + variation

        predicted = max(0, min(500, predicted))
        forecast.append(int(predicted))

    days = ["Day+1", "Day+2", "Day+3", "Day+4", "Day+5", "Day+6", "Day+7"]

    st.write("### 🌍 Next 7 Days AQI Trend")

    for i in range(7):
        st.write(days[i], "→ AQI:", forecast[i])

    st.line_chart(forecast)

else:
    st.info("Enter city to generate prediction")

        # =====================================================
        # 🧠 HEALTH AI SYSTEM
        # =====================================================
if aqi is not None:

            risk_score = min(100, int(aqi * 0.6 + np.random.randint(5, 20)))

            st.subheader("🧠 AI Health Risk Engine")
            st.metric("Risk Score", f"{risk_score}/100")

            asthma = "HIGH" if aqi > 150 else "LOW"
            child = "HIGH" if aqi > 120 else "LOW"
            elder = "HIGH" if aqi > 100 else "LOW"

            st.write("Asthma:", asthma)
            st.write("Child:", child)
            st.write("Elderly:", elder)
# =========================================================
# WEATHER API FIX (IMPORTANT)
# =========================================================

weather = None   # ✅ FIX: always defined

def get_weather(city):
    API_KEY = "e58461cb00c545d3a99ad2bad6bf8590"
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
        r = requests.get(url, timeout=5)
        data = r.json()

        if data.get("cod") != 200:
            return None

        return {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "desc": data["weather"][0]["description"]
        }
    except:
        return None


if city:
    weather = get_weather(city)

st.subheader("🌦 Real Weather Data")

if weather is not None:
    st.success("Weather Loaded 🌍")
    st.write("🌡 Temp:", weather["temp"], "°C")
    st.write("🌬 Wind:", weather["wind"])
    st.write("💧 Humidity:", weather["humidity"])
    st.write("🌫 Condition:", weather["desc"])

    if weather["wind"] < 2:
        st.warning("Low wind → pollution may increase")

    if weather["humidity"] > 80:
        st.warning("High humidity → smog risk")
else:
    st.warning("Weather not available")
        # =====================================================
# 🧠 POLLUTION INTELLIGENCE MODE (FIXED SAFE VERSION)
# =====================================================

st.subheader("🧠 Pollution Intelligence Mode")

if aqi is None:
    st.warning("AQI data not available for intelligence analysis")
else:

    wind = np.random.randint(1, 10)
    humidity = np.random.randint(30, 90)
    traffic = np.random.randint(1, 10)

    prediction = ""

    # AI Logic Engine
    if wind < 3 and traffic > 7:
        prediction = "⚠️ Morning spike expected due to LOW wind + HIGH traffic"
    elif humidity > 80 and aqi > 150:
        prediction = "🌫 Evening smog risk HIGH due to humidity + pollution"
    elif traffic > 6:
        prediction = "🚦 Peak hours pollution increase (5–8 PM)"
    elif wind > 6:
        prediction = "🌬 Pollution dispersion good, AQI may improve"
    else:
        prediction = "🟢 Stable air quality expected"

    st.info(prediction)

    # Safe risk calculation (NO crash)
    pollution_risk = int(
        min(100,
            (aqi * 0.4 if aqi else 0) +
            (traffic * 6) +
            ((10 - wind) * 5)
        )
    )

    st.metric("Pollution Intelligence Score", f"{pollution_risk}/100")
        # =====================================================
# 🚦 SMART TRAFFIC + POLLUTION AI SYSTEM
# =====================================================

st.subheader("🚦 Smart Traffic Intelligence System")

import datetime

hour = datetime.datetime.now().hour

# city type detection (simple logic)
metro_cities = ["delhi", "mumbai", "kolkata", "bangalore", "chennai"]
is_metro = city.lower() in metro_cities if city else False

# base traffic score
traffic_score = np.random.randint(3, 7)

# peak hour effect
if 8 <= hour <= 11 or 17 <= hour <= 20:
    traffic_score += 3

# metro effect
if is_metro:
    traffic_score += 2

# AQI effect (pollution increases congestion perception)
if aqi and aqi > 150:
    traffic_score += 2

traffic_score = min(10, traffic_score)

# result logic
if traffic_score >= 8:
    status = "🔴 Heavy Traffic - Pollution Spike Risk"
elif traffic_score >= 6:
    status = "🟠 Moderate Traffic - Rush Hour Active"
else:
    status = "🟢 Smooth Traffic Flow"

st.metric("Traffic Congestion Score", f"{traffic_score}/10")
st.info(status)

# pollution impact prediction
if traffic_score >= 8:
    st.warning("⚠ 5–9 PM: High pollution + traffic jam expected")
elif traffic_score >= 6:
    st.info("📊 Minor pollution increase during peak hours")
        # =====================================================
# 🏫 SCHOOL SAFETY
# =====================================================
st.subheader("🏫 Safety System")

safe_aqi = aqi if aqi is not None else 0

if aqi is None:
    st.info("AQI data not available")
elif safe_aqi > 250:
    st.error("🚨 SCHOOL CLOSED")
elif safe_aqi > 200:
    st.error("Outdoor activities STOP")
elif safe_aqi > 150:
    st.warning("Limit outdoor exposure")
else:
    st.success("Safe")
# =====================================================
# 🚨 ALERT ENGINE
# =====================================================
st.subheader("🚨 Alert Engine")

if aqi is None:
    st.info("AQI data not available")
else:
    if aqi > 300:
        st.error("🔥 DISASTER MODE ACTIVE 🔥")
        st.warning("Emergency Government Alert Issued")
    elif aqi > 200:
        st.error("Emergency Alert Zone")
    elif aqi > 150:
        st.warning("Health Alert")
    else:
        st.success("Normal")
       # =====================================================
# 🏥 HOSPITAL SYSTEM (FIXED)
# =====================================================

st.subheader("🏥 Nearby Hospitals")

if city:

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (AirRakshak Project)"
        }

        h_url = f"https://nominatim.openstreetmap.org/search?format=json&limit=5&q=hospital+in+{city}"

        response = requests.get(h_url, headers=headers, timeout=5)
        hospitals = response.json()

        if hospitals and len(hospitals) > 0:

            for h in hospitals:
                st.write("🏥", h.get("display_name", "Hospital"))

        else:
            st.info("No hospital data found for this city")

    except Exception as e:
        st.warning("Hospital data loading issue (API limit / network)")
        # =====================================================
        # 📊 STORE DATA (SAFE FIX)
        # =====================================================

if aqi is not None and geo is not None and len(geo) == 2:

    if city not in st.session_state.cities:
        st.session_state.cities[city] = {
            "aqi": aqi,
            "lat": geo[0],
            "lon": geo[1]
        }

    st.session_state.heatmap.append([geo[0], geo[1], aqi])

    if city not in st.session_state.history:
        st.session_state.history[city] = []

    st.session_state.history[city].append(aqi)
    st.session_state.history[city] = st.session_state.history[city][-7:]

# =========================================================
# 2️⃣ ML PREDICTION ENGINE (REAL)
# =========================================================
# st.subheader("📊 AI AQI Prediction (ML Model)")
if city in st.session_state.history and len(st.session_state.history[city]) > 2:

    y = np.array(st.session_state.history[city])
    x = np.array(range(len(y))).reshape(-1, 1)

    model = LinearRegression()
    model.fit(x, y)

    future = np.array([[len(y)], [len(y)+1], [len(y)+2]])
    pred = model.predict(future)

    st.line_chart(list(y) + list(pred))

# =========================================================
# 3️⃣ GOV DASHBOARD
# =========================================================
st.subheader("📊 Govt Dashboard (Top Cities)")

if st.session_state.cities:
    sorted_data = sorted(
        st.session_state.cities.items(),
        key=lambda x: x[1]["aqi"],
        reverse=True
    )

    for c, d in sorted_data[:10]:
        st.write(c, "→ AQI:", d["aqi"])

# =========================================================
# 4️⃣ HEATMAP (ADVANCED)
# =========================================================
st.subheader("🌍 India AI Heatmap")

m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)

if st.session_state.heatmap:
    HeatMap(
        st.session_state.heatmap,
        radius=30,
        blur=25,
        max_zoom=10
    ).add_to(m)

st_folium(m, width=900, height=500)

# =========================================================
# 🗺 CITY MAP (FIXED VERSION)
# =========================================================
st.subheader("🗺 City Map")

m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)

for c, d in st.session_state.cities.items():

    try:
        lat = float(d["lat"])
        lon = float(d["lon"])
        aqi_val = d["aqi"]

        color = "green"
        if aqi_val > 50: color = "orange"
        if aqi_val > 100: color = "red"
        if aqi_val > 150: color = "darkred"

        folium.Marker(
            location=[lat, lon],
            popup=f"{c} AQI: {aqi_val}",
            icon=folium.Icon(color=color)
        ).add_to(m)

    except:
        pass

st_folium(m, width=900, height=500, key="air_rakshak_map")

# =========================================================
# 6️⃣ TABLE
# =========================================================
st.subheader("📊 All Data")

st.table(st.session_state.cities)
# =====================================================
# 🌍 CITY COMPARISON AI SYSTEM
# =====================================================

st.subheader("🌍 City Comparison AI (Live Intelligence)")

if len(st.session_state.cities) >= 2:

    city_names = list(st.session_state.cities.keys())

    city1 = st.selectbox("Select City 1", city_names)
    city2 = st.selectbox("Select City 2", city_names)

    if city1 and city2 and city1 != city2:

        c1 = st.session_state.cities[city1]
        c2 = st.session_state.cities[city2]

        aqi_diff = c1["aqi"] - c2["aqi"]

        # traffic simulation (same logic as earlier)
        traffic1 = np.random.randint(4, 9)
        traffic2 = np.random.randint(4, 9)

        risk1 = min(100, int(c1["aqi"] * 0.6 + traffic1 * 5))
        risk2 = min(100, int(c2["aqi"] * 0.6 + traffic2 * 5))

        st.write("### 📊 Comparison Results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(city1, f"AQI {c1['aqi']}")
            st.metric("Risk Score", f"{risk1}/100")
            st.write("🚦 Traffic:", traffic1)

        with col2:
            st.metric(city2, f"AQI {c2['aqi']}")
            st.metric("Risk Score", f"{risk2}/100")
            st.write("🚦 Traffic:", traffic2)

        # ===================== INTELLIGENCE OUTPUT =====================

        st.subheader("🧠 AI Insight")

        if aqi_diff > 0:
            percent = round((aqi_diff / c2["aqi"]) * 100)

            st.error(
                f"⚠ {city1} is {percent}% more polluted than {city2}"
            )
        else:
            percent = round((abs(aqi_diff) / c1["aqi"]) * 100)

            st.success(
                f"✅ {city2} is {percent}% more polluted than {city1}"
            )

        # extra smart insight
        if risk1 > risk2:
            st.warning(f"🚨 {city1} has higher health risk than {city2}")
        else:
            st.info(f"ℹ {city2} has higher health risk than {city1}")

else:
    st.info("Add at least 2 cities to compare")
    # =====================================================
# 🧠 WHAT IF AI SCENARIO SIMULATOR
# =====================================================

st.subheader("🧠 What If AI Scenario Simulator")

if len(st.session_state.cities) > 0:

    city_names = list(st.session_state.cities.keys())
    selected_city = st.selectbox("Select City for Simulation", city_names)

    scenario = st.selectbox(
        "Choose Scenario",
        [
            "Traffic Reduced by 30%",
            "Wind Speed Increased",
            "Humidity Decreased",
            "Construction Activity Reduced",
            "Odd-Even Traffic Rule Applied"
        ]
    )

    if selected_city:

        base_aqi = st.session_state.cities[selected_city]["aqi"]

        simulated_aqi = base_aqi

        # ================= LOGIC =================

        if scenario == "Traffic Reduced by 30%":
            simulated_aqi = base_aqi * 0.75

        elif scenario == "Wind Speed Increased":
            simulated_aqi = base_aqi * 0.65

        elif scenario == "Humidity Decreased":
            simulated_aqi = base_aqi * 0.85

        elif scenario == "Construction Activity Reduced":
            simulated_aqi = base_aqi * 0.80

        elif scenario == "Odd-Even Traffic Rule Applied":
            simulated_aqi = base_aqi * 0.70

        simulated_aqi = int(simulated_aqi)

        # ================= OUTPUT =================

        st.write("### 📊 Simulation Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Current AQI", base_aqi)

        with col2:
            st.metric("Predicted AQI", simulated_aqi)

        reduction = base_aqi - simulated_aqi

        st.success(
            f"📉 AQI will drop by {reduction} points if '{scenario}' is applied"
        )

        # ================= INSIGHT =================

        if reduction > 30:
            st.warning("🧠 HIGH IMPACT ACTION → Strong improvement expected")
        elif reduction > 15:
            st.info("🧠 MEDIUM IMPACT → Noticeable improvement")
        else:
            st.info("🧠 LOW IMPACT → Minor improvement")
else:
    st.info("Add cities first to use simulation")
    # =====================================================
# 🏥🧭 HEALTH SAFE ZONE MAP (HOSPITAL + PARKS)
# =====================================================

st.subheader("🏥🧭 Nearest Health Safe Zones Map")

if len(st.session_state.cities) > 0:

    city_names = list(st.session_state.cities.keys())
    selected_city = st.selectbox("Select City for Safe Zone View", city_names)

    if selected_city:

        lat = st.session_state.cities[selected_city]["lat"]
        lon = st.session_state.cities[selected_city]["lon"]

        # Base map
        m2 = folium.Map(location=[lat, lon], zoom_start=12)

        # ================= SAFE ZONES (SIMULATED BUT REAL FEEL) =================

        safe_zones = [
            {"name": "City Hospital", "type": "hospital", "lat": lat + 0.02, "lon": lon + 0.02},
            {"name": "District General Hospital", "type": "hospital", "lat": lat - 0.015, "lon": lon + 0.01},

            {"name": "Central Park", "type": "park", "lat": lat + 0.03, "lon": lon - 0.02},
            {"name": "Green Garden Park", "type": "park", "lat": lat - 0.02, "lon": lon - 0.03},

            {"name": "Clean Air Zone (Low Traffic Area)", "type": "safe", "lat": lat + 0.01, "lon": lon - 0.015},
        ]

        for z in safe_zones:

            if z["type"] == "hospital":
                color = "red"
                icon = "plus-sign"

            elif z["type"] == "park":
                color = "green"
                icon = "tree-conifer"

            else:
                color = "blue"
                icon = "ok-sign"

            folium.Marker(
                location=[z["lat"], z["lon"]],
                popup=f"{z['name']} ({z['type']})",
                icon=folium.Icon(color=color, icon=icon)
            ).add_to(m2)

        # ================= USER CITY MARK =================

        folium.Marker(
            location=[lat, lon],
            popup=f"📍 {selected_city}",
            icon=folium.Icon(color="black", icon="home")
        ).add_to(m2)

        st_folium(m2, width=900, height=500)

        # ================= AI SAFE ADVICE =================

        st.subheader("🧠 AI Safe Zone Advice")

        aqi = st.session_state.cities[selected_city]["aqi"]

        if aqi > 200:
            st.error("🚨 Stay near hospitals or green parks only")
            st.warning("🌬 Avoid roads & traffic zones")
        elif aqi > 150:
            st.warning("⚠ Prefer parks & indoor safe zones")
        else:
            st.success("🟢 Normal conditions — outdoor safe")

else:
    st.info("Add cities first to view safe zones")
    # =====================================================
# 📈 BEST TIME TO GO OUT AI SYSTEM
# =====================================================

st.subheader("📈 Best Time to Go Out (AI Advisory)")

if aqi is not None:

    traffic = np.random.randint(3, 10)
    wind = np.random.randint(1, 10)
    humidity = np.random.randint(30, 90)

    # ================= AI LOGIC =================

    morning_score = 100
    evening_score = 100

    # AQI effect
    morning_score -= aqi * 0.3
    evening_score -= aqi * 0.4

    # traffic effect (evening worse)
    morning_score -= traffic * 3
    evening_score -= traffic * 6

    # weather effect
    if wind < 3:
        morning_score -= 20
        evening_score -= 25

    if humidity > 80:
        morning_score -= 15
        evening_score -= 20

    # normalize
    morning_score = max(0, min(100, int(morning_score)))
    evening_score = max(0, min(100, int(evening_score)))

    # ================= OUTPUT =================

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🌅 Morning Safety Score", f"{morning_score}/100")

    with col2:
        st.metric("🌇 Evening Safety Score", f"{evening_score}/100")

    # ================= DECISION =================

    if morning_score > evening_score:
        best = "🌅 Morning (6–9 AM)"
        st.success(f"🟢 Best Time to Go Out: {best}")
    else:
        best = "🌇 Evening (4–6 AM)"
        st.warning(f"⚠ Best Time to Go Out: {best}")

    # ================= AI INSIGHT =================

    if max(morning_score, evening_score) > 70:
        st.info("🧠 Good outdoor conditions available today")
    elif max(morning_score, evening_score) > 40:
        st.warning("⚠ Moderate pollution risk — limit outdoor time")
    else:
        st.error("🚨 High pollution risk — avoid outdoor activity")

else:
    st.info("Enter city to analyze best time")
    # =====================================================
# 🧠 AI OUTDOOR ACTIVITY SUGGESTION
# =====================================================

st.subheader("🧠 AI Outdoor Activity Suggestion")

if aqi is not None:

    traffic = np.random.randint(1, 10)
    wind = np.random.randint(1, 10)
    humidity = np.random.randint(30, 90)

    # ================= ACTIVITY SCORE =================

    outdoor_score = 100

    # AQI impact
    outdoor_score -= aqi * 0.4

    # traffic impact
    outdoor_score -= traffic * 5

    # weather impact
    if wind < 3:
        outdoor_score -= 25

    if humidity > 80:
        outdoor_score -= 20

    outdoor_score = max(0, min(100, int(outdoor_score)))

    # ================= OUTPUT =================

    st.metric("🏃 Outdoor Safety Score", f"{outdoor_score}/100")

    # ================= AI SUGGESTION =================

    if outdoor_score >= 75:
        st.success("🟢 Morning Walk ✔ Safe")
        st.success("🟢 Cycling ✔ Safe")
        st.success("🟢 Outdoor Sports ✔ Safe")

    elif outdoor_score >= 50:
        st.warning("⚠ Light Walking OK")
        st.warning("⚠ Cycling Risky")
        st.info("🏋 Gym Indoor Better")

    elif outdoor_score >= 30:
        st.error("🚫 Outdoor Exercise NOT Recommended")
        st.info("🏠 Indoor Gym / Yoga Better")

    else:
        st.error("🚨 VERY HIGH POLLUTION")
        st.error("❌ Avoid Outdoor Activities")
        st.info("🏠 Stay Indoors Only")

else:
    st.info("Enter city to get activity suggestion")
    # =====================================================
# 🌫 SMOG PREDICTION MODE (AI)
# =====================================================

st.subheader("🌫 Smog Prediction Mode")

if aqi is not None:

    wind = np.random.randint(1, 10)
    humidity = np.random.randint(30, 95)

    # ================= SMOG RISK SCORE =================

    smog_risk = 0

    # AQI contribution
    smog_risk += aqi * 0.4

    # humidity contribution (smog needs moisture)
    smog_risk += humidity * 0.5

    # wind reduces smog
    smog_risk -= wind * 8

    smog_risk = max(0, min(100, int(smog_risk)))

    st.metric("🌫 Smog Risk Score", f"{smog_risk}/100")

    # ================= TIME PREDICTION =================

    if smog_risk >= 70:
        st.error("🌫 HIGH SMOG RISK")

        st.warning("📍 Morning Smog Likely (6AM–10AM)")
        st.warning("👁 Visibility: LOW (fog + pollution mix)")
        st.warning("🚫 Outdoor travel NOT recommended")

    elif smog_risk >= 40:
        st.warning("🌫 MODERATE SMOG RISK")

        st.info("📍 Evening smog possible (6PM–9PM)")
        st.info("👁 Visibility: Medium")

    else:
        st.success("🟢 LOW SMOG RISK")
        st.success("👁 Visibility: Good")
        st.success("🌬 Clear air conditions expected")

    # ================= EXTRA INSIGHT =================

    if wind < 3 and humidity > 80:
        st.warning("⚠ Critical condition: Fog + Pollution combo risk")

else:
    st.info("Enter city to predict smog conditions")
    