import json, threading, websocket, time, asyncio, typing, dispy
import dispy.http.rest

class Gateway:
    def __init__(self, gateway_version: int, token: str, intents: int, activity: dict, status: str, on_ready: typing.Awaitable, on_message: typing.Awaitable):
        # Setting up connecting to Gateway
        self.gateway_version: int = gateway_version
        self.ws = websocket.WebSocket()
        self.intents = intents
        self.activity = activity
        self.status = status
        self.token = token
        self._rest = dispy.http.rest.Rest(token)
        self.on_ready = on_ready
        self.on_message = on_message

        # Connecting to Gateway
        self.ws.connect(f"wss://gateway.discord.gg/?v={self.gateway_version}&encoding=json")

        # Parsing Opcode 10 Hello to Heartbeat Interval
        self.heartbeat_interval = self.get_responce()["d"]["heartbeat_interval"]

        # Setting up Opcode 1 Heartbeat
        self.heartbeat_thread = threading.Thread(target=self.heartbeat)
        self.heartbeat_thread.start()

        # Sending Opcode 2 Identify
        self.send_request({"op": 2, "d": {"token": self.token,
                                          "properties": {"$os": "linux", "$browser": "dispy", "$device": "dispy"},
                                          "presence": {"activities": [activity],
                                                       "status": self.status, "since": 91879201, "afk": False},
                                          "intents": self.intents}})

    def send_request(self, json_data):
        self.ws.send(json.dumps(json_data))

    def get_responce(self):
        responce = self.ws.recv()
        return json.loads(responce)

    def on_ready(self):
        return

    def on_message(self, message: dispy.message.DisMessage):
        return

    def heartbeat(self):
        while True:
            self.send_request({"op": 1, "d": "null"})
            event = self.get_responce()
            print(event)

            if event["t"] == "READY":
                asyncio.run(self.on_ready())

            if event["t"] == "MESSAGE_CREATE":
                asyncio.run(self.on_message(dispy.message.DisMessage(self._rest.fetch(event["d"]["channel_id"], event["d"]["id"]), self._rest)))

            time.sleep(self.heartbeat_interval / 1000)


async def on_ready():
    print("Ready!")


async def on_message(message: dispy.message.DisMessage):
    await message.channel.send("Test)")

g = Gateway(9, "TOKEN", 512, {"name": "test"}, "dnd", on_ready, on_message)