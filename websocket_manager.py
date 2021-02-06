import json
import time
from threading import Thread, Lock

from websocket import WebSocketApp


class WebsocketManager:
    _CONNECT_TIMEOUT_S = 5

    def __init__(self):
        self.connect_lock = Lock()
        self.ws = None
        self.msg = None
        self.wst = None

    def _get_url(self):
        return "wss://ftx.com/ws/"

    def _on_message(self, ws, message):
        self.msg = json.loads(message)['data']['last']
        #print(json.loads(message)['data']['last'])

    def _on_open(self, ws):
        print("opened")
        sub_data = {"op": "subscribe", "channel": "ticker", "market": "DOGE-PERP"}
        self.send_json(sub_data)


    def send(self, message):
        print("msg sent")
        self.connect()
        self.ws.send(message)

    def send_json(self, message):
        print("json sent")
        self.send(json.dumps(message))

    def _connect(self):
        assert not self.ws, "ws should be closed before attempting to connect"
        print("_connect")
        self.ws = WebSocketApp(
            self._get_url(),
            on_message=self._wrap_callback(self._on_message),
            #on_close=self._wrap_callback(self._on_close),
            on_error=self._wrap_callback(self._on_error),
            on_open=self._wrap_callback(self._on_open),
        )

        wst = Thread(target=self._run_websocket, args=(self.ws,))
        wst.daemon = True
        wst.start()

        # Wait for socket to connect
        ts = time.time()
        while self.ws and (not self.ws.sock or not self.ws.sock.connected):
            #print(time.time() - ts)
            if time.time() - ts > self._CONNECT_TIMEOUT_S:
                self.ws = None
                return
            time.sleep(0.1)

    def _wrap_callback(self, f):
        def wrapped_f(ws, *args, **kwargs):
            if ws is self.ws:
                try:
                    f(ws, *args, **kwargs)
                except Exception as e:
                    raise Exception(f'Error running websocket callback: {e}')
        return wrapped_f

    def _run_websocket(self, ws):
        print("trying...")
        try:
            print("running forever...")
            ws.run_forever()
        except Exception as e:
            raise Exception(f'Unexpected error while running websocket: {e}')
        finally:
            self._reconnect(ws)

    def _reconnect(self, ws):
        print("trying to reconnect")
        assert ws is not None, '_reconnect should only be called with an existing ws'
        if ws is self.ws:
            self.ws = None
            ws.close()
            self.connect()

    def connect(self):
        print("connect")
        if self.ws:
            return
        with self.connect_lock:
            while not self.ws:
                print("connect - not self.ws")
                self._connect()
                if self.ws:
                    return

    def _on_close(self, ws):
        print("connection closed")
        self._reconnect(ws)

    def _on_error(self, ws, error):
        print("error!")
        self._reconnect(ws)

    def reconnect(self) -> None:
        print("reconnect pt1")
        if self.ws is not None:
            print("reconnect pt2")
            self._reconnect(self.ws)

    def close_connection(self):
        print("closing connection")
        self.ws.close()
        self.ws = None