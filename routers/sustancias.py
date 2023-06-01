from fastapi import APIRouter, HTTPException, status
from db.client import db_client
from db.schemas.sustancias import sustancia_schema, sustancias_schema


router = APIRouter(prefix="/sustancias",
                   tags=["sustancias"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.get("/")
async def sustancias():
    try:
        data = sustancias_schema(db_client.sustancias.find())
        return data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{name}")
async def sustancia(name: str):
    try:
        data = db_client.sustancias.find_one({"nombre_sustancia": name})
        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sustancia no encontrada")
        return data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
