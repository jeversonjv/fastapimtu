from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from util.rabbitmq import RabbitMQClient
from util.get_database import get_db
import sql_app.crud as crud
from prometheus_fastapi_instrumentator import Instrumentator
import json

rabbitmq = RabbitMQClient()
app = FastAPI()
Instrumentator().instrument(app).expose(app)


@app.get("/get_history/{id}")
async def get_history(id: int, db: Session = Depends(get_db)):
    history = crud.get_history(db=db, id=id)
    if history is None:
        return {
            "code": "404",
            "msg": "not found"
        }
    return history


@app.get("/get_all_history")
async def get_all_history(db: Session = Depends(get_db)):
    history = crud.get_all_history(db=db)
    return history


@app.post("/dtm")
async def create_dtm(info: Request):
    info = await info.json()
    dtms = info.get("dtms", [])
    for idx, dtm in enumerate(dtms):
        if "states" not in dtm or len(dtm["states"]) == 0:
            return {
                "code": "400",
                "msg": "states cannot be empty, dtm index: " + str(idx)
            }

        if "input_symbols" not in dtm or len(dtm["input_symbols"]) == 0:
            return {
                "code": "400",
                "msg": "input_symbols cannot be empty, dtm index: " + str(idx)
            }

        if "tape_symbols" not in dtm or len(dtm["tape_symbols"]) == 0:
            return {
                "code": "400",
                "msg": "tape_symbols cannot be empty, dtm index: " + str(idx)
            }

        if "initial_state" not in dtm or dtm["initial_state"] == "":
            return {
                "code": "400",
                "msg": "initial_state cannot be empty, dtm index: " + str(idx)
            }

        if "blank_symbol" not in dtm or dtm["blank_symbol"] == "":
            return {
                "code": "400",
                "msg": "blank_symbol cannot be empty, dtm index: " + str(idx)
            }

        if "final_states" not in dtm or len(dtm["final_states"]) == 0:
            return {
                "code": "400",
                "msg": "final_states cannot be empty, dtm index: " + str(idx)
            }

        if "transitions" not in dtm or len(dtm["transitions"]) == 0:
            return {
                "code": "400",
                "msg": "transitions cannot be empty, dtm index: " + str(idx)
            }

        if "input" not in dtm or dtm["input"] == "":
            return {
                "code": "400",
                "msg": "input cannot be empty, dtm index: " + str(idx)
            }

    for dtm in dtms:
        rabbitmq.publish_message(json.dumps(dtm))

    return {
        "code": "200",
        "msg": "messages published in rabbitmq"
    }
