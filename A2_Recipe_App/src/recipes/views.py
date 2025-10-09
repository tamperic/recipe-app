from django.shortcuts import render     # Imported by default
from django.views.generic import ListView, DetailView   # To display lists and details
from .models import Recipe   # To access Recipe model 
from django.contrib.auth.mixins import LoginRequiredMixin   # To protect class-based view so that view isn't displayed before successful login / authentication.
from django.contrib.auth.decorators import login_required   # To protect function-based views
from .forms import RecipesSearchForm    
from .models import Recipe
import pandas as pd
from .utils import get_chart
from django.db.models import Q


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
    # Create an instance of RecipesSearchForm that is defined in recipes/forms.py
    form = RecipesSearchForm(request.POST or None)
 
    recipes_df = None   # Initialize dataframe to None
    chart = None    # Initialize chart to None

    recipe_name = None
    ingredients = None
    difficulty = None
   
    qs = Recipe.objects.all()   # Display all recipes by default

    # Check if the form is submitted - if the form button (search) is clicked (i.e., POST request made)
    if request.method == 'POST':
        if 'show_all' in request.POST:
            qs = Recipe.objects.all()   # Display all recipes when button 'Show All Recipes' is clicked

        else:
            # If it's true get data from the form -> read recipe_name and chart_type
            recipe_name = request.POST.get('recipe_name')
            ingredients = request.POST.get('ingredients')
            difficulty = request.POST.get('difficulty')

            # Querying the database
            if recipe_name:
                qs = qs.filter(name__icontains = recipe_name)    # Filter by recipe_name

            elif ingredients:
                ingredients_list = [ing.strip() for ing in ingredients.split(',') if ing.strip()]
                query = Q()
                for ing in ingredients_list: 
                    query |= Q(ingredients__icontains = ing)
                qs = qs.filter(query)       # Filter by ingredients

            elif difficulty:
                qs = qs.filter(difficulty = difficulty)     # Filter by difficulty

        # Converting query results to a DataFrame for table and charts
        if qs:
            recipes_df = pd.DataFrame(qs.values())      # If data found, convert the QuerySet values to pandas DataFrame
            recipes_df = recipes_df.drop(columns=['description', 'pic'])    # Don't display 'description' and 'pic' columns in pandas table

            # Generate charts based on input
            if ingredients:
                chart = get_chart('#3', recipes_df, searched_ingredients = ingredients_list)     # Line chart for ingredients frequency
            elif recipe_name:
                chart = get_chart('#1', recipes_df)     # Bar chart for cooking time vs name
            elif difficulty:
                # Pie chart for diffculty distribution for all recipes not just filtered ones
                all_recipes_df = pd.DataFrame(Recipe.objects.all().values())
                all_recipes_df = all_recipes_df.drop(columns=['description', 'pic'])
                chart = get_chart('#2', all_recipes_df)

            recipes_df = recipes_df.to_html()       # Make DataFrame readable as HTML

        else:
            recipes_df = None

    else:
        # # Default view - show all recipes table
        if qs:
            recipes_df = pd.DataFrame(qs.values())
            recipes_df = recipes_df.drop(columns=['description', 'pic'])
            recipes_df = recipes_df.to_html() 

    # Pack up data to be sent to template in the context dictionary
    context = {
        'form' : form,
        'recipes_df': recipes_df,
        'chart': chart
    }

    # Load the recipes/records.html page using the data from above
    return render(request, 'recipes/records.html', context)  # Display page
