from app import create_app
from flask_cors import CORS
from flask_migrate import Migrate
from app.db.session import db
from dotenv import load_dotenv
import os

load_dotenv()
print("Clé API OpenAI :", os.getenv("OPENAI_API_KEY"))

app = create_app()
migrate = Migrate(app, db) 

for rule in app.url_map.iter_rules():
    print(f"{rule.methods} -> {rule.rule}") 

if __name__ == "__main__":
    app.run(debug=True)
