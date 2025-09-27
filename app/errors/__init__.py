from fastapi import FastAPI
from .handlers import register_exception_handlers


def init_error_handlers(app: FastAPI):
    register_exception_handlers(app)
