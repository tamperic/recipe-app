# Recipe Web Application

A full-stack web application built with **Python** and **Django** framework, deployed on **Heroku**, and powered by a **Postgres** database. This platform allows users to create, manage, and eplore recipes while providing statistical dashboards for recipe insights and data visualization.

## 🛠️ Tech Stack
- Backend - **Python** & **Django** framework
- Frontend - **HTML** & **CSS** (Django templating)
- Database - **PostgreSQL** 
- Deployment - **Heroku**

## 🚀 Features
- **User Authentication** - signup & login
- **Recipe Management**: 
    - Create, edit, delete recipes
    - Add ingredients, cooking time and description
    - Automatic calculation of fecipe difficulty based on cooking time and number of ingredients
- **Recipe Search** - search for recipes by ingredient
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