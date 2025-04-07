import edge_tts
import asyncio

async def synthesize(text: str, filename: str):
    communicate = edge_tts.Communicate(text=text)
    await communicate.save(filename)

text = """Simple example to generate an audio file with randomized
        dynamic voice selection based on attributes such as Gender,
        Language, or Locale."""

# Run the async function properly
# asyncio.run(synthesize(text, filename='test.wav'))


async def stream_tts(text: str):
    communicate = edge_tts.Communicate(text=text)

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]  # This is binary audio data


