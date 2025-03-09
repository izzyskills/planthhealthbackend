from fastapi import FastAPI

from src.auth.routes import auth_router
from src.predictions.routes import prediction_router
from .errors import register_all_errors

from .middleware import register_middleware


version = "v1"

description = """
PlantHealth API
- Register and Login
- Predict plant disease using image
- Get plant disease information
    """

version_prefix = f"/api/{version}"

app = FastAPI(
    title="PlantHealth",
    description=description,
    version=version,
    license_info={"name": "GPLv3", "url": "https://www.gnu.org/licenses/gpl-3.0.html"},
    contact={
        "name": "Omola Israel",
        "url": "https://github.com/izzyskills",
    },
    terms_of_service="https://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
)

register_all_errors(app)

register_middleware(app)


app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(
    prediction_router, prefix=f"{version_prefix}/predictions", tags=["predictions"]
)
