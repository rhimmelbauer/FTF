import sys, threading, Queue, time
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

from twisted.python import log
from twisted.internet import reactor
import server

log.startLogging(sys.stdout)

factory = WebSocketServerFactory(u"ws://127.0.0.1:8001")
factory.protocol = server.MyServerProtocol
# factory.setProtocolOptions(maxConnections=2)

q = Queue.Queue()
server.MyServerProtocol.setQueue(q)
q.join()

reactor.listenTCP(8001, factory)
t = threading.Thread(target = reactor.run, kwargs = {'installSignalHandlers':0})
t.start()

def receiveMsg(msg):
    print("Text message received: {0}".format(msg.decode('utf8')))

while True:
    if not q.empty():
    	print 'msg'
        receiveMsg(q.get())
    time.sleep(1)