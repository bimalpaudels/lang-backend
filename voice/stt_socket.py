import asyncio
import json

import websockets
from config import settings

REALTIME_BASE_URL = "wss://api.openai.com/v1/realtime?intent=transcription"
OPENAI_API_KEY = settings.openai_api_key

headers = {
    "Authorization": "Bearer " + OPENAI_API_KEY,
    "OpenAI-Beta": "realtime=v1",
}

session_update = {
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


async def connect_to_realtime():
    async with websockets.connect(REALTIME_BASE_URL, additional_headers=headers) as websocket:
        out = await websocket.recv()
        out = json.loads(out)
        event = out.get('event_id')
        if event:
            await websocket.send(json.dumps(session_update))
        out = await websocket.recv()
        print(json.loads(out))

if __name__ == '__main__':
    asyncio.run(connect_to_realtime())
