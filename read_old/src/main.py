import sys
sys.path.append('.')
from src.logging_config import *
from fastapi import FastAPI, Request, APIRouter
import logging
from logging.handlers import RotatingFileHandler
from src.routers import routes, stops
from src.routers import route_paths
from src.routers import search
from src.routers import makro_locations
from src.routers import traffic
from src.routers import auth, friendship, location_share, dashboard
from fastapi.responses import JSONResponse
from src.routers import complaints, feedback
from fastapi.responses import RedirectResponse

# إعداد ملف اللوغ
log_file = 'server.log'
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# إعداد root logger
logging.basicConfig(level=logging.INFO, handlers=[file_handler])

app = FastAPI(
    title="Makroji API",
    description="API for Makroji transportation app with authentication, friendship, and location sharing features",
    version="1.0.0"
)

# Middleware لتسجيل جميع الاستثناءات في ملف اللوغ
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        import traceback
        tb_str = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        logging.error(f"Exception during request {request.method} {request.url.path}:\n{tb_str}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.middleware("http")
async def log_requests(request: Request, call_next):
    access_logger = logging.getLogger('access')
    response = await call_next(request)
    access_logger.info(f"{request.method} {request.url.path} - {response.status_code} - {request.client.host}")
    return response

app.include_router(route_paths.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Hello, Makroji!"}

app.include_router(routes.router, prefix="/api/v1")
app.include_router(stops.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(makro_locations.router, prefix="/api/v1")
app.include_router(traffic.router, prefix="/api/v1")

# Authentication and social features
app.include_router(auth.router, prefix="/api/v1")
app.include_router(friendship.router, prefix="/api/v1")
app.include_router(location_share.router, prefix="/api/v1")

# Government Dashboard
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(complaints.router, prefix="/api/v1")
app.include_router(feedback.router, prefix="/api/v1")

health_router = APIRouter()
@health_router.get("/health")
def health_check():
    return {"status": "healthy"}
app.include_router(health_router, prefix="/api/v1")

@app.get("/api/v1/docs")
def custom_docs():
    return RedirectResponse(url="/docs")

@app.get("/api/v1/redoc")
def custom_redoc():
    return RedirectResponse(url="/redoc") 