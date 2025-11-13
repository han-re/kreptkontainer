from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)
#creating instance of flask application
#Python built in that represents the name of the current module

# Function to insert pod data in, makes it easier as we don't have to repeat the pod code.
def pod_data(data):
    return {
        **data, # this unpacks the data directory. As we're creating a dictionary, if we want to return the data we need to exit the dictionary so this ** command exits the dictionary. 
        "pod_name": os.environ.get("HOSTNAME", "unknown"),
        # This basically gets the environment variable named "HOSTNAME", if hostname isn't set it returns unknown. For context os.environ is mapping the environment variables in the os and  .get just fetches it.
        "pod_ip": socket.gethostbyname(socket.gethostname())
        # This gets the ip address of the pod. So .gethostname() basically gets the the hostname of the current machine OR in our case the current container. and .gethostbyname() translates that hostname into an IPv4 address. 
    }

@app.route('/hello')
#route decorater - 
def hello():
    return jsonify({
        "message": "Hello from Flask, Yessir!",
        "pod_name": os.environ.get("HOSTNAME", "unknown"),
        "pod_ip": socket.gethostbyname(socket.gethostname()) 
    })


@app.route('/status')
def status():
    return jsonify({
        "status": "API is running smoothly,", "version": "1.0",
        "pod_name": os.environ.get("HOSTNAME", "unknown"),
        "pod_ip": socket.gethostbyname(socket.gethostname())
        })

@app.route('/data')
def data():
    fake_db = {
        "users": [ #q about users
            {"id":1, "name": "Alice", "role": "admin"},
            {"id":2, "name": "Bob", "role": "user"},
            {"id":3, "name": "Charlie", "role": "moderator"} #q about semi colons
        ]
    }

    
    return jsonify(pod_data(fake_db))

@app.route('/user/<int:user_id>')
def get_user(user_id):
    users = [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "moderator"} 
    ]

    # Loops through the "users" dictionary then yields the name that is equal to user_id.
    user = next((u for u in users if u["id"] == user_id), None)
    
    if user:
        return jsonify(pod_data(user))
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)