#This file at a high-level should 
#   1. Load environment variables
#   2. Provide a single place for configuration
#   3. Work unchanged across local, Docker and Kubernetes

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost:5432/kreptkon'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False