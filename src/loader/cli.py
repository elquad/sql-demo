# arg parsing, pipeline executing
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser(description="TODO description.")
    parser.add_argument("--dsn", help="DSN connection string")
    parser.add_argument("--batch-size", type=int)
    return parser.parse_args()