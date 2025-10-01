from django.contrib.auth import authenticate, login, logout     # Django authentication libraries
from django.contrib.auth.forms import AuthenticationForm    # Django Form for authentication
from django.shortcuts import render, redirect       # Django authentication libraries

# Function to log in that takes a request from user
def login_view(request):
    error_message = None
    form = AuthenticationForm()     # Form object with username and password fileds

    # After user clicks the 'login' button, POST request is generated
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)    # Read the data sent by the form via POST request

    # Check if form is valid
    if form.is_valid():
        username = form.cleaned_data.get('username')        # Read username
        password = form.cleaned_data.get('password')        # Read password

        user = authenticate(username=username, password=password)   # Use Django authenticate function to validate the user
        if user is not None: 
            login(request, user)    # If user is authenticated then use pre-defined Django function to login
            return redirect('recipes:list')    # and send the user to desired page
        else: 
            error_message = 'Oops, something went wrong.'   # Print error message in case of error

    # Prepare data to send from view to template
    context = {
        'form': form,   # Send the form data
        'error_message': error_message  # and the error message
    }
    # Load the login page using "context" information
    return render(request, 'auth/login.html', context)


# Function to log out that takes a request from user
def logout_view(request):
    logout(request)     # The use pre-defined Django function that logs user out

    # Where to redirect
    if request.GET.get('next') == 'login':
        next_page = 'login'
        message = 'Redirecting back to the login page...'
    else:
        next_page = 'recipes:home'
        message = 'Redirecting back to the homepage...'

    # Pass 'next_page' to template
    return render(request, 'auth/logout.html', {
        'next_page': next_page,
        'redirect_message': message
    })