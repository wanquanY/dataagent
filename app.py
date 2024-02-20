# from fastapi import FastAPI, Body
# from pydantic import BaseModel
# from taskweaver.app.app import TaskWeaverApp
# from typing import Optional,List, Dict, Any, Literal

# class UserQuery(BaseModel):
#     user_query: str
#     files: Optional[List[Dict[Literal["name", "path", "content"], Any]]] = None

# app = FastAPI()
# # 启动fastAPI命令：uvicorn app:app --reload，停止命令：Ctrl+C
# #测试命令:curl -X POST "http://localhost:8000/get_response" -H "Content-Type: application/json" -d "{\"user_query\": \"你好\"}
# # 测试命令:curl -X POST "http://localhost:8000/get_response" -H "Content-Type: application/json" -d "{\"user_query\": \"我现在有100万元预算，请你给我筛选15个达人，我希望预期播放量大于1000万\", \"files\": [{\"name\": \"test2.xlsx\", \"path\": \"D:\\\\Synergence\\\\TaskWeaver\\\\TaskWeaver\\\\project\\\\sample_data\\\\test2.xlsx\", \"content\": null}]}"
# @app.post("/get_response")
# def get_response(query: UserQuery):  # 使用 Pydantic 模型来解析和验证请求体
#     app_dir = "D:\Synergence\TaskWeaver\TaskWeaver\project"
#     app = TaskWeaverApp(app_dir=app_dir)
#     session = app.get_session()

#     response_round = session.send_message(query.user_query,files=query.files)
#     return response_round.to_dict()
# 



#import logging
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from pydantic import BaseModel
# from taskweaver.app.app import TaskWeaverApp
# from typing import Optional, List, Dict, Any, Literal
# import asyncio

# # 设置日志格式
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# class UserQuery(BaseModel):
#     user_query: str
#     files: Optional[List[Dict[Literal["name", "path", "content"], Any]]] = None

# app = FastAPI()

# # 用于保存 WebSocket 连接的字典
# websocket_connections = {}

# @app.post("/get_response")
# async def get_response(query: UserQuery):
#     app_dir = "C:\code\TaskWeaver\project"
#     app_instance = TaskWeaverApp(app_dir=app_dir)
#     session = app_instance.get_session()

#     response_round = session.send_message(query.user_query, files=query.files)
#     return response_round.to_dict()

# async def send_response(websocket: WebSocket, client_id: int, response_data: dict):
#     try:
#         await websocket.send_json(response_data)
#         logging.info(f"Sent message to client {client_id}: {response_data}")
#     except WebSocketDisconnect:
#         logging.info(f"WebSocket connection from client {client_id} closed.")

# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     logging.info(f"WebSocket connection from client {client_id} established.")
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             logging.info(f"Received message from client {client_id}: {data}")
#             response_data = await get_response(UserQuery(user_query=data))
#             asyncio.create_task(send_response(websocket, client_id, response_data))
#     except WebSocketDisconnect:
#         logging.info(f"WebSocket connection from client {client_id} closed.")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Literal
import asyncio

# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UserQuery(BaseModel):
    user_query: str
    files: Optional[List[Dict[Literal["name", "path", "content"], Any]]] = None

app = FastAPI()

# 根据你提供的TaskWeaverApp和Session类实现
from taskweaver.app.app import TaskWeaverApp  # 假设这是正确的导入路径

@app.post("/get_response")
async def get_response(query: UserQuery):
    app_dir = "C:\\code\\TaskWeaver\\project"
    loop = asyncio.get_running_loop()
    
    # 异步执行同步的TaskWeaverApp初始化和获取Session
    app_instance = await loop.run_in_executor(None, lambda: TaskWeaverApp(app_dir=app_dir))
    session = await loop.run_in_executor(None, lambda: app_instance.get_session())
    
    # 异步执行同步的Session.send_message方法
    response_round = await loop.run_in_executor(None, lambda: session.send_message(query.user_query, files=query.files))
    return response_round.to_dict()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    logging.info(f"WebSocket connection from client {client_id} established.")
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(f"Received message from client {client_id}: {data}")
            response_data = await get_response(UserQuery(user_query=data))
            await websocket.send_json(response_data)
    except WebSocketDisconnect:
        logging.info(f"WebSocket connection from client {client_id} closed.")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)