document.addEventListener("DOMContentLoaded", function () {
    // Ensure the search button exists before adding an event listener
    const searchBtn = document.querySelector(".search-btn");
    if (searchBtn) {
        searchBtn.addEventListener("click", () => {
            const selectedIngredients = getSelectedIngredients(); // Get selected ingredients

            if (selectedIngredients.length === 0) {
                alert("Please select at least one ingredient.");
                return;
            }

            fetch("http://127.0.0.1:5000/generate_recipe", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ingredients: selectedIngredients })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("recipe-result").innerText = data.recipe || "No recipe found.";
            })
            .catch(error => console.error("Error:", error));
        });
    }
});

// Function to collect selected ingredient names
function getSelectedIngredients() {
    let selected = [];
    document.querySelectorAll(".ingredient-card.selected").forEach(card => {
        const ingredientName = card.querySelector("img").alt;
        selected.push(ingredientName);
    });
    return selected;
}

// Function to toggle ingredient selection and tick mark
function toggleSelect(element) {
    element.classList.toggle("selected");
}
