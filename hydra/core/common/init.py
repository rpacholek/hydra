import asyncio

from ..config import Config
from ..factory.loader import install_modules, get_this


async def init(Main, config_path=""):
    # Needs to be inside async to initialize queue
    # async enforces to run loop

    config = Config(Main, config_path)
    install_modules([get_this()])
    # CoroManager
    return Main(config)


async def run(main):
    await main.start_coro()
    await main.run()
