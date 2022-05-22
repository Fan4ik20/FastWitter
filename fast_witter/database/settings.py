import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

blog_engine = create_engine(
    os.getenv('DB_URL')
)

BlogSession = sessionmaker(autoflush=False, bind=blog_engine)
