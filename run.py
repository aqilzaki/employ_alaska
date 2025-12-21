from app import create_app
from dotenv import load_dotenv
import os


load_dotenv()


app = create_app()

if __name__ == '__main__':
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'

    app.run(host=host, port=port, debug=debug)
