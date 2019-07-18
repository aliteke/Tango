# import requests
# from uuid import uuid4
from flask import Flask, jsonify, request

# custom classes
from lib.node import Node
from lib.util import Util

# Instantiate our Node
# Instantiate Tangle
app = Flask(__name__)
utils = Util()

print "[+] Node object is being created."
node = Node(utils.unique_gen())


@app.route('/node/register_neighbours', methods=['POST'])
def register_new_node():
	print "register_new node"
	response = node.register_neighbours(request.get_json())
	return jsonify(response), 201


@app.route('/transactions/new', methods=['POST'])
def make_transaction():
	request_params = request.get_json()
	response = node.make_transaction(request_params['receiving_addr'], request_params['value'])
	return jsonify(response), 201


@app.route('/wallet/balance', methods=['POST'])
def wallet_balance():
	return "wallets and balances of this node"


@app.route('/dag', methods=['GET'])
def show_DAG():
	print node.DAG
	return jsonify(node.DAG.keys()), 201
	# problem with the original code is that, DAG dictionary has Transaction Objects as values, and those are not
	# serializable as JSON objects. Maybe, find a way to make class Transaction JSON serialiazible (encoding)
	#return jsonify(node.DAG), 201


@app.route('/hello', methods=['GET'])
def hello():
	print "test hello API endpoint"
	return "test hello API endpoint"

# print "[+] __name__: " + __name__


if __name__ == '__main__':
	# reload each time a code change happens (ali)
	# app.debug = True
	print "[+] In main function, starting flask app on port 4001, host 0.0.0.0"
	app.run(host='0.0.0.0', port=4001)