# import requests
# from uuid import uuid4
from flask import Flask, jsonify, request
from flask import send_file
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

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
	# request_params = request.get_json(force=True)
	response = node.tangle.make_transaction(request.form.get('sndr_addr'),
											request.form.get('rcvr_addr'),
											request.form.get('value'))
	return jsonify(response), 201


@app.route('/wallet/balance', methods=['POST'])
def wallet_balance():
	address = request.form.get('address')
	if address in node.wallet.getWalletAddresses():
		return "[+] Wallet balance for address [%s] is: %s " % (address, node.wallet.getbalance(address))
	else:
		return "[-] This node's wallet has no such address: %s" % address


@app.route('/wallet/addresses', methods=['GET'])
def wallet_addresses():
	return "[+] Wallets addresses of this node: " + str(node.wallet.getWalletAddresses().keys())


@app.route('/dag', methods=['GET'])
def show_DAG():
	serializable_format = node.getTangleAsJSONdict()
	node.writeTangleToJSONfile()
	return jsonify(serializable_format), 201

	# return jsonify(node.tangle.DAG), 201
	# problem with the original code was that, DAG dictionary has Transaction Objects as values,
	# and those are not serializable as JSON objects.
	# return jsonify(node.DAG), 201


@app.route('/dag/png', methods=['GET'])
def get_DAG_as_png():
	serializable_format = node.getTangleAsJSONdict()
	node.writeTangleToJSONfile()

	tngl = nx.DiGraph()

	for n in serializable_format:
		print "[+] node: " + n + ", edge: " + str(serializable_format[n]['pre_transactions'])
		for x in serializable_format[n]['pre_transactions']:
			tngl.add_edge(n, x)

	lbls = {}
	for k in tngl.nodes().keys():
		lbls.update({k: k[0:3]})
	pos = nx.spring_layout(tngl)  # positions for all nodes
	nx.draw_networkx_nodes(tngl, pos, node_size=700)
	nx.draw_networkx_labels(tngl, pos, labels=lbls, font_size=8, font_family='sans-serif')
	nx.draw_networkx_edges(tngl, pos, width=2)
	# nx.draw(tngl)
	# plt.show(block=False)

	if "Graph.png" in os.listdir("."):
		print "[+] Deleting Graph.png"
		os.remove("Graph.png")

	plt.axis('off')
	plt.savefig("Graph.png", format="PNG")
	plt.clf()

	return send_file("Graph.png", mimetype='image/png')


@app.route('/hello', methods=['GET'])
def hello():
	print "[+] response: test hello API endpoint"
	return "test hello API endpoint\n"

# print "[+] __name__: " + __name__


if __name__ == '__main__':
	# reload each time a code change happens (ali)
	# app.debug = True

	if not len(sys.argv) >= 1:
		print "[-] ip and port number are required to run this node.\n " \
			  "$ python runNode.py <ip-address> <portnumber>"
		exit
	ip = sys.argv[1]
	port = sys.argv[2]

	print "[+] In main function, starting flask app on host: %s, port: %s" % (ip, port)
	app.run(host=ip, port=int(port))
