from django.shortcuts import render     # Imported by default
from django.views.generic import ListView, DetailView   # To display lists and details
from .models import Recipe   # To access Recipe model 
from django.contrib.auth.mixins import LoginRequiredMixin   # To protect class-based view so that view isn't displayed before successful login / authentication.
from django.contrib.auth.decorators import login_required   # To protect function-based views


# Create your views here.
def home(request):
    return render(request, 'recipes/recipes_home.html', {'is_home': True})

# Class-based view for recipe list
class RecipeListView(ListView, LoginRequiredMixin):
    # Specify model
    model = Recipe

    # Specify template
    template_name = 'recipes/main.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_home'] = False
        return context

# Class-based view for recipe details
class RecipeDetailView(DetailView, LoginRequiredMixin):
    model = Recipe
    template_name = 'recipes/detail.html'


# Function-based view - records(request)
# Keep protected
@login_required
def records(request):
    return render(request, 'recipes/records.html')  # Display page