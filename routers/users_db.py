from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId
import bcrypt


router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


# Helper
def search_user(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}

# LISTA DE USUARIOS


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# USUARIO ESPECIFICO


@router.get("/")  # Query
async def one_user(id: str):
    return search_user("_id", ObjectId(id))


# CREATE USER
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def createUser(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")

    try:
        # Encriptar la contraseña
        hashed_password = bcrypt.hashpw(
            user.password.encode('utf-8'), bcrypt.gensalt())

        # Crear un diccionario del usuario con la contraseña encriptada
        user_dict = dict(user)
        user_dict["password"] = hashed_password.decode('utf-8')
        del user_dict["id"]  # autogenerado por mongodb

        # Insertar el usuario en la base de datos
        id = db_client.users.insert_one(user_dict).inserted_id
        new_user = user_schema(db_client.users.find_one({"_id": id}))

        return User(**new_user)

    except HTTPException as e:
        return e
# UPDATE USER


@router.put("/", response_model=User)
async def update_user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))

# DELETE USER


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}
