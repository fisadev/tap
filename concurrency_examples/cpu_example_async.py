#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
from asyncio import gather, run, sleep
from common import BASE_URL, WORDS, logger, get_ranking_position, show_ranking


async def analyze_and_rank_word(word, ranking):
    """
    Get the likes of a word, and add it to the ranking depending on that.
    """
    logger.info("%s: getting word data", word)
    # silly slow calculation
    likes = 0
    for _ in range(1000000):
        await sleep(0)  # yield control to the event loop
        likes += len(word)

    # no semaphore needed here: there are no awaits between reading the ranking and
    # modifying it, so no other coroutine can run in the middle of these two steps
    logger.info("%s: calculating ranking position for %s likes", word, likes)
    position = get_ranking_position(ranking, likes)

    logger.info("%s: inserting into ranking at position %s", word, position)
    ranking.insert(position, (word, likes))


async def main():
    """Analyze all the words and generate the ranking."""
    ranking = []

    # launch all the coroutines and wait for them to finish
    coros = [analyze_and_rank_word(word, ranking) for word in WORDS]
    await gather(*coros)

    show_ranking(ranking)


run(main())
