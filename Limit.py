import requests
import random
import sys
from Currency import currency_Pairs
import json
from simplejson import JSONDecodeError


order_Id =[]

order_Type = sys.argv[1]


BASE_URL = "http://141.76.130.35:8989"
headers = {
    'Content-Type' : 'application/json',
    'Authorization' : 'Device-Key=5085afa48he45e1a81c82b455bd0664111, Authorization-Key=pG9xP17k6Bn72QLueh9RSkk3kWls6Sgoq4'
}
buy_sell = random.choice(["buy","sell"])

def token():
    try:
        get_Csrf = requests.get(BASE_URL + "/createorder/{}".format(buy_sell), headers=headers)
        Csrf_res = get_Csrf.json()
        token = Csrf_res['csrf_token']
        return token
    except KeyError:
        sys.exit("Auth-Key changed")


def currency_Matching():
    id = list(currency_Pairs.keys())
    pair_id = random.choice(id)
    value = currency_Pairs.get(pair_id)
    return pair_id,value

pair_id,value = currency_Matching()

def payload(pload = None):
    if pload == 'limit_Payload':
        limit_Payload = {
            "price" : "10.5",
            "quantity" : "10.5",
            "pair_id" : pair_id,
            "order_type" : "limit",
            "csrf_token" : token()
        }
        return limit_Payload
    elif pload == 'market_Payload':
        market_Payload = {
            "quantity" : "11",
            "pair_id" : pair_id,
            "order_type" : "market",
            "csrf_token" :  token()
        }
        return market_Payload
    elif pload == 'stop_limit_Payload':
        stop_limit_Payload = {
            "price" : "11",
            "quantity" : "11",
            "stop_price" : "10",
            "pair_id" : pair_id,
            "order_type" : "stop_limit",
            "csrf_token" : token()

        }
        return stop_limit_Payload
    elif pload == "stop_loss_Payload":
        stop_loss_Payload = {
            "stop_price" : "10",
            "quantity" : "10",
            "pair_id" : pair_id,
            "order_type" : "stop_order",
            "csrf_token" : token()

        }
        return stop_loss_Payload
    else:
        fetch_Orders = {
            "size" : 500
        }
        return fetch_Orders


def order_Fetch():
    checkorder_Res = requests.post(BASE_URL + "/orders", headers=headers, json=payload())
    res_Orders = checkorder_Res.json()
    return res_Orders


def limit_Order():
    try:
        limit_payload = payload("limit_Payload")
        res = requests.post(BASE_URL + "/createorder/{}".format(buy_sell),headers=headers,json=limit_payload)
        type = limit_payload["order_type"]
        res = res.json()
        check_Order(res,type)
    except JSONDecodeError as e:
        print(str(e))
        print("Issue with Limit Order line is - " + str(sys.exc_info()[2].tb_lineno))

def market_Order():
    try:
        market_Payload = payload('market_Payload')
        res = requests.post(BASE_URL + "/createorder/{}".format(buy_sell), headers=headers, json=market_Payload)
        type = market_Payload["order_type"]
        res = res.json()
        check_Order(res,type)
    except JSONDecodeError as e:
        print(str(e))
        print("Issue with Market Order line is - " + str(sys.exc_info()[2].tb_lineno))

# def stop_limit_Order():
#     try:
#         stop_limit_Payload   = payload('stop_limit_Payload')
#         res = requests.post(BASE_URL + "/create_order/{}".format(buy_sell), headers=headers, json=stop_limit_Payload)
#         type = stop_limit_Payload["order_type"]
#         res = res.json()
#         check_Order(res, type)
#     except JSONDecodeError as e:
#         print(str(e))
#         print("Issue with Stop_Limit cOrder line is - " + str(sys.exc_info()[2].tb_lineno))
#
# def stop_loss_Order():
#     try:
#         stop_loss_Payload = payload('stop_loss_Payload')
#         res = requests.post(BASE_URL + "/create_order/{}".format(buy_sell), headers=headers, json=stop_loss_Payload)
#         type = stop_loss_Payload["order_type"]
#         res = res.json()
#         check_Order(res, type)
#     except JSONDecodeError as e:
#         print(str(e))
#         print("Issue with Stop_Loss Order line is - :" + str(sys.exc_info()[2].tb_lineno))

# Checking Order
def check_Order(res,type):

    type = type.upper()
    check_Order = res['order_id']
    res_Orders = order_Fetch()

    for present in res_Orders['payload']:
        order_Id.append(present['order_id'])

    if check_Order in order_Id:
        if buy_sell == "buy":
            print("{} Buy Order for {} Placed Succesfully".format(type,value))
        else:
            print("{} Sell Order for {} Placed Succesfully".format(type,value))
    else:
        print("{} Order Not Placed for {}".format(type,value))

order = order_Type.lower()

if order == "l":
    limit_Order()
elif order == "m":
    market_Order()
# elif order == "stop_limit":
#     stop_limit_Order()
# elif order == "stop_order":
#     stop_loss_Order()







