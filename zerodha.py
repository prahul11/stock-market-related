import requests

def get_400_days_back_date():
    from datetime import datetime, timedelta

    today = datetime.today()
    forty_days_ago = today - timedelta(days=400)
    return forty_days_ago.strftime('%Y-%m-%d')

def save_to_file(data, filename):
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_historical_data(
    instrument_token,
    from_date,
    to_date,
    user_id,
    enctoken,
    interval="60minute",
    oi=1
):
    """
    Fetch historical data from Zerodha Kite (web session based).

    Args:
        instrument_token (str/int): e.g. 256265
        from_date (str): 'YYYY-MM-DD'
        to_date (str): 'YYYY-MM-DD'
        user_id (str): e.g. 'ZW1419'
        enctoken (str): your enctoken from browser
        interval (str): minute/day/5minute etc
        oi (int): 1 for open interest, 0 otherwise

    Returns:
        dict: JSON response
    """

    url = f"https://kite.zerodha.com/oms/instruments/historical/{instrument_token}/{interval}"

    params = {
        "user_id": user_id,
        "oi": oi,
        "from": from_date,
        "to": to_date
    }

    headers = {
        "authority": "kite.zerodha.com",
        "accept": "*/*",
        "authorization": f"enctoken {enctoken}",
        "referer": "https://kite.zerodha.com/",
        "user-agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
    

if __name__ == "__main__":
    from datetime import datetime, timedelta
    # Example usage
    instrument_token = 256265  # NIFTY 50
    # from_date = "2026-01-01"
    # to_date = "2026-11-31"
    from_date=get_400_days_back_date()
    to_date=datetime.today().strftime('%Y-%m-%d')
    user_id = ""
    enctoken = "=="

    try:
        data = get_historical_data(instrument_token, from_date, to_date, user_id, enctoken)
        print(data)
        save_to_file(data, "historical_data_nifty.json")
    except Exception as e:
        print(e)
