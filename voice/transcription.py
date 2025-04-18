import asyncio
import base64
import json

import websockets
from config import settings

REALTIME_URL = "wss://api.openai.com/v1/realtime?intent=transcription"


class OpenAIRealTime:
    def __init__(self):
        self.websocket = None
        self.session_update = {
          "type": "transcription_session.update",
          "session": {
            "input_audio_format": "pcm16",
            "input_audio_transcription": {
              "model": "whisper-1",
              "prompt": "",
              "language": "en"
            },
            "turn_detection": {
              "type": "server_vad",
              "threshold": 0.5,
              "prefix_padding_ms": 300,
              "silence_duration_ms": 500,
            },
            "input_audio_noise_reduction": {
              "type": "near_field"
            },
            "include": [
              "item.input_audio_transcription.logprobs",
            ]
          }
        }

    async def connect(self):
        headers = {
            'Authorization': 'Bearer ' + settings.openai_api_key,
            'OpenAI-Beta': "realtime=v1",
        }

        self.websocket = await websockets.connect(REALTIME_URL, additional_headers=headers)

        session = await self.websocket.recv()
        print("Session started", json.loads(session))

        # Session update
        await self.websocket.send(json.dumps(self.session_update))
        updated_session = await self.websocket.recv()
        print("Session updated", json.loads(updated_session))

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()

    async def handle_stream(self, front_ws):

        async def forward_audio():
            while True:
                audio = await front_ws.receive_bytes()
                print(audio)
                base64_audio = base64.b64encode(audio).decode("utf-8")
                await self.websocket.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "audio": base64_audio
                }))

        async def receive_transcription():
            while True:
                event = await self.websocket.recv()
                print(json.loads(event))
                await front_ws.send_text(event)

        await asyncio.gather(forward_audio(), receive_transcription())
