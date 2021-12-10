import uvicorn
from settings import settings


uvicorn.run("backend.app:app", host=settings.server_host, port=settings.server_port, reload=True)
