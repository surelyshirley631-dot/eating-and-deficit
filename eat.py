import streamlit as st
import pandas as pd

# ------------------------
# Load database
# ------------------------
@st.cache_data
def load_db(path="nutrition_db.csv"):
    return pd.read_csv(path)

db = load_db()

# ------------------------
# BMR calculation (Mifflin-St Jeor)
# ------------------------
def calculate_bmr(weight, height, age, gender):
    if gender == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

# ------------------------
# Macronutrient calculation
# ------------------------
def calculate_macros(calories, goal):
    if goal == "fat loss":
        carbs = 0.45 * calories / 4
        protein = 0.30 * calories / 4
        fat = 0.25 * calories / 9
    else:  # muscle gain
        carbs = 0.50 * calories / 4
        protein = 0.30 * calories / 4
        fat = 0.20 * calories / 9

    return {
        "Carbs (g)": round(carbs),
        "Protein (g)": round(protein),
        "Fat (g)": round(fat),
    }

# ------------------------
# Fat loss calories
# ------------------------
def calculate_fat_loss_calories(bmr, activity_factor=1.2):
    tdee = bmr * activity_factor
    return round(tdee * 0.84)  # 16% deficit

# ------------------------
# Muscle gain calories
# ------------------------
def calculate_muscle_gain_calories(bmr, c, d, training_day=True):
    b = bmr / 0.7
    if training_day:
        e1 = b + c + d
        return round(e1 * 0.84)
    else:
        e2 = b + d
        return round(e2 * 0.84)

# ------------------------
# Meal Plan generator
# ------------------------
def generate_meal_plan(db, calories, macros):
    meals = {}
    for meal in ["Breakfast", "Lunch", "Dinner", "Snacks"]:
        meals[meal] = db.sample(2)["Food"].tolist()
    df = pd.DataFrame.from_dict(meals, orient="index").transpose()
    return df

# ------------------------
# Streamlit App
# ------------------------
st.title("Nutrition & Training Planner")

# User input
name = st.text_input("Your Name")
gender = st.selectbox("Gender", ["male", "female"])
age = st.number_input("Age", 18, 80, 25)
height = st.number_input("Height (cm)", 140, 210, 170)
weight = st.number_input("Weight (kg)", 40, 150, 60)
goal = st.selectbox("Goal", ["fat loss", "muscle gain"])

# Training info (for muscle gain)
c = st.number_input("Strength training calories (c)", 0, 1000, 300)
d = st.number_input("Cardio calories (d)", 0, 1000, 200)

if st.button("Generate Plan"):
    bmr = calculate_bmr(weight, height, age, gender)

    if goal == "fat loss":
        calories = calculate_fat_loss_calories(bmr)
        macros = calculate_macros(calories, goal)

        st.subheader("Fat Loss Plan")
        st.write(f"Recommended calories: **{calories} kcal/day**")

        st.subheader("Macronutrient Breakdown")
        st.write(macros)

        st.subheader("Sample Meal Plan")
        st.dataframe(generate_meal_plan(db, calories, macros))

    else:  # muscle gain
        training_day_calories = calculate_muscle_gain_calories(bmr, c, d, training_day=True)
        rest_day_calories = calculate_muscle_gain_calories(bmr, c, d, training_day=False)

        st.subheader("Muscle Gain Plan")
        st.write(f"Training day calories: **{training_day_calories} kcal**")
        st.write(f"Rest day calories: **{rest_day_calories} kcal**")

        # Training day
        st.markdown("### Training Day")
        training_macros = calculate_macros(training_day_calories, goal)
        st.write(training_macros)
        st.dataframe(generate_meal_plan(db, training_day_calories, training_macros))

        # Rest day
        st.markdown("### Rest Day")
        rest_macros = calculate_macros(rest_day_calories, goal)
        st.write(rest_macros)
        st.dataframe(generate_meal_plan(db, rest_day_calories, rest_macros))
