from fastapi import FastAPI
from .db import Base, engine
from .routes import pets, center, adoption_status, vaccines

# Inicializar tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MS1 Pets")

app.include_router(pets.router)
app.include_router(center.router)
app.include_router(adoption_status.router)
app.include_router(vaccines.router)
