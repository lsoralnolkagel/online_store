from flask import Flask, request, jsonify
import uuid
import re
import datetime
import json


app = Flask(__name__)

@app.route('/')
def get_greeting():
    return 'Welcome to my website!'


@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = str(uuid.uuid4())

    def validate_data(data):
        age = data.get('age')
        if not age or age < 1 or age > 100:
            return False

        phone = data.get('phone')
        if not phone or not re.match('^[0-9]{11}$', phone):
            return False

        try:
            birthday = datetime.datetime.strptime(data.get('birthday'), '%Y-%m-%d')
        except ValueError:
            return False
        if birthday > datetime.datetime.today():
            return False

        return True

    if not validate_data(data):
        return 'Invalid age, birthday date and/or phone number', 400

    user = {"id": user_id,
            "name": data["name"],
            "surname": data["surname"],
            "age": data["age"],
            "phone": data["phone"],
            "birthday": data["birthday"]}

    with open('users.json', 'r') as file:
        users = json.load(file)
    users.append(user)
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)
    return 'User created successfully', 200


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    with open('users.json', 'r') as file:
        users = json.load(file)
        for user in users:
            if "id" in user and user["id"] == id:
                return jsonify(user)


if __name__ == '__main__':
    app.run()
