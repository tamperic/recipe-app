from django.shortcuts import render     # Imported by default
from django.views.generic import ListView, DetailView   # To display lists and details
from .models import Recipe   # To access Recipe model 

# Create your views here.
def home(request):
    return render(request, 'recipes/recipes_home.html', {'is_home': True})

# Class-based view
class RecipeListView(ListView):
    # Specify model
    model = Recipe

    # Specify template
    template_name = 'recipes/main.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_home'] = False
        return context

    model = Recipe
    template_name = 'recipes/detail.html'