from sql_app import models
from sql_app.database import engine
from sql_app.database import SessionLocal

models.Base.metadata.create_all(bind=engine)

# Patter Singleton
# Dependency


def get_db():
    db = SessionLocal()
    return db
