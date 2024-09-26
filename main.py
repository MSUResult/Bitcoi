import requests
import time

# Replace with your CoinMarketCap API key and bot token
API_KEY = 'd8f80797-8c2e-4987-8045-2667be84e10d'
BASE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
BOT_TOKEN = '7653100991:AAE1NvC5J8kS--ZKgAMqnbh_9Fk3LVcHh7c'
CHANNEL_ID = '@bit45670'  # Replace with your channel username

URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

def botSendText(botMessage, chat_id):
    send_text = f'{URL}sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={botMessage}'
    
    try:
        response = requests.get(send_text)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

def fetch_prices():
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    parameters = {
        'symbol': 'BTC,ETH',
        'convert': 'USD'
    }
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=parameters)
        response.raise_for_status()
        data = response.json()
        
        btc_price = data['data']['BTC']['quote']['USD']['price']
        eth_price = data['data']['ETH']['quote']['USD']['price']
        
        return btc_price, eth_price
    except requests.exceptions.RequestException as e:
        print(f"Error fetching prices: {e}")
        return None, None

def send_crypto_prices(chat_id):
    btc_price, eth_price = fetch_prices()
    if btc_price and eth_price:
        btc_message = f'Bitcoin price: ${btc_price:.2f}'
        eth_message = f'Ethereum price: ${eth_price:.2f}'
        
        botSendText(btc_message, chat_id)
        botSendText(eth_message, chat_id)
    else:
        botSendText("Couldn't retrieve prices. Try again later.", chat_id)

if __name__ == '__main__':
    while True:
        # Send price updates to the channel every 60 seconds
        send_crypto_prices(CHANNEL_ID)
        time.sleep(60)  # Wait 1 minute before sending prices again
