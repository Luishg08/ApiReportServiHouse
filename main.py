import webbrowser 
from fastapi import FastAPI

app = FastAPI()

# Prueba para verificar que FastAPI está funcionando bien
@app.get("/TestApiReport")
def read_root():
    return {"message": "Hola desde ApiReport"}


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8088/docs") # Se abre automáticamente Swagger UI para la documentación de ApiReport

# Ejecutar con siguiente comando: $ uvicorn main:app --reload --port 8088 --host 0.0.0.0