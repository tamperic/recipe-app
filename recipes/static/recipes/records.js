// Wait untill the entire HTML document (DOM) is loaded before running this script
document.addEventListener('DOMContentLoaded', function() {

    // 1. Get references to the 3 input form fields (recipe name, ingredients, difficulty) by their HTML IDs
    const nameField = document.getElementById('id_recipe_name');
    const ingredientsField = document.getElementById('id_ingredients');
    const difficultyField = document.getElementById('id_difficulty');

    // 2. Function to disable all other fields except currently active (focused) field
    function disableOtherFields(activeField) {
        // Loop through all 3 fields
        [nameField, ingredientsField, difficultyField].forEach(field => {
            // If the field is NOT active, disable it
            if (field !== activeField) {
                field.disabled = true;
            }
        });
    }

    // 3. Function to re-enable all fields so that user can switch filters
    function enableAll() {
        [nameField, ingredientsField, difficultyField].forEach(field => 
            field.disabled = false
        );
    }

    // 4. Add event listeners when field is clicked/focused
    nameField.addEventListener('focus', () => disableOtherFields(nameField));   // When user clicks 'Recipe name' field, disable other 2 fields
    ingredientsField.addEventListener('focus', () => disableOtherFields(ingredientsField));  // When user clicks 'Ingredients' field, disable other 2 fields
    difficultyField.addEventListener('focus', () => disableOtherFields(difficultyField));   // When user clicks 'Difficulty' field, disable other 2 fields

    // 5. Optional: re-enable all fields when user clicks outside form
    document.addEventListener('click', (e) => {
        if (!e.target.closest('form')) {
            enableAll();
        }
    });
});