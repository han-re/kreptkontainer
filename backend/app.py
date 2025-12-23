from flask import Flask, jsonify, request
from models import db, User
from config import Config
import os
import socket

app = Flask(__name__)
#creating instance of flask application
#Python built in that represents the name of the current module
app.config.from_object(Config) #Loads database configuration
db.init_app(app) #Connects database to Flask app


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

#methods=['GET'], POST
@app.route('/users', methods=['GET'])
def get_user_db():
    users = User.query.all() #Query all users (Basically how you get the data in db out)
    jsonify([
        users.to_dict() for user in users #user is basically just the temp variable in the for loop used to define each iteration (same as using i in a for loop)

    ])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() #Gets json data from request body (using request module)


    #Validation n dat
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({
            'error': 'Missing Username or Email'
        }), 400
    
    try:
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        db.session.add(new_user)
        db.session.commit
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback() #Rollback if there's an error
        return jsonify({
            'error': str(e)
        }), 400

@app.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    #Get a specific user from database
    user = User.query.get_or_404(id) #Gets user or returns 404
    return jsonify(user.to_dict())

@app.route('/users/<int:id>', methods=['POST'])
#Deleting a user from db
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user) #Staging deletion of user
        db.session.commit() #Actually deletes it
        return '', 204 #Returns empty response with no content
    except Exception as e:
        db.session.rollback() 
        return jsonify({
            'error': str(e)
        }), 400




if __name__ == '__main__':
    print(f"Starting Flask API {API_VERSION} in {ENVIRONMENT} mode")
    print(f"Log Level: {LOG_LEVEL}")
    print(f"Pod Name: {os.environ.get('HOSTNAME', 'localhost')}")
    print(f"Secrets loaded: DB={bool(DATABASE_PASSWORD)}, API={bool(API_KEY)}, JWT={bool(JWT_SECRET)}")

    #Creates database tables if they don't exist already
    with app.app_context():
        db.create_all()
        print("Database tables created/verified")
    
    app.run(host="0.0.0.0", port=5000, debug=(ENVIRONMENT == 'development'))
    
