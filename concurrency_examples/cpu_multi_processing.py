#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
from datetime import datetime
from random import randint
from multiprocessing import Process, Manager, Semaphore
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

    shared_memory = Manager()
    ranking = shared_memory.list([])
    processes = []

    # launch all the processes
    for word in WORDS:
        process = Process(target=analyze_and_rank_word, args=(word, ranking))
        processes.append(process)
        process.start()

    # wait for all the processes to finish
    for process in processes:
        process.join()

    show_ranking(ranking)

    logger.info("Total time: %s", datetime.now() - start)


main()
