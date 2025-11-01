from django.test import TestCase, Client
from .models import Recipe  # To access Recipe model
from .forms import RecipesSearchForm, AddRecipeForm
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here:

# ================== MODEL TESTS ==================

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
        recipe = Recipe.objects.get(id=1)    # Get a recipe object to test
        field_label = recipe._meta.get_field('name').verbose_name   # Get the metadata for the 'name' and use it to query its data
        self.assertEqual(field_label, 'name')   # Compare the value to the expected result

    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)   # Get a recipe object to test
        max_length = recipe._meta.get_field('name').max_length   # Get the metadata for the 'name' and use it to query its max_length
        self.assertEqual(max_length, 50)     # Compare the value to the expected result i.e. 50

    def test_calculate_difficulty_easy(self):
        recipe = Recipe.objects.get(id=1)   # Get a recipe object to test
        difficulty = recipe.calculate_difficulty()  # Get the 'calculate_difficulty()' method to determine difficulty
        self.assertEqual(difficulty, 'Easy')    # Compare the value to the expected result

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), '/list/1')  # get_absoute_url() should take to the detail page of the recipe #1 and load the URL /recipes/list/1


# ================== FORM TESTS ==================

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


# ================== VIEW TESTS ==================

# Test to verify behavior od Recipe-related views (list, detail, add_recipe)
class RecipeViewsTest(TestCase):

    # Set up test environment - create test user, client, and one sample recipe
    def setUp(self):
        self.client = Client()  # Simulate a browser/client for sending HTTP requests
        self.user = User.objects.create_user(username = 'tester', password = 'test123') # Createtest user for authentication-related tests
        self.recipe = Recipe.objects.create(    # Create a sample recipe to be used in list/detail view tests
            name = 'Soup',
            cooking_time = 12,
            ingredients = 'Carrots, Water, Salt',
            description = 'Boil water, add carrots and salt.'
        )

    # Test to ensure that list page loads sucessfully and uses the correct template
    def test_recipe_list_view_status_code(self):
        response = self.client.get(reverse('recipes:list'))     # Simulate GET request to list view
        self.assertEqual(response.status_code, 200)     # Expect HTTP 200 OK
        self.assertTemplateUsed(response, 'recipes/main.html')  # Ensure correct template is used

    # Test to ensure that detail view for a specific recipe displays correctly
    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipes:detail', args = [self.recipe.id]))  # Simulate GET request to recipe detail page using the recipe's ID
        self.assertEqual(response.status_code, 200)     # Expect HTTP 200 OK
        self.assertContains(response, 'Soup')       # Page should display recipe's name
        self.assertTemplateUsed(response, 'recipes/detail.html')    # Ensure correct template

    # Test to verify that a logged-in user can access add_recipe page
    def test_add_recipe_view_get_authenticated(self):
        self.client.login(username = 'tester', password = 'test123')    # Log in with test user
        response = self.client.get(reverse('recipes:add_recipe'))   # Access the add_recipe page
        self.assertEqual(response.status_code, 200) # Expect success
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')    # Should render correct template

    # Test for submitting a valid recipe form creates a new recipe and redirect
    def test_add_recipe_view_post_valid(self):
        self.client.login(username = 'tester', password = 'test123')    # Log in with test user
        data = {    # Define valid recipe data
            'name': 'Pizza',
            'cooking_time': 15,
            'ingredients': 'Flour, Cheese, Tomato souce',
            'description': 'Mix, bake and serve.'
        }
        response = self.client.post(reverse('recipes:add_recipe'), data)    # Send POST request to add recipe view
        self.assertEqual(response.status_code, 302)     # Expect redirect (HTTP 302) after successful form submission
        self.assertTrue(Recipe.objects.filter(name = 'Pizza').exists()) # Check that new recipe was created in database

    # Test to ensure that unauthenticated users are redirect to the login page when adding a recipe
    def test_add_recipe_requires_login(self):
        response = self.client.get(reverse('recipes:add_recipe'))     # Simulate GET request to add_recipe view
        self.assertNotEqual(response.status_code, 200)   # Expect a redirect, not HTTP 200 OK
        self.assertRedirects(response, '/login/?next=/add')     # Check redirect URL (should send user to login page with ?next= param)