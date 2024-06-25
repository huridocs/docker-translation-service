import sys
from fastapi import FastAPI, HTTPException
from configuration import service_logger
from src.data_model.TranslationTask import TranslationTask
from src.translate import get_translations

app = FastAPI()


@app.get("/")
async def info():
    return sys.version


@app.post("/")
async def run(translation_task: TranslationTask):
    try:
        return get_translations(translation_task)
    except Exception:
        service_logger.error("Error", exc_info=1)
        raise HTTPException(status_code=422, detail="Error getting translation")
