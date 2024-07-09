from fastapi import FastAPI, WebSocket
from requests import post

app = FastAPI()

bluenass_endpoint = "http://localhost:8000"


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        token = websocket.headers["sec-websocket-protocol"]
        # await websocket.send_text(f"Message text was: {data}")
        # token = data["token"]
        response = post(f"{bluenass_endpoint}/init", json={"token": token})
        # print("Token", response)
