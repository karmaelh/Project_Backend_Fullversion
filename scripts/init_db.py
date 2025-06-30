print("Script started")  # Ligne ajoutée

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import engine
from app.db.base import Base
from app.models import user

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    init_db()
