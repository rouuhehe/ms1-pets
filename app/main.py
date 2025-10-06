from fastapi import FastAPI
from .db import Base, engine
from .routes import pets, center, adoption_status, vaccines
from fastapi.middleware.cors import CORSMiddleware

# Inicializar tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MS1 Pets")

origins = [
    "https://main.d28p0502xzwadt.amplifyapp.com",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pets.router)
app.include_router(center.router)
app.include_router(adoption_status.router)
app.include_router(vaccines.router)
