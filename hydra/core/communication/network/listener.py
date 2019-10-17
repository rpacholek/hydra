import asyncio

from .device import Device, ConnMaster
from ...config import shadow_copy


def new_client(manager, conn_type, coromanager=None):
    async def new_client_cb(reader, writer):
        node = manager.create_node(Device(reader, writer, conn_type))
        print("New client")
        if coromanager:
            # TODO: Register this coro
            pass
        await node.run()
    return new_client_cb


async def listener(manager, config={}, coromanager=None):
    server_config = shadow_copy(
        config,
        requires=["port"],
        allowed=["host", "timeout"]
    )
    server = await asyncio.start_server(new_client(manager, ConnMaster.SERVER, coromanager), **server_config)
    async with server:
        print("Run server")
        await server.serve_forever()


async def connect(manager, config={}, coromanager=None):
    conn_config = shadow_copy(
        config,
        requires=["host", "port"],
    )
    print(f"Connecting {conn_config}")
    # TODO: host == "discover"
    # TODO: retry, increase timeout
    try:
        conn = await asyncio.wait_for(asyncio.open_connection(**conn_config), config.get("timeout", 10))
        print("Connected")
        await new_client(manager, ConnMaster.CLIENT, coromanager)(*conn)
    except TimeoutError:
        # TODO: Do something usefull
        pass
    except ConnectionRefusedError:
        pass
    print("Finish connection")
