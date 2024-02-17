from fastapi import FastAPI

from api.routers import molecule


app = FastAPI()
app.include_router(molecule.router)
