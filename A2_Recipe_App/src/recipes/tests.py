from django.test import TestCase
from .models import Recipe # To access Recipe model

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