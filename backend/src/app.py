import streamlit as st
import pandas as pd
import joblib
import os

# --- 1. SETTINGS & CUSTOM HUMAN STYLING ---
st.set_page_config(page_title="UrbanVista", layout="wide") # If i want to add a icon then i have to write the  page_icon="🏠",

# This block adds the "Human" feel without changing your logic
st.markdown("""
    <style>
    /* Main background and font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #111827;
        color: white;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        color: white;
    }
    
    /* Valuation box */
    .prediction-box {
        background-color: #064e3b;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #10b981;
    }
    </style>
    """, unsafe_allow_html=True)

def format_indian_currency(num):
    """Formats numbers into the Indian Lakh/Crore system (e.g., 1,25,000)"""
    s = str(int(num))
    if len(s) <= 3: return s
    last_three = s[-3:]
    other_parts = s[:-3]
    res = ""
    for i, char in enumerate(reversed(other_parts)):
        if i % 2 == 0 and i > 0:
            res = "," + res
        res = char + res
    return res + "," + last_three

# --- 2. LOAD DATA & AI MODEL (Robust Path Logic) ---
# Ye code khud detect karega ki 'src' folder kahan hai
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ye 'src' se ek kadam piche 'backend' folder mein jayega
backend_dir = os.path.dirname(current_dir)

# Ab hum folders ko system-independent tarike se join karenge
MODEL_PATH = os.path.join(backend_dir, 'models', 'house_model.pkl')
COLUMNS_PATH = os.path.join(backend_dir, 'models', 'model_columns.pkl')
DATA_PATH = os.path.join(backend_dir, 'data', 'master_data.csv')

try:
    model = joblib.load(MODEL_PATH)
    model_columns = joblib.load(COLUMNS_PATH)
    df_raw = pd.read_csv(DATA_PATH)
except Exception as e:
    st.error(f"Files nahi mili! Check karo: {MODEL_PATH}")
    st.info("Make sure your GitHub structure has backend/models and backend/data folders.")
    st.stop()

# --- 3. SIDEBAR: LOCATION & GLOBAL SETTINGS ---
st.sidebar.header("Location & Currency")

currency_choice = st.sidebar.selectbox("Display Currency", ["INR (₹)", "USD ($)", "EUR (€)"])
rates = {"INR (₹)": 1.0, "USD ($)": 0.012, "EUR (€)": 0.011}
curr_symbol = currency_choice.split(" ")[1].strip("()")

selected_city = st.sidebar.selectbox("Select City", sorted(df_raw['City'].unique()))
city_locations = df_raw[df_raw['City'] == selected_city]['Location'].unique()
selected_location = st.sidebar.selectbox("Select Locality", sorted(city_locations))

area = st.sidebar.number_input("Total Area (sq. ft)", min_value=100, value=1200)
bhk = st.sidebar.slider("Bedrooms (BHK)", 1, 10, 2) # default 2 kar ke rakah hu
resale = st.sidebar.selectbox("Is it a Resale Property?", ["No", "Yes"])

# --- 4. MAIN PAGE: HUMANIZED TABS ---
st.title("UrbanVista")
st.write(f"Evaluating the market landscape for a property in **{selected_location}, {selected_city}**.")

# Adding the Graph early for visual appeal
st.subheader(f"Market Trends in {selected_city}")

# Filter and clean data specifically for the visualization
city_data = df_raw[df_raw['City'] == selected_city].copy()

if not city_data.empty:
    # 1. Clean data: Ensure BHK and Price are numeric to avoid "undefined" labels
    city_data['No. of Bedrooms'] = pd.to_numeric(city_data['No. of Bedrooms'], errors='coerce')
    city_data['Price'] = pd.to_numeric(city_data['Price'], errors='coerce')
    
    # 2. Group data by BHK and calculate the average price
    avg_price_bhk = city_data.groupby('No. of Bedrooms')['Price'].mean().sort_index().reset_index()
    
    # Rename for professional display
    avg_price_bhk.columns = ['BHK Type', 'Average Market Price']
    
    # 3. Create the bar chart with a professional custom color
    # Setting the 'BHK Type' as index ensures the X-axis is labeled 1, 2, 3...
    st.bar_chart(
        data=avg_price_bhk.set_index('BHK Type'), 
        use_container_width=True,
        color="#fbbf24" # A premium gold/amber color
    )
    st.write(f"This analysis represents the current valuation trends for residential properties in {selected_city} based on configuration.")
else:
    st.info("Gathering more market data for this specific region...")

st.markdown("---")
st.subheader("Property Features & Lifestyle")

