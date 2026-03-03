import websocket
import json

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@trade"

def on_open(ws):
    print("Connected to Binance WebSocket")

def on_message(ws, message):
    data = json.loads(message)
    price = data['p']   # trade price
    qty = data['q']     # quantity
    print(f"Price: {price} | Qty: {qty}")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

ws = websocket.WebSocketApp(
    SOCKET,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()