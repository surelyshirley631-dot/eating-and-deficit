# training-and-deficit-
combine your training plan with scientific diet 
# nutrition_ai_app - Nutrition Database

This repository file `nutrition_db_110.csv` is a generated English nutrition database (110+ items) intended for use with the AI Nutrition Meal Planner Streamlit app.

## File: nutrition_db_110.csv
Columns:
- food: name of food item (string)
- category: high-level category (carb/protein/fat/veg/fruit/other)
- cal_per_100g: kilocalories per 100 g (number)
- protein_g_per_100g: protein grams per 100 g (number)
- carbs_g_per_100g: carbohydrate grams per 100 g (number)
- fat_g_per_100g: fat grams per 100 g (number)
- tags: semicolon-separated tags (string)
- allergens: comma-separated allergens (string) — e.g. milk, nuts, soy, gluten

## Usage
Place `nutrition_db_110.csv` in the same folder as `yyxapp.py`. The Streamlit app will load it and use the `category` or `tags` columns to provide meal suggestions. If you upload your own CSV, make sure columns match the names above (case-insensitive).

## How to upload to GitHub & deploy to Streamlit Cloud
1. Create a GitHub repo and add files: `yyxapp.py`, `nutrition_db_110.csv`, `requirements.txt`, and `README.md`.
2. Example `requirements.txt`:
```
streamlit
pandas
openpyxl
```
3. Push to GitHub and sign into https://share.streamlit.io with your GitHub account. Create a new app and select your repo and `yyxapp.py` as the main file.
4. Streamlit Cloud will install dependencies and host the app. The share link will be something like:
`https://share.streamlit.io/<your-username>/<repo-name>/main/yyxapp.py`

## Notes
- The nutrition values are approximate and for demo purposes. For clinical use, replace with authoritative data (USDA / country-specific database).
- If you want a larger dataset (USDA), I can provide code to fetch and transform it for you.
