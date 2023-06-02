from fastapi import FastAPI
from routers import jwt_auth_users, users_db, sustancias

app = FastAPI()


app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
app.include_router(sustancias.router)


# Inicia el server:
# py -m uvicorn main:app --reload
