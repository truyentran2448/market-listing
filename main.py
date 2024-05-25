from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Embed

from listing import get_rare_strong_unit
import asyncio

pass_units = [0]*30

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

@client.event
async def on_ready():
    # print(data)
    while True:
        market_listing_channel = client.get_channel(1243864238884257893)
        data, ron_rate = await get_rare_strong_unit()
        print(pass_units)
        for unit in data:
            if unit[5] in pass_units: continue
            embed =  Embed(title= unit[0].capitalize(),
                        url=unit[3])
            embed.set_thumbnail(url=unit[4])
            embed.add_field(name="Price", value=str(unit[2]) + " RON /$" + str(round(ron_rate*unit[2], 3)) + "USD", inline=False)
            embed.add_field(name="Sell Price", value=str(round(unit[2]/0.925, 3)) + " RON /$" + str(round(ron_rate*unit[2]/0.925, 3)) + "USD", inline=False)
            pass_units.pop(0)
            pass_units.append(unit[5])

            await market_listing_channel.send(embed=embed)
        await asyncio.sleep(6)

client.run(TOKEN)
