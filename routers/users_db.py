from fastapi import HTTPException, status
from fastapi import APIRouter, HTTPException, status
from db.models.models import User
from db.schemas.user import user_schema,  users_from_db_schema, user_db_schema
from passlib.context import CryptContext

from db.client import db_client
from bson import ObjectId, errors
from utils.utils import get_user_by_id

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_by_key(key: str, value: str | ObjectId):

    # Buscar al usuario en MongoDB según su clave de valor
    user = db_client.users.find_one({key: value})
    if user:
        user_dict = user_schema(user)  # Convertir a diccionario
        return user_dict
    else:
        return None


@router.get("/", response_model=list[User])  # LISTA DE USUARIOS
async def users():
    if db_client.users.find():
        return users_from_db_schema(db_client.users.find())
    else:
        return None


@router.get("/{user_id}")  # usuario especifico
async def get_user(user_id: str):
    return get_user_by_id(ObjectId(user_id))


# CREATE USER
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def createUser(user: User):
    if get_by_key("email", user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La dirección de correo ya está asociada a un usuario",
        )
    try:
        # Encriptar la contraseña
        hashed_password = get_password_hash(user.password.encode('utf-8'))

        # Crear un diccionario del usuario con la contraseña encriptada
        user_dict = dict(user)
        user_dict["password"] = hashed_password

        # Insertar el usuario en la base de datos
        result = db_client.users.insert_one(user_dict)
        # Asignar el ObjectId generado por MongoDB al nuevo usuario
        new_user = user.copy()
        new_user.id = str(result.inserted_id)

        new_user.password = None

        return new_user

    except HTTPException as e:
        return e


# UPDATE USER
@router.put("/{user_id}")
def update_user(user_id: str, user: User):
    # Convertir el modelo a un diccionario, eliminando los valores vacíos
    user_data = user.dict(exclude_unset=True)

    try:
        # Verificar si el usuario existe en la base de datos
        existing_user = db_client.users.find_one({"_id": ObjectId(user_id)})
        if existing_user is None:
            raise HTTPException(status_code=404, detail="El usuario no existe")

        # si existe el usuario aplicar encoding a la contraseña
        if user_data.get("password"):
            user_data["password"] = get_password_hash(
                user_data["password"].encode('utf-8'))

        # Actualizar el usuario en la base de datos
        db_client.users.update_one(
            {"_id": ObjectId(user_id)}, {"$set": user_data})

        return {"message": "Usuario actualizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# DELETE USER
@router.delete("/{user_id}")
async def delete_user(user_id: str):
    # Convert the user_id string to a MongoDB ObjectId
    try:
        # Verify if the user_id is a valid ObjectId
        user_object_id = ObjectId(user_id)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    # Check if the user exists
    user = db_client.users.find_one({"_id": user_object_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    result = db_client.users.delete_one({"_id": user_object_id})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}

    raise HTTPException(status_code=500, detail="User deletion failed")
