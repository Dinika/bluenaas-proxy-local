import json
from typing import Any
from fastapi import FastAPI, WebSocket
from requests import post
from time import sleep


app = FastAPI()

bluenaas_endpoint = "http://localhost:8005"

global_ws: WebSocket | None = None


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global global_ws
    global_ws = websocket
    try:
        token = websocket.headers["sec-websocket-protocol"]
        init_response = post(f"{bluenaas_endpoint}/init", json={"token": token})
        print("Init Response", init_response.json())
        deploy_response = post(f"{bluenaas_endpoint}/deploy", json={"token": token})
        print("Deploy Response", deploy_response.json())
    except Exception as e:
        print(
            f"websocket_endpoint/e: {type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}"
        )

    await websocket.send_json({"message": "Processing message"})


@app.post("/")
async def message_from_bluenaas(msg: Any) -> None:
    print("MESSAGE", msg)

    return None
