import asyncio
from aiohttp import web

from google.cloud import speech


AUTH_PATH = 'src/integrations/google/secret.json'
CLIENT: speech.SpeechAsyncClient


async def service(app: web.Application):
    global CLIENT
    CLIENT = speech.SpeechAsyncClient.from_service_account_file(AUTH_PATH)
    yield


async def speech2text(
        content: bytes, language_code: str = 'ru-RU', channels: int = 1, rate: int = 16000, encoding: str = 'LINEAR16'
    ) -> str:
    audio = speech.RecognitionAudio(content=content)
    try:
        encoding = speech.RecognitionConfig.AudioEncoding[encoding.upper()]
    except KeyError:
        raise
    
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=rate,
        language_code=language_code,
        audio_channel_count=channels,
        
    )

    response = await CLIENT.recognize(config=config, audio=audio)

    
    return response.results[0].alternatives[0].transcript


if __name__ == '__main__':
    import asyncio
    
    async def main():
        path = 'src/integrations/google/ru16.flac'
        content = open(path, 'rb').read()
        print(await speech2text(content, encoding='flac', language_code='ru'))
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
