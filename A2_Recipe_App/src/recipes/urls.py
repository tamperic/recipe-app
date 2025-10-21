from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, records, add_recipe

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),
    path('list/', RecipeListView.as_view(), name='list'),
    path('list/<pk>', RecipeDetailView.as_view(), name='detail'),
    path('recipes/', records, name='records'),
    path('add', add_recipe, name='add_recipe'),
]