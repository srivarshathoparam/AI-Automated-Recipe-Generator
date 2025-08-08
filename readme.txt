## AI Automated Recipe Generator 

The AI Automated Recipe Generator is an intelligent web application that recommends and generates recipes based on user preferences, available ingredients, and dietary requirements.
It combines Flask (Python backend), MongoDB (database), and HTML/CSS/JavaScript (frontend) with AI-powered recommendation algorithms to provide a personalized cooking experience.

# Key Features
Personalized Recommendations – Suggests recipes based on user profile data such as:
Dietary restrictions
Allergies
Favorite cuisines
Preferred meal types (breakfast, lunch, dinner, snacks, etc.)
Ingredient-Based Search – Select or input available ingredients, and the system finds recipes you can cook right now.
AI-Generated Recipes – Creates unique, never-seen-before recipes with step-by-step instructions and AI-generated images.
Cuisine Explorer – Browse recipes by cuisine type (Italian, Indian, Mexican, Chinese, etc.).
Recipe Detail Pages – Full cooking process with feedback, review, and comment sections.
User Profiles – Store preferences, liked recipes, and recently viewed dishes.
Responsive UI – Elegant, mobile-friendly design with an adaptive navigation bar.
Dataset Integration – Works with a large recipe dataset for better recommendations.

# Tech Stack
## Frontend
HTML5, CSS3, JavaScript (Vanilla)
Responsive design with modern styling
Dynamic rendering for recipe cards and cuisines

## Backend
Python Flask (REST API endpoints)
AI-based recommendation engine (content-based filtering + custom rules)
Integration with large recipe datasets

## Database
MongoDB Atlas (cloud-hosted, scalable)

## AI/ML
Ingredient and preference-based filtering
AI text generation for unique recipes
AI image generation for dishes

## How It Works
User Login/Register → Create a profile with preferences, allergies, and favorite cuisines.
Ingredient Search → Select from ingredient images or enter text manually.
AI Processing → Backend AI combines dataset matches + preferences to recommend recipes.
View Recipe → Get step-by-step instructions, cooking tips, and images.
Feedback Loop → Users can like, rate, and comment to improve recommendations.

## Future Enhancements
Voice-based recipe search.
Meal planning for an entire week.
Grocery list generation from selected recipes.
Real-time nutrition analysis.