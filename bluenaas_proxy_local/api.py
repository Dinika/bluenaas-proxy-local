from typing import Any
from fastapi import FastAPI, Request, WebSocket
from fastapi.websockets import WebSocketState
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


class ConnectionManager:
    def __init__(self):
        self.connection: WebSocket

    def add_connection(self, websocket: WebSocket):
        self.connection = websocket

    def get_status(self):
        print("----------")
        print("@@status/client:", self.connection.client_state)
        print("@@status/app:", self.connection.application_state)
        print("----------")

    async def send_message(self, message: Any):
        ws = self.connection
        if ws.application_state == WebSocketState.CONNECTED:
            await ws.send_json(message)
        else:
            print("WebSocket connection is closed.")


connection_manager = ConnectionManager()


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global global_token
    connection_manager.add_connection(websocket)
    token = websocket.headers["sec-websocket-protocol"]
    bearer = token.replace("Bearer-", "", 1)
    

    try:
        if not global_token and check_token(bearer):
            global_token = token
            post(
                f"{bluenaas_endpoint}/init",
                json={"token": token.replace("Bearer-", "Bearer ")},
            )
            resp = post(
                f"{bluenaas_endpoint}/default",
                json={},
            )
            js = resp.json()
            await connection_manager.send_message(js)
        elif global_token and check_token(global_token.replace("Bearer-", "", 1)):
            while True:
                client_data = await websocket.receive_json()
                resp = post(f"{bluenaas_endpoint}/default", json=client_data)
                js = resp.json()
                await connection_manager.send_message(js)
    except Exception as e:
        print(
            f"websocket_endpoint/e: {type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}"
        )


@app.post("/naas")
async def message_from_bluenaas(request: Request) -> None:
    try:
        connection_manager.get_status()
        msg = await request.json()
        print("MESSAGE", msg)
        await connection_manager.send_message(msg)
        return None
    except Exception as e:
        print("/naas/e", e)
