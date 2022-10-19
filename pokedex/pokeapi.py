import aiohttp
import asyncio
import aiofiles
import json

base_url = "https://pokeapi.co/api/v2/"

# _____________________
# --- Pokemon Stats ---
# ~~~~~~~~~~~~~~~~~~~~~
async def writePokemonStats(pokemon: str):
    await writeResults("stats", await getApiContent("pokemon", pokemon))


async def getPokemonStats(pokemon: str):
    return await getApiContent("pokemon", pokemon)


# _______________________
# --- Pokemon Details ---
# ~~~~~~~~~~~~~~~~~~~~~~~
async def writePokemonDetails(pokemon: str):
    await writeResults("detail", await getApiContent("pokemon-species", pokemon))


async def getPokemonDetails(pokemon: str):
    return await getApiContent("pokemon-species", pokemon)


# ____________________
# --- Move Details ---
# ~~~~~~~~~~~~~~~~~~~~
async def writeMoveDetails(move: str):
    await writeResults(f"moves/{move}", await getApiContent("move", move))


async def getMoveDetails(move: str):
    return await getApiContent("move", move)


# ___HELPERS___
async def writeResults(filename: str, content: dict):
    async with aiofiles.open(f"./output/{filename}.txt", mode="w") as f:
        await f.write(json.dumps(content, indent=4))


async def getApiContent(content_type: str, content: str, base_url: str = base_url):
    url = base_url + content_type + "/" + content
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                resp.raise_for_status()
            except Exception as e:
                print(e)
            return await resp.json()


async def getImage(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                resp.raise_for_status()
            except Exception as e:
                print(e)
            return await resp.read()


# ___INTERFACES___
async def getPokemon(pokemon: str):
    result = await asyncio.gather(
        getPokemonStats(pokemon),
        getPokemonDetails(pokemon),
    )
    image = await asyncio.gather(getImage(result[0]["sprites"]["front_default"]))
    result = (*result, *image)
    return result


async def getPokemonMoveList(pokemon: str):
    result = await asyncio.gather(
        getPokemonStats(pokemon),
    )
    moves = []
    for i in range(len(result[0]["moves"])):
        moves.append(result[0]["moves"][i]["move"]["name"])
    return moves


async def main():
    result = await getPokemonMoveList("voltorb")
    for name in result[:3]:
        await writeMoveDetails(name)


if __name__ == "__main__":
    asyncio.run(main())
