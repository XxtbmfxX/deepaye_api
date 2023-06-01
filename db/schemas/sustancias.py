
def sustancia_schema(sustancia) -> dict:
    return {
        "id": str(sustancia["_id"]),
        "nombre_sustancia": sustancia["nombre_sustancia"],
        "descripcion": sustancia["descripcion"],
        "foto": sustancia["foto"]
    }


def sustancias_schema(sustancias) -> list:
    return [sustancia_schema(sustancia) for sustancia in sustancias]
