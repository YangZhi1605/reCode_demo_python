from BootVueDemo import create_app
from flask_cors import CORS
app = create_app()

if __name__ == '__main__':
    app.run(port=5200, debug=True)
    CORS(app, supports_credentials=True)