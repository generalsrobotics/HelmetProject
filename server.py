from websocket_server import WebsocketServer
from detect import Detector
import threading

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])


# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
	print("Client(%d) said %s" % client['id'],message)


PORT=9001
server = WebsocketServer(PORT,host="0.0.0.0")
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
detector = Detector(server)
detector.startStream()
threading.Thread(target=server.run_forever, daemon = True).start()
detector.startDetecting()

