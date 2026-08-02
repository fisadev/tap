#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
from common import WORDS, logger, get_ranking_position, show_ranking


def analyze_and_rank_word(word, ranking):
    """
    Get the likes of a word, and add it to the ranking depending on that.
    """
    logger.info("%s: getting word data", word)
    # silly slow calculation
    likes = 0
    for _ in range(1_000_000):
        likes += len(word)

    # no semaphore needed here: there is a single thread of execution, so nothing else
    # can touch the ranking while we are reading and modifying it
    logger.info("%s: calculating ranking position for %s likes", word, likes)
    position = get_ranking_position(ranking, likes)

    logger.info("%s: inserting into ranking at position %s", word, position)
    ranking.insert(position, (word, likes))


def main():
    """Analyze all the words and generate the ranking."""
    ranking = []

    # analyze the words one by one, waiting for each calculation to finish before
    # starting the next one
    for word in WORDS:
        analyze_and_rank_word(word, ranking)

    show_ranking(ranking)


main()
