from django import forms    # Import Django forms

# Specify choices as a tuple 
CHART_CHOICES = (
    ('#1', 'Bar chart'),    # when user selects Bar chart, it is stored as #1
    ('#2', 'Pie chart'),
    ('#3', 'Line chart')
)

DIFFICULTY_CHOICES = (
    ('', '--- Select Difficulty ---'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Intermediate', 'Intermediate'),
    ('Hard', 'Hard'),
)

# Define class-based form imported from Django forms
class RecipesSearchForm(forms.Form):
    recipe_name = forms.CharField(
        max_length=120, 
        label='1. Enter one recipe name', 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_recipe_name'})
    )
    ingredients = forms.CharField(
        max_length=250, 
        label='2. Enter one or multiple ingredients (separated by commas)', 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_ingredients'})
    )
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES, 
        label='3. Choose difficulty level', 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_difficulty'})
    )
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES, 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )