import webbrowser 
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Order, Stock, StockTransaction, Delivery, Location


#No se requieren crear las tablas.

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Prueba para verificar que FastAPI está funcionando bien
@app.get("/TestApiReport")
def read_root():
    return {"message": "Hola desde ApiReport"}





if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8088/docs") # Se abre automáticamente Swagger UI para la documentación de ApiReport

# Ejecutar con siguiente comando: $ uvicorn main:app --reload --port 8088 --host 0.0.0.0