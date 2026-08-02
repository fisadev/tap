import logging
import os


BASE_URL = "http://localhost:5000/get_likes/"
WORDS = [
    "asado",
    "icecream",
    "swords",
    "movies",
    "dogs",
    "cats",
    "BTS",
    "sandro",
    "python",
    "java",
]

repeat = int(os.environ.get("REPEAT", 0))
if repeat:
    extra_words = []
    for i in range(1, repeat):
        extra_words.extend([f"{word}_{i + 1}" for word in WORDS])
    WORDS.extend(extra_words)


def get_ranking_position(ranking, likes):
    """
    Get the position in the ranking for a given number of likes.
    The ranking is a list of tuples (word, likes) sorted in descending order by likes.
    """
    for position, (_, other_likes) in enumerate(ranking):
        if likes > other_likes:
            return position
    return len(ranking)


def show_ranking(ranking):
    """
    Show the ranking in a human-readable format.
    Also, check if the ranking is sorted correctly and print an error message if not.
    """
    print("\nRanking:")
    last_likes = None
    for position, (word, likes) in enumerate(ranking):
        if last_likes is not None and likes > last_likes:
            error = "<-- ERROR: ranking is not sorted correctly"
        else:
            error = ""
        last_likes = likes

        print(f"{position + 1}. {word}: {likes} likes {error}")


logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger("example")
logging.getLogger("httpx").setLevel(logging.ERROR)  # disabling httpx verbose logs
