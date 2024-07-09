from fastapi import FastAPI, WebSocket
from requests import post

app = FastAPI()

bluenass_endpoint = "http://localhost:8000"

websocket_conn: any = None


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        websocket_conn = websocket
        print(websocket_conn)
        token = websocket.headers["sec-websocket-protocol"]
        post(f"{bluenass_endpoint}/init", json={"token": token})


@app.post("/")
async def message_from_bluenaas(msg: any):
    print("MESSAGE", msg)
    websocket_conn.send_json(msg)
