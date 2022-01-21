from Connect import XTSConnect
from InteractiveSocketClient import OrderSocket_io

# Interactive API Credentials
API_KEY = "cd454b5dd84a077dbe14592"
API_SECRET = "Rxdud147#sV"
source = "WEBAPI"

# Initialise
xt = XTSConnect(API_KEY, API_SECRET, source)

#hostlookuplogin
res = xt.hostlookup_login()
print(res)

# Login for authorization token
response = xt.interactive_login()

# Store the token and userid
set_interactiveToken = response['result']['token']
set_iuserID = response['result']['userID']
print("Login: ", response)



# Connecting to Interactive socket
soc = OrderSocket_io(set_interactiveToken, set_iuserID,xt.connectionString)


# Callback for connection
def on_connect():
    """Connect from the socket."""
    print('Interactive socket connected successfully!')
    response = xt.place_order(
        exchangeSegment=xt.EXCHANGE_NSECM,
        exchangeInstrumentID=2885,
        productType=xt.PRODUCT_MIS,
        orderType=xt.ORDER_TYPE_MARKET,
        orderSide=xt.TRANSACTION_TYPE_BUY,
        timeInForce=xt.VALIDITY_DAY,
        disclosedQuantity=0,
        orderQuantity=10,
        limitPrice=0,
        stopPrice=0,
        orderUniqueIdentifier="454845")
    print("Place Order: ", response)

# Callback for receiving message
def on_message():
    print('I received a message!')


# Callback for joined event
def on_joined(data):
    print('Interactive socket joined successfully!' + data)


# Callback for error
def on_error(data):
    print('Interactive socket error!' + data)


# Callback for order
def on_order(data):
    print("Order placed!" + data)


# Callback for trade
def on_trade(data):
    print("Trade Received!" + data)


# Callback for position
def on_position(data):
    print("Position Retrieved!" + data)


# Callback for trade conversion event
def on_tradeconversion(data):
    print("Trade Conversion Received!" + data)


# Callback for message logout
def on_messagelogout(data):
    print("User logged out!" + data)


# Callback for disconnection
def on_disconnect():
    print('Interactive Socket disconnected!')


# Assign the callbacks.
soc.on_connect = on_connect
soc.on_message = on_message
soc.on_joined = on_joined
soc.on_error = on_error
soc.on_order = on_order
soc.on_trade = on_trade
soc.on_position = on_position
soc.on_tradeconversion = on_tradeconversion
soc.on_messagelogout = on_messagelogout
soc.on_disconnect = on_disconnect

# Event listener
el = soc.get_emitter()
el.on('connect', on_connect)
el.on('order', on_order)
el.on('trade', on_trade)
el.on('position', on_position)
el.on('tradeConversion', on_tradeconversion)

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
soc.connect()
