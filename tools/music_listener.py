import asyncio
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager

async def read_music_info():
    manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
    session = manager.get_current_session()
    if session:
        media_info = await session.try_get_media_properties_async()
        return f'"{media_info.title}" por {media_info.artist}'
    return None

def read_music_info_wrapper():
    return asyncio.run(read_music_info())