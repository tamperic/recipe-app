from django.test import TestCase
from .models import Recipe # To access Recipe model
from .forms import RecipesSearchForm

# Create your tests here.
class RecipeModelTest(TestCase):

    def setUpTestData():
        # Set up non-modified objects used by all test methods
        Recipe.objects.create(
            name="Tea", 
            cooking_time=3, 
            ingredients="Tea Leaves, Sugar, Water", 
            description="Bring water to a boil. Add tea leaves and let them steep for 3–5 minutes, depending on desired strength. Strain the tea into a cup and add sugar to taste. This quick and refreshing drink is perfect for any time of the day."
        )

    def test_recipe_name(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'name' and ise it to query its data
        field_label = recipe._meta.get_field('name').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'name')

    def test_recipe_name_max_length(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the 'name' and ise it to query its max_length
        max_length = recipe._meta.get_field('name').max_length
    
        # Compare the value to the expected result i.e. 50
        self.assertEqual(max_length, 50)

    def test_calculate_difficulty_easy(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)
        
        # Get the 'calculate_difficulty()' method to determine difficulty
        difficulty = recipe.calculate_difficulty()
    
        # Compare the value to the expected result i.e. 50
        self.assertEqual(difficulty, 'Easy')

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        # get_absoute_url() should tak to the detail page of the recipe #1 adn load the URL /recipes/list/1
        self.assertEqual(recipe.get_absolute_url(), '/list/1')


class RecipeSearchFormTest(TestCase):
    # Tests that difficulty dropdown has expected choices
    def test_difficulty_choices(self):
        form = RecipesSearchForm()
        expected_diff_choices = [
            ('', '--- Select Difficulty ---'),
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('Intermediate', 'Intermediate'),
            ('Hard', 'Hard'),
        ]
        self.assertEqual(form.fields['difficulty'].choices, expected_diff_choices)

    # Test that valid data passes form validation
    def test_form_valid_data(self):
        form_data = {
            'recipe_name': 'Spaghetti',
            'ingredients': 'Spaghetti, Parsley, Black papper',
            'difficulty': 'Intermediate'
        }
        form = RecipesSearchForm(data = form_data)
        self.assertTrue(form.is_valid())

    # Test that missing required data fails validation
    def test_form_invalid_data(self):
        form_data = {
            'recipe_name': '',
            'ingredients': '',
            'difficulty': ''
        }
        form = RecipesSearchForm(data = form_data)
        self.assertTrue(form.is_valid())

    # Test that all form fields have correct labels
    def test_field_labels(self):
        form = RecipesSearchForm()
        self.assertEqual(form.fields['recipe_name'].label, '1. Enter one recipe name')
        self.assertEqual(form.fields['ingredients'].label, '2. Enter one or multiple ingredients (separated by commas)')
        self.assertEqual(form.fields['difficulty'].label, '3. Choose difficulty level')

    # Test that the form contains all expected
    def test_form_fields_exist(self):
        form = RecipesSearchForm()
        self.assertIn('recipe_name', form.fields)
        self.assertIn('ingredients', form.fields)
        self.assertIn('difficulty', form.fields)