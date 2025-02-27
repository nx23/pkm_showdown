import json

with open('config.json') as f:
    env = json.load(f)

SECRET_KEY = env["secret_key"]
ALGORITHM = env["refresh_token"]["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = env["refresh_token"]["expires_in"]["minutes"]
HOST = env["host"]
PORT = env["port"]
DEBUG = env["debug"]
DATABASE_URL = env["database"]["url"]