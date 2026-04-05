from fastapi import FastAPI
import jwt
import time

app = FastAPI()

API_KEY = "APIPePbKoLtV4Zq"
API_SECRET = "LkWSaLRGIk21ng144dcVQM7uO2rsFq2qXrDBBXeahbD"

@app.get("/token")
def get_token(identity: str = "user"):
    payload = {
        "iss": API_KEY,
        "sub": identity,
        "exp": int(time.time()) + 3600,
        "video": {
            "room": "test-room",
            "roomJoin": True,
            "canPublish": True,
            "canSubscribe": True
        }
    }

    token = jwt.encode(payload, API_SECRET, algorithm="HS256")
    return {"token": token}