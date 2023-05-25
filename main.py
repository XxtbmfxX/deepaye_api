from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
# from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=12475
app.include_router(products.router)
app.include_router(users.router)

# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=14094
app.include_router(basic_auth_users.router)

# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=17664
app.include_router(jwt_auth_users.router)

# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=20480
app.include_router(users_db.router)

# Clase en vídeo: https://youtu.be/_y9qQZXE24A?t=13618
# app.mount("/static", StaticFiles(directory="static"), name="static")


# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc
