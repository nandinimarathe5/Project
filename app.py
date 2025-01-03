from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load your CSV dataset with the specified path and encoding
recipes = pd.read_csv(r"C:\Users\nandi\Desktop\food row\food row\new new.csv", encoding='ISO-8859-1')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input for both fields
        ingredients_input = request.form.get('ingredients', '')
        recipe_name_input = request.form.get('recipe_name', '')

        # Initialize no_match flag
        no_match = False
        results = pd.DataFrame()

        # Process ingredients input
        ingredient_list = [ingredient.strip().lower() for ingredient in ingredients_input.split(',') if ingredient.strip()]

        if ingredients_input:
            # Modify logic to return only recipes where all ingredients exactly match
            results = recipes[recipes['ingredients'].apply(
                lambda x: set(ingredient_list) == set([i.strip().lower() for i in x.split(',')]) if isinstance(x, str) else False
            )]
            if results.empty:
                no_match = True  # No matching recipes found

        # Process recipe name input without changing its functionality
        if recipe_name_input:
            recipe_name_input = recipe_name_input.lower()
            recipe_results = recipes[recipes['Recipe Name'].str.lower() == recipe_name_input]
            if not recipe_results.empty:
                results = recipe_results
            else:
                # Only set no_match if there was no match for ingredients either
                if results.empty:
                    no_match = True

        return render_template('index.html', results=results, no_match=no_match)

    return render_template('index.html', results=pd.DataFrame(), no_match=False)

@app.route('/recipe_detail/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = recipes[recipes['Recipe ID'] == recipe_id].iloc[0]  # Get the specific recipe
    return render_template('recipe_detail.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
