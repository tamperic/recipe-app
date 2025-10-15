from io import BytesIO  # A class that lets you use memory (RAM) as if it were a file. Instead of writing an image to disk, you write it into memory.
import base64       # A module that converts binary data into a text string (Base64 encoding), useful for embedding images directly in HTML.
import matplotlib.pyplot as plt     # The library for making plots in Python.
import pandas as pd     # Handling data structures like DataFrames and Series (tables)

def get_graph():
    # Create a BytesIO buffer/object for the image
    buffer = BytesIO()

    # Create a plot with a BytesIO object as a file-object. Set format to png
    plt.savefig(buffer, format='png')

    # Set cursor to the beginning of the stream - move back to the beginnging of the file
    buffer.seek(0)

    # Retrieve the content of the file
    image_png = buffer.getvalue()

    # Encode the bytes-like object
    graph = base64.b64encode(image_png)

    # Decode to get the string as output
    graph = graph.decode('utf-8')

    # Free up the memory of buffer
    buffer.close()

    # Return the image/graph
    return graph

# chart_type: user input of type of chart,
# data: pandas DataFrame
def get_chart(chart_type, data, **kwargs):
    # Switch plot backend to AGG (Anti-Grain Geometry -> (non-interactive backend suitable for generating image files)) to write to file
    # AGG is preferred solution to write PNG files
    plt.switch_backend('AGG')

    # Specify figure size (width = 6, height = 3)
    fig = plt.figure(figsize=(6,3))

    # Select chart_type based on user input from the form 
    if chart_type == '#1':
        # Bar chart: cooking time vs name
        plt.bar(data['name'], data['cooking_time'], color="#74bee9")
        plt.xlabel('Recipe Name')
        plt.ylabel('Cooking Time (min)')
        plt.title('Cooking Time by Recipe')

    elif chart_type == '#2':
        # Pie chart: difficulty distribution
        labels = data['difficulty'].value_counts().index
        sizes = data['difficulty'].value_counts().values

        plt.pie(sizes, labels = labels, colors=['#e98074', '#e85a4f', '#d8c3a5', '#8e8d8a'], autopct='%1.1f%%', startangle=90)
        plt.title('Difficulty Level Distribution from All Recipes')

    elif chart_type == '#3':
        # Line chart: ingredient frequenty
        ingredients = data['ingredients'].str.split(', ')

        # Nested list comprehension - goes through every sublist  inside 'ingredients' list, and every item inside that sublist, and puts all of them into one flat list.
        all_ingredients = [item for sublist in ingredients for item in sublist]
        ingredient_counts = pd.Series(all_ingredients).value_counts()

        # If user selected ingredients, focus only on them
        selected_ingredients = kwargs.get('searched_ingredients')
        if selected_ingredients: 
            ingredient_counts = ingredient_counts.reindex(selected_ingredients, fill_value=0)

        plt.plot(ingredient_counts.index, ingredient_counts.values, color='#e85a4f', marker='o')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Ingredients')
        plt.ylabel('Number of Recipes')
        plt.title('Frequency of Searched Ingredients Across Recipes')

    else:
        print('Unknown chart type')

    # Specify layout details
    plt.tight_layout()

    # Render the graph to file
    chart = get_graph()
    return chart