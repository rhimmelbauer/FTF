from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

import Queue, time

class MyServerProtocol(WebSocketServerProtocol):
    __q = None
    __r = None
    def onConnect(self, request):
        pass

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        MyServerProtocol.__q.put(payload)
        if not MyServerProtocol.__r.empty():
            msg = MyServerProtocol.__r.get()
        else:
            msg = "Ok"
        self.sendMessage(msg,False)

    def onClose(self, wasClean, code, reason):
        pass

    @staticmethod
    def setQueue(q,r):
        MyServerProtocol.__q = q
        MyServerProtocol.__r = r
        print q
