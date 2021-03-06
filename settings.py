# Security
import os

SECRET_KEY = 'e43a1b7f1374bc3c556cdab56e599b7fd2a54d48c19c40019920959913cb786e'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 90

# Database
DB_NAME = 'tourneyman'
DB_USER = 'tourneyman'
DB_PASSWORD = 'password'
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = '5432'
SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
