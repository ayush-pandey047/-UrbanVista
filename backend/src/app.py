import streamlit as st
import pandas as pd
import joblib
import os

# 1. Load Model and Data
# Using absolute paths or relative paths based on your previous execution
try:
    model = joblib.load('models/house_model.pkl')
    model_columns = joblib.load('models/model_columns.pkl')
    df_raw = pd.read_csv('data/master_data.csv')
except:
    model = joblib.load('../models/house_model.pkl')
    model_columns = joblib.load('../models/model_columns.pkl')
    df_raw = pd.read_csv('../data/master_data.csv')

st.set_page_config(page_title="UrbanVista", page_icon="🏠", layout="wide")

st.title("UrbanVista: Full-Feature House Price Predictor")
st.markdown("Enter all details to get the most accurate price estimation.")

# --- SIDEBAR: MAIN FEATURES ---
st.sidebar.header("📍 Location & Size")
selected_city = st.sidebar.selectbox("Select City", sorted(df_raw['City'].unique()))

city_locations = df_raw[df_raw['City'] == selected_city]['Location'].unique()
selected_location = st.sidebar.selectbox("Select Locality", sorted(city_locations))

area = st.sidebar.number_input("Total Area (sq. ft)", min_value=100, value=1200)
bhk = st.sidebar.slider("Bedrooms (BHK)", 1, 10, 2)
resale = st.sidebar.selectbox("Is it a Resale Property?", ["No", "Yes"])

# --- MAIN PAGE: AMENITIES ---
st.subheader("🏢 Amenities & Features")
st.write("Select the facilities available in the property:")

# We organize the 30+ features into columns to look nice
col1, col2, col3, col4 = st.columns(4)

with col1:
    gym = st.checkbox("Gymnasium")
    pool = st.checkbox("Swimming Pool")
    garden = st.checkbox("Landscaped Gardens")
    jogging = st.checkbox("Jogging Track")
    security = st.checkbox("24X7 Security")
    power = st.checkbox("Power Backup")
    parking = st.checkbox("Car Parking")
    staff = st.checkbox("Maintenance Staff")

with col2:
    rain = st.checkbox("Rain Water Harvesting")
    indoor = st.checkbox("Indoor Games")
    mall = st.checkbox("Shopping Mall")
    intercom = st.checkbox("Intercom")
    sports = st.checkbox("Sports Facility")
    atm = st.checkbox("ATM")
    club = st.checkbox("Club House")
    school = st.checkbox("School")

with col3:
    quarter = st.checkbox("Staff Quarter")
    cafe = st.checkbox("Cafeteria")
    multi = st.checkbox("Multipurpose Room")
    hosp = st.checkbox("Hospital")
    wash = st.checkbox("Washing Machine")
    gas = st.checkbox("Gas Connection")
    ac = st.checkbox("AC")
    wifi = st.checkbox("Wifi")

with col4:
    play = st.checkbox("Children's Play Area")
    lift = st.checkbox("Lift Available")
    bed = st.checkbox("BED")
    vaastu = st.checkbox("Vaastu Compliant")
    micro = st.checkbox("Microwave")
    golf = st.checkbox("Golf Course")
    tv = st.checkbox("TV")
    fridge = st.checkbox("Refrigerator")
    sofa = st.checkbox("Sofa")
    wardrobe = st.checkbox("Wardrobe")
    dining = st.checkbox("Dining Table")

# --- PREDICTION LOGIC ---
if st.button("Calculate Market Price"):
    # 1. Create a template row with all zeros
    input_row = pd.DataFrame(0, index=[0], columns=model_columns)
    
    # 2. Map Numeric/Basic Features
    input_row['Area'] = area
    input_row['No. of Bedrooms'] = bhk
    input_row['Resale'] = 1 if resale == "Yes" else 0
    
    # 3. Map One-Hot Encoded City/Location
    city_col = "City_" + selected_city
    loc_col = "Location_" + selected_location
    if city_col in input_row.columns: input_row[city_col] = 1
    if loc_col in input_row.columns: input_row[loc_col] = 1
    
    # 4. Map All Binary Amenities (The checkboxes)
    # The keys here must match the CSV column names exactly
    amenities_map = {
        'Gymnasium': gym, 'SwimmingPool': pool, 'LandscapedGardens': garden,
        'JoggingTrack': jogging, 'RainWaterHarvesting': rain, 'IndoorGames': indoor,
        'ShoppingMall': mall, 'Intercom': intercom, 'SportsFacility': sports,
        'ATM': atm, 'ClubHouse': club, 'School': school, '24X7Security': security,
        'PowerBackup': power, 'CarParking': parking, 'StaffQuarter': quarter,
        'Cafeteria': cafe, 'MultipurposeRoom': multi, 'Hospital': hosp,
        'WashingMachine': wash, 'Gasconnection': gas, 'AC': ac, 'Wifi': wifi,
        "Children'splayarea": play, 'LiftAvailable': lift, 'BED': bed,
        'VaastuCompliant': vaastu, 'Microwave': micro, 'GolfCourse': golf,
        'TV': tv, 'DiningTable': dining, 'Sofa': sofa, 'Wardrobe': wardrobe,
        'Refrigerator': fridge, 'MaintenanceStaff': staff
    }
    
    for feature, val in amenities_map.items():
        if feature in input_row.columns:
            input_row[feature] = 1 if val else 0

    # 5. Predict
    try:
        price_prediction = model.predict(input_row)[0]
        st.success(f"## 💰 Estimated Price: ₹ {round(price_prediction, 2):,}")
    except Exception as e:
        st.error(f"Error in prediction: {e}")