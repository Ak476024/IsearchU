
from flask import Flask
from flask_cors import CORS
from extensions import db
from routes.drive import drive_bp

app = Flask(__name__)
CORS(app,supports_credentials=True, origins=['*'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db.init_app(app)
app.register_blueprint(drive_bp)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


if __name__ == '__main__':
    app.run(host='localhost',port=5001,debug=True)
