from database import engine
from models import Post

Post.metadata.create_all(bind=engine)
