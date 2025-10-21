# Recipe Web Application

A full-stack web application built with **Python** and **Django** framework, deployed on **Heroku**, and powered by a **PostgreSQL** database. This platform allows users to create, manage, and explore recipes while providing data insights and visualization dashboards for a richer cooking experiance.

## 🛠️ Tech Stack
- Backend - **Python** & **Django** framework
- Frontend - **HTML** & **CSS** (Django templating)
- Database - **PostgreSQL** 
- Deployment - **Heroku**

## 🚀 Features
- **User Authentication** - login system
- **Recipe Management**: 
    - Create new recipes
    - Add recipe name, ingredients, cooking time, description, and image
    - Automatic calculation of recipe difficulty based on cooking time and number of ingredients
- **Recipe Search** - search for recipes by recipe name, ingredients, and difficuty level
- **Dashboards & Analytics**:
    - View recipe statistics
    - Data visualization (charts)
- **Responsive Frontend** - clean HTML & CSS pages rendered via Django templates

## ⚙️ Installation & Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/tamperic/recipe-app.git
    cd recipe-app
    ```

2. Create and activate virtual environment:
    ```bash
    mkvirtualenv <nameOfNewVirEnv>
    workon <nameOfNewVirEnv>
    ```

3. Run migrations:
    ```bash
    python manage.py migrate
    ```

4. Run the server:
    ```bash
    python manage.py runserver
    ```
    Starting development server at `http://127.0.0.1:8000/`