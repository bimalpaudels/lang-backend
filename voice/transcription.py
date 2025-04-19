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

                message = await front_ws.receive()

                if message.get('type') == 'websocket.disconnect':
                    print("Frontend disconnected")
                    break

                if isinstance(message.get('bytes'), bytes):
                    chunk = message['bytes']
                    base64_audio = base64.b64encode(chunk).decode("utf-8")
                    await self.websocket.send(json.dumps({
                        "type": "input_audio_buffer.append",
                        "audio": base64_audio
                    }))

        async def receive_transcription():
            try:
                while True:
                    message = await self.websocket.recv()
                    msg = json.loads(message)
                    print(msg)
                    if msg['type'] == "conversation.item.input_audio_transcription.completed":
                        print(msg['transcript'])
                    await front_ws.send_text(message)
            except Exception as e:
                print("Is it crashing", e)

        try:
            await asyncio.gather(
                forward_audio(),
                receive_transcription(),
                return_exceptions=True
            )
        except Exception as e:
            print(f"Stream ended suddenly: {e}")
        finally:
            # Clean up if needed
            await front_ws.close()
