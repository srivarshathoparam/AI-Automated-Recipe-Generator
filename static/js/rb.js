document.getElementById("searchBar").addEventListener("input", debounce(searchRecipes, 1000));

function debounce(func, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
}

async function searchRecipes() {
    const input = document.getElementById("searchBar");
    const filter = input.value.trim().toLowerCase();
    const recipeContainer = document.getElementById("recipeResults");

    if (filter.length === 0) {
        recipeContainer.innerHTML = ""; // Clear results
        return;
    }

    recipeContainer.innerHTML = "<p>Searching...</p>"; // Show loader

    let foundMatch = false;

    // Get all existing recipe and cuisine cards
    const recipeCards = document.querySelectorAll(".recipe-card");
    const cuisineCards = document.querySelectorAll(".cuisine-card");

    function filterCards(cards) {
        cards.forEach(card => {
            let title = card.querySelector("h3");
            if (title && title.innerText.toLowerCase().includes(filter)) {
                card.style.display = "";
                foundMatch = true;
            } else {
                card.style.display = "none";
            }
        });
    }

    // Filter visible cards
    filterCards(recipeCards);
    filterCards(cuisineCards);

    if (foundMatch) {
        recipeContainer.innerHTML = ""; // Clear loader if matched locally
        return;
    }

    try {
        const response = await fetch(`/search?q=${encodeURIComponent(filter)}`);
        
        if (!response.ok) throw new Error("Fetch failed");

        const data = await response.json();

        if (data.found && data.recipes && data.recipes.length > 0) {
            displayRecipes(data.recipes);
        } else {
            // Try AI fallback
            await generateAIRecipe(filter);
        }

    } catch (error) {
        console.error("Error fetching recipes:", error);
        recipeContainer.innerHTML = "<p style='color: red;'>Error fetching recipe...</p>";
    }
}

// ✅ Function to display multiple recipes
function displayRecipes(recipes) {
    let recipeContainer = document.getElementById("recipeResults");
    recipeContainer.innerHTML = ""; // Clear old results

    if (recipes.length === 0) {
        recipeContainer.innerHTML = "<p>No recipes found.</p>";
        return;
    }

    // Only show the first 10 recipes
    const topRecipes = recipes.slice(0, 10);

    topRecipes.forEach(recipe => {
        let imageUrl = recipe.image || "default-image.jpg";
        let title = recipe.name || recipe.title || "Untitled Recipe";
        let description = recipe.description || "A delicious recipe!";

        let recipeCard = `
            <div class="recipe-card">
                <img src="${imageUrl}" alt="${title}">
                <h3>${title}</h3>
                <p>${description}</p>
                <a href="/recipe/${recipe.id || '#'}">View Recipe</a>
            </div>
        `;
        recipeContainer.innerHTML += recipeCard;
    });
}


// ✅ Function to Generate AI-Based Recipe
async function generateAIRecipe(query) {
    const recipeContainer = document.getElementById("recipeResults");

    try {
        console.log("Attempting AI generation for:", query);

        let aiResponse = await fetch(`/api/generate-recipe`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredients: [query], preferences: "None" })
        });

        if (!aiResponse.ok) {
            throw new Error("AI route failed: " + aiResponse.status);
        }

        let aiData = await aiResponse.json();
        console.log("AI Response:", aiData);

        if (aiData.recipe) {
            displayRecipes([aiData.recipe]); // Show AI-generated recipe
        } else {
            recipeContainer.innerHTML = "<p>No recipes found.</p>";
        }

    } catch (error) {
        console.error("Error generating AI recipe:", error);
        recipeContainer.innerHTML = "<p style='color: red;'>Failed to generate a recipe.</p>";
    }
}

function generateSlug(title) {
    return title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

    recipes.forEach(recipe => {
        let slug = generateSlug(recipe.title);
        let html = `
          <div class="recipe-card">
            <img src="${recipe.image_url}" alt="${recipe.title}" />
            <h3>${recipe.title}</h3>
            <p>${recipe.description}</p>
            <a href="/recipe/${slug}">
              <button class="view-btn">View Recipe</button>
            </a>
          </div>
        `;
      
        document.getElementById("recipes-container").innerHTML += html;
      });
}

