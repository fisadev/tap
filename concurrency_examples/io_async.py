#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["aiohttp"]
# ///
from datetime import datetime
from asyncio import gather, run
import aiohttp
from common import BASE_URL, WORDS, logger, get_ranking_position, show_ranking


async def analyze_and_rank_word(word, ranking):
    """
    Get the likes of a word, and add it to the ranking depending on that.
    """
    logger.info("%s: getting word data", word)
    try:
        async with aiohttp.ClientSession() as client:
            response = await client.get(BASE_URL + word, timeout=5)
            word_data = await response.json()
            likes = word_data["likes"]
    except:
        likes = -1

    # no semaphore needed here: there are no awaits between reading the ranking and
    # modifying it, so no other coroutine can run in the middle of these two steps
    logger.info("%s: calculating ranking position for %s likes", word, likes)
    position = get_ranking_position(ranking, likes)

    logger.info("%s: inserting into ranking at position %s", word, position)
    ranking.insert(position, (word, likes))


async def main():
    """Analyze all the words and generate the ranking."""
    start = datetime.now()

    ranking = []

    # launch all the coroutines and wait for them to finish
    coros = [analyze_and_rank_word(word, ranking) for word in WORDS]
    await gather(*coros)

    show_ranking(ranking)

    logger.info("Total time for %s io heavy tasks, async: %s", len(WORDS), datetime.now() - start)


run(main())
