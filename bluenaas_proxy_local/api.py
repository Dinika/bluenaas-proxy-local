from typing import Any
from fastapi import FastAPI, Request, WebSocket
from requests import post
import jwt

app = FastAPI()

bluenaas_endpoint = "http://localhost:8000"

global_ws: WebSocket | None = None
global_token: str | None = None

def check_token(token: str) -> bool:
    try:
        jwt.decode(token, options={"verify_signature": False})
        return True
    except Exception as e:
        return False
    
@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global global_ws
    global global_token
    global_ws = websocket
    token = websocket.headers["sec-websocket-protocol"]
    bearer = token.replace("Bearer-", "", 1)

    try:
        if not global_token and check_token(bearer):
            global_token = token
            post(f"{bluenaas_endpoint}/init", json={"token": token})
            resp = post(f"{bluenaas_endpoint}/default", json={})
            js = resp.json()
            await websocket.send_json(js)
        elif global_token and check_token(global_token.replace("Bearer-", "", 1)):
            client_data = await websocket.receive_json()
            resp = post(f"{bluenaas_endpoint}/default", json=client_data)
            js = resp.json()
            await websocket.send_json(js)
    except Exception as e:
        print(
            f"websocket_endpoint/e: {type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}"
        )
    finally:
        await websocket.close()


@app.post("/naas")
async def message_from_bluenaas(request: Request) -> None:
    try:
        msg = await request.json()
        print("MESSAGE", msg)
        await global_ws.send_json(msg)
        return None
    except Exception as e:
        print('e', e)


@app.post("/healthz")
async def healthz(msg: Any) -> None:
    return {"message": "running ok"}