# Organizing your original checkboxes into Tabs for a cleaner look
tab1, tab2, tab3 = st.tabs(["Building & Society", "Sports & Health", "Furnishing & Appliances"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        security = st.checkbox("24X7 Security")
        power = st.checkbox("Power Backup")
        parking = st.checkbox("Car Parking")
        lift = st.checkbox("Lift Available")
        intercom = st.checkbox("Intercom")
    with col2:
        rain = st.checkbox("Rain Water Harvesting")
        staff_q = st.checkbox("Staff Quarter")
        m_staff = st.checkbox("Maintenance Staff")
        vaastu = st.checkbox("Vaastu Compliant")
        m_room = st.checkbox("Multipurpose Room")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        gym = st.checkbox("Gymnasium")
        pool = st.checkbox("Swimming Pool")
        garden = st.checkbox("Landscaped Gardens")
        jogging = st.checkbox("Jogging Track")
        club = st.checkbox("Club House")
    with col2:
        sports = st.checkbox("Sports Facility")
        play_area = st.checkbox("Children's Play Area")
        golf = st.checkbox("Golf Course")
        indoor = st.checkbox("Indoor Games")
        hospital = st.checkbox("Hospital")
        school = st.checkbox("School")
        shopping = st.checkbox("Shopping Mall")
        atm = st.checkbox("ATM")
        cafeteria = st.checkbox("Cafeteria")

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        wash = st.checkbox("Washing Machine")
        gas = st.checkbox("Gas Connection")
        ac = st.checkbox("AC")
        wifi = st.checkbox("Wifi")
        bed = st.checkbox("BED")
    with col2:
        tv = st.checkbox("TV")
        dining = st.checkbox("Dining Table")
        sofa = st.checkbox("Sofa")
        wardrobe = st.checkbox("Wardrobe")
        fridge = st.checkbox("Refrigerator")
        micro = st.checkbox("Microwave")

# --- 5. PREDICTION LOGIC ---
st.markdown("<br>", unsafe_allow_html=True)

if st.button("Calculate Market Price"):
    if area < (bhk * 150):  # at least ek bhk ko 150 sqft dena hai
        st.error(f"Area Error: {area} sq.ft is too small for a {bhk} BHK property.")
    else:
        # Create input row
        input_row = pd.DataFrame(0, index=[0], columns=model_columns)
        input_row['Area'] = area
        input_row['No. of Bedrooms'] = bhk
        input_row['Resale'] = 1 if resale == "Yes" else 0
        
        c_col, l_col = f"City_{selected_city}", f"Location_{selected_location}"
        if c_col in input_row.columns: input_row[c_col] = 1
        if l_col in input_row.columns: input_row[l_col] = 1
        
        amenities_map = {
            'MaintenanceStaff': m_staff, 'Gymnasium': gym, 'SwimmingPool': pool,
            'LandscapedGardens': garden, 'JoggingTrack': jogging, 'RainWaterHarvesting': rain,
            'IndoorGames': indoor, 'ShoppingMall': shopping, 'Intercom': intercom,
            'SportsFacility': sports, 'ATM': atm, 'ClubHouse': club, 'School': school,
            '24X7Security': security, 'PowerBackup': power, 'CarParking': parking,
            'StaffQuarter': staff_q, 'Cafeteria': cafeteria, 'MultipurposeRoom': m_room,
            'Hospital': hospital, 'WashingMachine': wash, 'Gasconnection': gas,
            'AC': ac, 'Wifi': wifi, "Children'splayarea": play_area, 'LiftAvailable': lift,
            'BED': bed, 'VaastuCompliant': vaastu, 'Microwave': micro, 'GolfCourse': golf,
            'TV': tv, 'DiningTable': dining, 'Sofa': sofa, 'Wardrobe': wardrobe, 'Refrigerator': fridge
        }

        for feature, val in amenities_map.items():
            if feature in input_row.columns:
                input_row[feature] = 1 if val else 0

        # Predict
        price_inr = model.predict(input_row)[0]
        final_price = price_inr * rates[currency_choice]

        # Display Result in a Styled Box
        st.markdown("---")
        if currency_choice == "INR (₹)":
            indian_fmt = format_indian_currency(final_price)
            st.markdown(f"""<div class="prediction-box">
                <h3 style='color: white; margin:0;'>Estimated Valuation: ₹ {indian_fmt}</h3>
            </div>""", unsafe_allow_html=True)
            
            if price_inr >= 10000000:
                st.info(f"💡 Approx: **{round(price_inr/10000000, 2)} Crore**")
            else:
                st.info(f"💡 Approx: **{round(price_inr/100000, 2)} Lakh**")
        else:
            st.markdown(f"""<div class="prediction-box">
                <h3 style='color: white; margin:0;'>Estimated Valuation: {curr_symbol} {final_price:,.2f}</h3>
            </div>""", unsafe_allow_html=True)