from fastapi import FastAPI
from fastapi.responses import Response
from env import Env
import routes, middleware

app = FastAPI()

middleware.include(app)
routes.include(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=5002,
        reload=True,
        log_config="./logging.ini" if not Env.DEBUG else None
    )