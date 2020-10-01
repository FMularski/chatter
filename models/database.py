"""
Having db in a separate file makes it global and allows to
import it to models files in order to create their fields.
Additionally, it prevents circular imports (from app to model
and then from model to app).
"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
