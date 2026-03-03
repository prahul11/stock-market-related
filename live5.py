import websocket
import struct
import json
from urllib.parse import quote

# ============================
# 🔹 UPDATE THESE VALUES
# ============================
API_KEY = "kitefront"
USER_ID = "ZW1419"
ENCTOKEN = "Rxc/RjMkLLIjC/cpB/aBHDg1Ai1aHTXdPy5567Q6s05hjkQLV/Nb3TYwspyVdn6zAjnuo/53BDVMyAr8utIpNE6ol0g9I+ulQ/3XxVA1fq1+Aus6reZ4Aw=="
INSTRUMENT_TOKEN = 121033991   # Example: NIFTY 50 (change to your instrument)
ENCTOKEN = quote(ENCTOKEN, safe='')

# WebSocket URL
ws_url = f"wss://ws.zerodha.com/?api_key={API_KEY}&user_id={USER_ID}&enctoken={ENCTOKEN}&uid=123456&user-agent=kite3-web&version=3.0.0"
headers = [
    "Origin: https://kite.zerodha.com",
    "User-Agent: Mozilla/5.0"
]

def on_open(ws):
    print("Connected")

    # Subscribe in LTP mode (mode = 1)
    subscribe_message = {
        "a": "subscribe",
        "v": [INSTRUMENT_TOKEN]
    }
    ws.send(json.dumps(subscribe_message))

    mode_message = {
        "a": "mode",
        "v": ["ltpc", [INSTRUMENT_TOKEN]]
    }
    ws.send(json.dumps(mode_message))


# def parse_binary(message):
#     """
#     Zerodha binary packet structure:
#     First 2 bytes = number of packets
#     Each packet:
#         4 bytes = instrument_token
#         4 bytes = last_price (int)
#     """

#     packet_count = struct.unpack(">H", message[:2])[0]
#     offset = 2

#     for i in range(packet_count):
#         instrument_token = struct.unpack(">I", message[offset:offset+4])[0]
#         last_price = struct.unpack(">I", message[offset+4:offset+8])[0] / 100

#         print(f"LTP -> {instrument_token}: {last_price}")

#         offset += 8

def parse_binary(message):
    packet_count = struct.unpack(">H", message[:2])[0]
    offset = 2

    for _ in range(packet_count):
        packet_length = struct.unpack(">H", message[offset:offset+2])[0]
        offset += 2

        packet = message[offset:offset+packet_length]

        instrument_token = struct.unpack(">I", packet[0:4])[0]
        last_price = struct.unpack(">I", packet[4:8])[0] / 100.0

        print("Token:", instrument_token, "LTP:", last_price)

        offset += packet_length


def on_message(ws, message):
    if isinstance(message, bytes):
        parse_binary(message)
    else:
        print("Text:", message)


def on_error(ws, error):
    # print("Error:", error)
    pass


def on_close(ws, close_status_code, close_msg):
    print("Closed")


ws = websocket.WebSocketApp(
    ws_url,
        header=headers,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()