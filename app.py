from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, Integer, String, create_engine
from faker import Faker
import os
from dotenv import load_dotenv

load_dotenv()

# Create a new Flask application - carla

class Base(DeclarativeBase):
    pass

app = Flask(__name__)

# Configure the database

db = SQLAlchemy(model_class=Base)
DB_URL = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
engine = create_engine(DB_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Define the model

class User(db.Model):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    name : Mapped[str] = mapped_column(String(25), nullable=False)
    last_name : Mapped[str] = mapped_column(String(25), nullable=False)
    email : Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    
    
# Create the database

with app.app_context():
    db.create_all()
    

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)



@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = [{'id': user.id, 'name': user.name, 'last_name': user.last_name, 'email': user.email} for user in users]
    return jsonify(users)  


@app.route('/users', methods=['POST'])
def create_user():
    fake = Faker()
    for i in range(10):
        user = User(
            name = fake.first_name(),
            last_name = fake.last_name(),
            email = fake.email()
        )
        
        db.session.add(user)
        db.session.commit()
        
    return jsonify({'message': 'Users created successfully!'})


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully!'})
    else:
        return jsonify({'message': 'User not found!'}), 404
    
    
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if user:
        user.name = 'Updated Name'
        db.session.commit()
        return jsonify({'message': 'User updated successfully!'})
    else:
        return jsonify({'message': 'User not found!'}), 404
    
    

    



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5600)