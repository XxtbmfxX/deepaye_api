from fastapi import HTTPException, status
from fastapi import APIRouter, HTTPException, status
from db.models.models import User
from db.schemas.user import user_schema,  users_from_db_schema, user_db_schema
from passlib.context import CryptContext

from db.client import db_client
from bson import ObjectId
from utils.utils import get_user_by_id

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def get_by_key(key, value):
    return user_db_schema(db_client.users.find_one({key: value}))


# LISTA DE USUARIOS


@router.get("/")  # response_model=list[User]
async def users():
    if db_client.users.find():
        return users_from_db_schema(db_client.users.find())
    else:
        return None


@router.get("/one/{id}")  # Query
async def one_user(id: str):
    return get_user_by_id(ObjectId(id))


# CREATE USER
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def createUser(user: User):
    if get_by_key("email", user.email) != None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="La dirección de correo ya está asociada a un usuario")

    try:
        # Encriptar la contraseña
        hashed_password = get_password_hash(user.password.encode('utf-8'))

        # Crear un diccionario del usuario con la contraseña encriptada
        user_dict = dict(user)
        user_dict["password"] = hashed_password

        # Insertar el usuario en la base de datos
        id = db_client.users.insert_one(user_dict).inserted_id
        new_user = user_schema(db_client.users.find_one({"_id": id}))

        return User(**new_user)

    except HTTPException as e:
        return e

# UPDATE USER

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Endpoint para actualizar un usuario
@router.put("/{user_id}")
def update_user(user_id: str, user: User):
    # Convertir el modelo a un diccionario, eliminando los valores vacíos
    user_data = user.dict(exclude_unset=True)

    try:
        # Verificar si el usuario existe en la base de datos
        existing_user = db_client.users.find_one({"_id": ObjectId(user_id)})
        if existing_user is None:
            raise HTTPException(status_code=404, detail="El usuario no existe")

        # Actualizar el usuario en la base de datos
        db_client.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": user_data})

        return {"message": "Usuario actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE USER

 # Still having a little bug but it works


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    try:
        found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
        if found is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no fue encontrado")
        else:
            return {"message": "Usuario eliminado correctamente"}
    except Exception as e:
        return {"datail": e}
