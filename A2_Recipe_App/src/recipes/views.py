from django.shortcuts import render     # Imported by default
from django.views.generic import ListView, DetailView   # To display lists and details
from .models import Recipe   # To access Recipe model 

# Create your views here.
def home(request):
    return render(request, 'recipes/recipes_home.html')

# Class-based view
class RecipeListView(ListView):
    # Specify model
    model = Recipe

    # Specify template
    template_name = 'recipes/main.html'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'