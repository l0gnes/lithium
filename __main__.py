from bot import Lithium
import asyncio

if __name__ == "__main__" :

    bot = Lithium()
    
    async def main():
        async with bot:
            await bot.bot_start_function()

    asyncio.run(main()) 