from fastapi import FastAPI
from app.db.session import init_db
from app.routes import pets, centers, vaccines, status
from app.errors import init_error_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title="Pet Adoption API",
        version="1.0.0",
        description="Pet adoption management microservice"
    )

    init_db()
    init_error_handlers(app)

    # Routers
    app.include_router(pets.router)
    app.include_router(centers.router)
    app.include_router(vaccines.router)
    app.include_router(status.router)

    return app
