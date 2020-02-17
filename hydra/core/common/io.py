import asyncio
import sys
import io


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
        if not char or char == b"\n" or char == b"\0" or char == b"\04":
            break
        data += char
    return data.decode()


async def test_channel():
    buffer = io.BytesIO()
    loop = asyncio.get_event_loop()

    reader = asyncio.StreamReader(loop=loop)
    await loop.connect_read_pipe(
        lambda: asyncio.StreamReaderProtocol(reader, loop=loop),
        buffer
    )

    writer_transport, writer_protocol = await loop.connect_write_pipe(
        lambda: asyncio.streams.FlowControlMixin(loop=loop),
        buffer
    )
    writer = asyncio.streams.StreamWriter(
        writer_transport, writer_protocol, None, loop)

    return reader, writer
