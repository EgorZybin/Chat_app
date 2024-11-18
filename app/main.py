from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from faststream.rabbit.fastapi import RabbitRouter
from app.models import Message, User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = RabbitRouter("amqp://guest:guest@localhost:5672/")
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

active_connections = {}
rooms = {}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    users = {
        "user1": "password1",
        "user2": "password2",
    }

    if token not in users.values():
        raise HTTPException(status_code=401, detail="Invalid token")

    for username, password in users.items():
        if password == token:
            return User(id=username, username=username)

    raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/message/")
async def send_message(message: Message, user: User = Depends(get_current_user)):
    if message.room_id not in rooms or len(rooms[message.room_id]) != 2:
        raise HTTPException(status_code=400, detail="Room does not exist or does not have exactly 2 users")

    await router.publish(message.dict(), routing_key=message.room_id)
    return JSONResponse(content={"detail": "Message sent successfully."})


@router.websocket('/updates/{room_id}')
async def get_updates(websocket: WebSocket, room_id: str):
    await websocket.accept()

    user = User(id=websocket.headers.get("user_id"))

    if room_id not in rooms:
        rooms[room_id] = []

    if len(rooms[room_id]) < 2:
        rooms[room_id].append(user.id)
        active_connections.setdefault(room_id, []).append(websocket)

        try:
            while True:
                data = await websocket.receive_text()
                message = Message(content=data, room_id=room_id, sender_id=user.id)

                await router.publish(message.dict(), routing_key=room_id)

                for connection in active_connections[room_id]:
                    await connection.send_text(data)

        except WebSocketDisconnect:

            active_connections[room_id].remove(websocket)
            rooms[room_id].remove(user.id)
            if not active_connections[room_id]:
                del active_connections[room_id]
                del rooms[room_id]

    else:
        await websocket.close()
