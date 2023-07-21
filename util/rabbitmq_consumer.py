from rabbitmq import RabbitMQClient
from automata.tm.dtm import DTM
from sqlalchemy.orm import Session
from email_body import EmailSchema
from sql_app import crud, schemas
import asyncio

import send_mail
import get_database
import json

rabbitmq = RabbitMQClient()


async def dtm(body):
    info = json.loads(body)

    print(dict(info.get("transitions", [])))

    dtm = DTM(
        states=set(info.get("states", [])),
        input_symbols=set(info.get("input_symbols", [])),
        tape_symbols=set(info.get("tape_symbols", [])),
        transitions=dict(info.get("transitions", {})),
        initial_state=info.get("initial_state", ""),
        blank_symbol=info.get("blank_symbol", ""),
        final_states=set(info.get("final_states", []))
    )

    if dtm.accepts_input(info.get("input", "")):
        print('accepted')
        result = "accepted"
    else:
        print('rejected')
        result = "rejected"

    with get_database.get_db() as db:
        history = schemas.History(query=str(info), result=result)
        crud.create_history(db=db, history=history)

    email_shema = EmailSchema(email=["to@example.com"])
    await send_mail.simple_send(email_shema, result=result, configuration=str(info))


def callback(ch, method, properties, body):
    asyncio.run(dtm(body))


rabbitmq.consume_messages(callback)
