import streamlit as st
import pandas as pd

# -----------------------------
# Load the food database
# -----------------------------
@st.cache_data
def load_db(path="nutrition_db.csv"):
    df = pd.read_csv(path)
    return df

db = load_db()

# -----------------------------
# User input
# -----------------------------
st.title("Nutrition & Training Planner")

st.header("Step 1: Your info")
name = st.text_input("Name")
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", min_value=10, max_value=100, value=25)
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=60.0)
height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)

# Calculate BMI
bmi = weight / ((height / 100) ** 2)
st.write(f"Your BMI: {bmi:.1f}")

# -----------------------------
# Basal Metabolism
# -----------------------------
if gender == "Male":
    bmr = 9.99 * weight + 6.25 * height - 4.92 * age + 5
else:
    bmr = 9.99 * weight + 6.25 * height - 4.92 * age - 161

no_activity = bmr / 0.7
st.write(f"Basal Metabolic Rate (BMR): {bmr:.0f} kcal")
st.write(f"Total daily energy expenditure (no exercise): {no_activity:.0f} kcal")

# -----------------------------
# Training & goal
# -----------------------------
goal = st.selectbox("Goal", ["Weight Loss", "Muscle Gain"])

has_strength_training = True if goal == "Muscle Gain" else st.checkbox("Do you have regular strength training?", value=True)
strength_level = st.selectbox("Strength training level", ["Beginner", "Intermediate", "Advanced"])
aerobic_minutes = st.number_input("Average daily aerobic (min)", min_value=0, max_value=180, value=0)

# Strength training calories burn
strength_cals = 0
if has_strength_training:
    if gender == "Male":
        if strength_level == "Beginner":
            strength_cals = 150
        elif strength_level == "Intermediate":
            strength_cals = 200
        else:
            strength_cals = 250
    else:
        if strength_level == "Beginner":
            strength_cals = 100
        elif strength_level == "Intermediate":
            strength_cals = 150
        else:
            strength_cals = 200

# Aerobic calories estimate (simple)
aerobic_cals = aerobic_minutes * 8  # ~8 kcal per min moderate intensity

# -----------------------------
# Calculate target calories
# -----------------------------
if goal == "Weight Loss":
    # Weight loss: 20% deficit
    e_train_day = no_activity + strength_cals + aerobic_cals
    f_train_day = e_train_day * 0.64
    e_rest_day = no_activity + aerobic_cals
    f_rest_day = e_rest_day * 0.64
else:
    # Muscle gain: 16% surplus (0.84 factor)
    e_train_day = no_activity + strength_cals + aerobic_cals
    f_train_day = e_train_day * 0.84
    e_rest_day = no_activity + aerobic_cals
    f_rest_day = e_rest_day * 0.84

st.write(f"Estimated calories (training day): {f_train_day:.0f} kcal")
st.write(f"Estimated calories (rest day): {f_rest_day:.0f} kcal")

# -----------------------------
# Macronutrient distribution
# -----------------------------
if goal == "Weight Loss":
    carbs_ratio = [0.2, 0.4, 0.3, 0.1]  # breakfast, lunch, dinner, snack
    protein_ratio = [0.2, 0.3, 0.3, 0.2]
else:
    carbs_ratio = [0.25, 0.4, 0.25, 0.1]
    protein_ratio = [0.25, 0.3, 0.25, 0.2]

fat = 60 if gender == "Male" else 50

st.write(f"Macro distribution (Carbs% per meal): {carbs_ratio}")
st.write(f"Macro distribution (Protein% per meal): {protein_ratio}")
st.write(f"Daily fat allowance: {fat} g")

# -----------------------------
# Meal plan generator
# -----------------------------
def generate_meal_plan(db, total_calories, carbs_ratio, protein_ratio, fat_g):
    meals = {}
    meal_names = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    
    for i, meal in enumerate(meal_names):
        sample = db.sample(2)
        meals[meal] = sample.apply(
            lambda row: f"{row['food']} ({row['cal_per_100g']} kcal, P:{row['protein_g_per_100g']}g C:{row['carbs_g_per_100g']}g F:{row['fat_g_per_100g']}g)",
            axis=1
        ).tolist()
    
    df = pd.DataFrame.from_dict(meals, orient="index").transpose()
    return df

st.header("Meal Plan Suggestion")
meal_plan = generate_meal_plan(db, f_train_day, carbs_ratio, protein_ratio, fat)
st.dataframe(meal_plan)
