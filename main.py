import asyncio, requests, pygame, uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from datetime import datetime

app = FastAPI()

config = {
    "instrument_token": "256265",
    "enctoken": "vN7iqdm4Msy332UJVHnneKGC+F8RvwiXgPcKOBoc74AZkMGJ+dDUk5BKiDJbKY+q2Mavhr/exd/ZiJEfzLTPwCEeRPkn6r/fy0ZelzR06CFh7EtZ4dbc3A==",
    "target_price": 22450.0,
    "range": 5.0,
    "current_ltp": 0.0,
    "alert_active": False,
    "last_update": "Never"
}

pygame.mixer.init()

async def fetch_loop():
    while True:
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"https://kite.zerodha.com/oms/instruments/historical/{config['instrument_token']}/minute?from={today}&to={today}"
        headers = {"Authorization": f"enctoken {config['enctoken']}", "User-Agent": "Mozilla/5.0"}
        
        try:
            r = requests.get(url, headers=headers, timeout=5).json()
            if r.get('status') == 'success' and r['data']['candles']:
                ltp = r['data']['candles'][-1][4]
                config["current_ltp"] = ltp
                config["last_update"] = datetime.now().strftime("%H:%M:%S")

                # Range check
                in_range = (config["target_price"] - config["range"]) <= ltp <= (config["target_price"] + config["range"])
                config["alert_active"] = in_range

                if in_range:
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.load("faaa.mp3")
                        pygame.mixer.music.play()
        except: pass
        await asyncio.sleep(30) # 20 seconds loop

@app.on_event("startup")
async def start_background():
    asyncio.create_task(fetch_loop())

@app.get("/")
async def ui(): return FileResponse('index.html')

@app.get("/api/status")
def get_status(): return config

@app.get("/update")
def update_params(target: float = None, range_val: float = None, instrument_token: str = None, enctoken: str = None):
    """
    URL Example: http://127.0.0.1:8000/update?target=22500&range_val=10
    """
    if target is not None: config["target_price"] = target
    if range_val is not None: config["range"] = range_val
    if instrument_token is not None: config["instrument_token"] = instrument_token
    if enctoken is not None: config["enctoken"] = enctoken
    
    return {"status": "Updated", "new_config": config}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)