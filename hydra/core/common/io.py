import asyncio
import sys

async def input(prefix=""):
    print(prefix, sep='', end='', flush=True)

    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader(loop=loop)
    await loop.connect_read_pipe(
            lambda: asyncio.StreamReaderProtocol(reader, loop=loop), 
            sys.stdin
        )
    data = bytes()
    while True:
        char = await reader.read(1)
        if char == b"\n" or char == b"\0":
            break
        data += char
    return data.decode()
    
