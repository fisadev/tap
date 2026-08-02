#!/usr/bin/env -S uv run --script
# alternatively, to make it fast with real parallelism, add this to the hasbang: --python pypy
from datetime import datetime
from random import randint
from threading import Thread, Semaphore
from common import BASE_URL, WORDS, logger, get_ranking_position, show_ranking


semaphore = Semaphore(1)


def analyze_and_rank_word(word, ranking):
    """
    Get the likes of a word, and add it to the ranking depending on that.
    """
    logger.info("%s: getting word data", word)
    # silly slow calculation
    likes = 0
    for _ in range(1_000_000):
        likes += randint(1, 10)

    with semaphore:
        logger.info("%s: calculating ranking position for %s likes", word, likes)
        position = get_ranking_position(ranking, likes)

        logger.info("%s: inserting into ranking at position %s", word, position)
        ranking.insert(position, (word, likes))


def main():
    """Analyze all the words and generate the ranking."""
    start = datetime.now()

    ranking = []
    threads = []

    # launch all the threads
    for word in WORDS:
        thread = Thread(target=analyze_and_rank_word, args=(word, ranking))
        threads.append(thread)
        thread.start()

    # wait for all the threads to finish
    for thread in threads:
        thread.join()

    show_ranking(ranking)

    logger.info("Total time for %s cpu heavy tasks, multi threading: %s", len(WORDS), datetime.now() - start)


main()
