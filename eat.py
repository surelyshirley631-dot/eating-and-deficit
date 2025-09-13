import streamlit as st
import pandas as pd

# --- Load database ---
@st.cache_data
def load_db(path="nutrition_db.csv"):
    df = pd.read_csv(path)
    df['tags'] = df['tags'].fillna("").apply(lambda x: [t.strip().lower() for t in str(x).split(";") if t.strip()])
    df['allergens'] = df['allergens'].fillna("").apply(lambda x: [a.strip().lower() for a in str(x).split(";") if a.strip()])
    return df

db = load_db()

# --- User Inputs ---
st.title("AI Nutrition Planner 🍎")

name = st.text_input("Name")
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", 18, 80, 25)
weight = st.number_input("Weight (kg)", 30, 200, 70)
height = st.number_input("Height (cm)", 130, 220, 170)
goal = st.selectbox("Goal", ["Weight Loss", "Muscle Gain"])
has_cardio = st.checkbox("Do you include cardio?")

# Calories burned per session
cardio_cal = st.number_input("Cardio calories burned per day", 0, 2000, 200 if has_cardio else 0)
strength_cal = st.number_input("Strength training calories burned per session", 0, 2000, 300)

# --- Calculations ---
bmi = round(weight / ((height/100) ** 2), 2)
# Basal Metabolic Rate (simplified Mifflin-St Jeor)
if gender == "Male":
    bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
else:
    bmr = 447.6 + (9.25 * weight) + (3.1 * height) - (4.3 * age)

# Total daily energy expenditure (TDEE baseline, no exercise)
tdee_no_ex = bmr / 0.7

results = {}

if goal == "Weight Loss":
    # Case 1: no strength training
    if strength_cal == 0:
        balance_cals = tdee_no_ex + cardio_cal
        target_cals = balance_cals * 0.64
        results["Daily"] = target_cals
    else:
        # Training day
        balance_train = tdee_no_ex + strength_cal + cardio_cal
        target_train = balance_train * 0.64
        # Rest day
        balance_rest = tdee_no_ex + cardio_cal
        target_rest = balance_rest * 0.64
        results["Training Day"] = target_train
        results["Rest Day"] = target_rest

elif goal == "Muscle Gain":
    # Always assume strength training
    # Training day
    balance_train = tdee_no_ex + strength_cal + cardio_cal
    target_train = balance_train * 0.84
    # Rest day
    balance_rest = tdee_no_ex + cardio_cal
    target_rest = balance_rest * 0.84
    results["Training Day"] = target_train
    results["Rest Day"] = target_rest

# --- Macro Recommendations ---
def macros_split(total_cals, goal):
    if goal == "Weight Loss":
        carb_pct, protein_pct, fat_g = 0.45, 0.30, 50 if gender == "Female" else 60
    else:  # Muscle Gain
        carb_pct, protein_pct, fat_g = 0.50, 0.30, 60 if gender == "Female" else 70

    carbs_g = (total_cals * carb_pct) / 4
    protein_g = (total_cals * protein_pct) / 4
    fat_cals = fat_g * 9
    return carbs_g, protein_g, fat_g, fat_cals

st.subheader("📊 Results")
st.write(f"**BMI:** {bmi}")
st.write(f"**BMR (a):** {bmr:.0f} kcal")
st.write(f"**TDEE no exercise (b=a÷0.7):** {tdee_no_ex:.0f} kcal")

for day_type, cals in results.items():
    st.markdown(f"### {day_type}")
    st.write(f"Target Calories: **{cals:.0f} kcal**")
    carbs, protein, fat_g, fat_cals = macros_split(cals, goal)
    st.write(f"- Carbs: {carbs:.0f} g")
    st.write(f"- Protein: {protein:.0f} g")
    st.write(f"- Fat: {fat_g} g ({fat_cals:.0f} kcal)")

st.info("🥦 Veggies and fruits are recommended freely: ~500 g vegetables + 300 g fruits daily.")

