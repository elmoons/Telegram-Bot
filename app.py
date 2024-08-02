import asyncio

from handlers import common
from loader import dispatcher, bot


def include_routers():
    routers = [common.router, ]
    for router in routers:
        dispatcher.include_router(router)


async def main():
    include_routers()
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
