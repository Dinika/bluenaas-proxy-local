from typing import Any
from fastapi import Body, FastAPI, WebSocket
from requests import post

app = FastAPI()

bluenaas_endpoint = "http://localhost:8017"

global_ws: WebSocket | None = None


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global global_ws
    global_ws = websocket
    try:
        plain_token = websocket.headers["sec-websocket-protocol"]
        token = plain_token.replace("Bearer-", "Bearer ")
        init_response = post(f"{bluenaas_endpoint}/init", json={"token": token})
        print("Init Response", init_response.json())
        deploy_response = post(f"{bluenaas_endpoint}/default", json={"token": token})
        print("Deploy Response", deploy_response.json())
    except Exception as e:
        print(
            f"websocket_endpoint/e: {type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}"
        )

    while True:
        data = await websocket.receive_json()
        print("Frontend Data", data)
        if data == {}:
            print("Empty data")
            await websocket.send_json({"message": "Processing message"})

        if data.get("cmd") is not None:
            cmd_response = post(f"{bluenaas_endpoint}/default", json=data)
            print("CMD Response", cmd_response.json())


@app.post("/")
async def message_from_bluenaas(msg: Any = Body(None)) -> None:
    print("MESSAGE", msg)

    return None
