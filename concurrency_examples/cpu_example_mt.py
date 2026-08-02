#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
from threading import Thread, Semaphore
import requests
from common import BASE_URL, WORDS, logger, get_ranking_position, show_ranking


semaphore = Semaphore(1)


def analyze_and_rank_word(word, ranking):
    """
    Get the likes of a word, and add it to the ranking depending on that.
    """
    logger.info("%s: getting word data", word)
    likes = 0
    for _ in range(1_000_000):
        likes += len(word)

    with semaphore:
        logger.info("%s: calculating ranking position for %s likes", word, likes)
        position = get_ranking_position(ranking, likes)

        logger.info("%s: inserting into ranking at position %s", word, position)
        ranking.insert(position, (word, likes))


def main():
    """Analyze all the words and generate the ranking."""
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


main()
