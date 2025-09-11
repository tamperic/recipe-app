from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text="Enter recipe name")
    cooking_time = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Enter cooking time in minutes")
    ingredients = models.TextField(help_text="Enter ingredients separated by commas")
    difficulty = models.CharField(max_length=12, editable=False, blank=True)
    description = models.TextField(help_text="Enter recipe description")

    # Method to convert the comma separated 'ingredients' string inside 'Recipe' object into a list
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        else:
            ingredients_list = [i.strip() for i in self.ingredients.split(",")]
            return ingredients_list

    # Function to calculate the difficulty of the recipe base on cooking time and number of ingredients
    def calculate_difficulty(self):
        numberOfIngredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and numberOfIngredients < 4:
            self.difficulty = "Easy"

        elif self.cooking_time < 10 and numberOfIngredients >= 4:
            self.difficulty = "Medium"

        elif self.cooking_time >= 10 and numberOfIngredients < 4:    
            self.difficulty = "Intermediate"

        elif self.cooking_time >= 10 and numberOfIngredients >= 4:
            self.difficulty = "Hard"

        return self.difficulty
    
    # Override save to automatically update difficulty before saving
    def save(self, *args, **kwargs):
        self.difficulty = self.calculate_difficulty()
        super().save(*args, **kwargs) 

    def __str__(self):
        return str(self.name)