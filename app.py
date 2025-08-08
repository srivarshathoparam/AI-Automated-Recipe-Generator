from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from mongo_connection import db
from routes import recipe_routes, auth_routes
from login import login_blueprint  # Import login Blueprint

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Set secret key for sessions
app.secret_key = os.getenv("SECRET_KEY", "supersecretdevkey") 

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")  # Add Secret Key for JWT

# Register Blueprints (Organizing Routes)
app.register_blueprint(recipe_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(login_blueprint, url_prefix="/auth")  # ✅ Register Login Routes

# Run Flask Server
if __name__ == "__main__":
    app.run(debug=True)
