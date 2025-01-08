from dotenv import load_dotenv
import os

load_dotenv()
    
class Config:
    API_TITLE = "Blog API"
    API_VERSION = "v1"

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///blog.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_PERMANENT = os.getenv("SESSION_PERMANENT", False)
    SESSION_TYPE = os.getenv("SESSION_TYPE", 'filesystem')

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", '94a4d3d2778599510619efe3862fbaa3a922407b86ff0c1ad823173076d88f2e')  
