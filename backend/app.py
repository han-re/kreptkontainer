from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)
#creating instance of flask application
#Python built in that represents the name of the current module

#Read configuration from environment variables (ConfigMap)
API_VERSION = os.getenv('API_VERSION', '1.0')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'DEVELOPMENT')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
MAX_CONNECTIONS = os.getenv('MAX_CONNECTIONS', '100')
FEATURE_FLAG_NEW_UI = os.getenv('FEATURE_FLAG_NEW_UI', 'false')


#Read Secrets - Don't expose these
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
API_KEY = os.getenv('API_KEY', '')
JWT_SECRET = os.getenv('JWT_SECRET', '')

# Function to insert pod data in, makes it easier as we don't have to repeat the pod code.
def pod_data(data):
    return {
        **data, # this unpacks the data directory. As we're creating a dictionary, if we want to return the data we need to exit the dictionary so this ** command exits the dictionary. 
        "pod_name": os.environ.get("HOSTNAME", "unknown"),
        # This basically gets the environment variable named "HOSTNAME", if hostname isn't set it returns unknown. For context os.environ is mapping the environment variables in the os and  .get just fetches it.
        "pod_ip": socket.gethostbyname(socket.gethostname()),
        # This gets the ip address of the pod. So .gethostname() basically gets the the hostname of the current machine OR in our case the current container. and .gethostbyname() translates that hostname into an IPv4 address. 
        "version": API_VERSION #Adding version to pod data
    }

@app.route('/hello')
#route decorater - 
def hello():
    return jsonify({
        "message": "Hello from Flask, Yessir!",
        "version": API_VERSION,
        "environment": ENVIRONMENT,
        "pod_name": os.environ.get("HOSTNAME", "unknown"),
        "pod_ip": socket.gethostbyname(socket.gethostname()) 
    })


@app.route('/status')
def status():
    return jsonify({
        "status": "API is running smoothly,", "version": "1.0",
        "version": API_VERSION,
        "environment": ENVIRONMENT,
        "log_level": LOG_LEVEL,
        "max_connections": MAX_CONNECTIONS,
        "pod_name": os.environ.get("HOSTNAME", "unknown"),
        "pod_ip": socket.gethostbyname(socket.gethostname())
        })

@app.route('/config')
def config():
    return jsonify({
        #Non-sensitive configuration and pod info
        "version": API_VERSION,
        "environment": ENVIRONMENT,
        "log_level": LOG_LEVEL,
        "max_connections": MAX_CONNECTIONS,
        "feature_flag_new_ui": FEATURE_FLAG_NEW_UI,
        "secrets_loaded": {
            "database_password": bool(DATABASE_PASSWORD),
            "api_key": bool(API_KEY),
            "jwt_secret": bool(JWT_SECRET)
        },
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
    print(f"Starting Flask API {API_VERSION} in {ENVIRONMENT} mode")
    print(f"Log Level: {LOG_LEVEL}")
    print(f"Pod Name: {os.environ.get('HOSTNAME', 'localhost')}")
    print(f"Secrets loaded: DB={bool(DATABASE_PASSWORD)}, API={bool(API_KEY)}, JWT={bool(JWT_SECRET)}")
    app.run(host="0.0.0.0", port=5000, debug=(ENVIRONMENT == 'development'))