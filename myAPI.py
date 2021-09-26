'''
The app keeps a data structure of messages with the information if the message is a palindrom. Each message is assigned an id when created. The id is used to access the message for reading, overwriting and deleting.

Accessing the data for reading or changing is done using http requests. json format is used for creating or updating messages.

Messages are kept in a dictionary, with message id as key. The app manages a list of available ids for quick access of possible ids in case of many messages.
'''

import flask
from flask import Flask, request, jsonify, json

api = flask.Flask(__name__)
api.config["DEBUG"] = True

msgs = {}
availables = {"num":0, "list":[]}

def isPalindromFunc(msg):
  i = 0
  j = len(msg)-1
  
  while i < j:
    if msg[i] != msg[j]:
      return False
    i += 1
    j -= 1
  return True

# List all messages
@api.route('/list', methods=['GET'])
def get_list():
  return jsonify(msgs)

# Creating a new message. Getting the assigned id in the response.
@api.route('/new_message', methods=['POST'])
def create_msg():
  msg_data = request.get_json()
  if 'msg' not in msg_data:
    return jsonify("problem with POST request"), 400

  msg = msg_data['msg']
  d = {"msg": msg, "isPalindrom": isPalindromFunc(msg)}
  k = 0
  if availables["num"] > 0:
    k = availables["list"][availables["num"]-1]
    availables["num"] -= 1
  else:
    k = len(msgs)
  msgs[k] = d
  return jsonify({"success": True, "id":k}), 201

# Accessing a message for reading, changing or deleting. 
@api.route('/message/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def handle_msg(id):
  if id not in msgs:
    return jsonify("message not found"), 404

  if request.method == 'DELETE':
    msgs.pop(id)
    if availables["num"] == len(availables["list"]):
      availables["list"] += [id]
    else:
      availables["list"][availables["num"]] = id
    availables["num"] += 1
    return jsonify({}), 204
  elif request.method == 'PATCH':
    msg = request.get_json()['msg']
    msgs[id]["msg"] = msg
    msgs[id]["isPalindrom"] = isPalindromFunc(msg)
    return jsonify({}), 204

  return jsonify(msgs[id])



if '__main__' == '__main__':
    api.run() 
