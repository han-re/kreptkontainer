from flask import Flask, jsonify

app = Flask(__name__)
#creating instance of flask application
#Python built in that represents the name of the current module

@app.route('/hello')
#route decorater - 
def hello():
    return jsonify({"message": "Hello from Flask, Yessir!"})

@app.route('/status')
def status():
    return jsonify({"status": "API is running smoothly,", "version": "1.0"})

@app.route('/data')
def data():
    fake_db = {
        "users": [ #q about users
            {"id":1, "name": "Alice", "role": "admin"},
            {"id":2, "name": "Bob", "role": "user"},
            {"id":3, "name": "Charlie", "role": "moderator"} #q about semi colons
        ]
    }
    return jsonify(fake_db)

@app.route('/user/<int:user_id>')
def get_user(user_id):
    users = [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "moderator"} 
    ]
    user = next((u for u in users if u["id"] == user_id), None)
    
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)