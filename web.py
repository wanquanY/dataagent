import asyncio
import websockets

async def connect_to_websocket():
    async with websockets.connect('ws://127.0.0.1:8000/ws/1') as websocket:  # 将 localhost:8000 替换为你的 FastAPI 服务器地址
        while True:
            try:
                message = await websocket.recv()
                print("Received message from server:", message)
            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed by server")
                break

asyncio.get_event_loop().run_until_complete(connect_to_websocket())
