from argparse import ArgumentParser, Namespace


def get_args() -> Namespace:
    parser = ArgumentParser(
        prog="loader", description="Loads IOC data (URL, IP addresses) from predefined sources. "
                                   "Run with 'init-db' first to ensure database schema."
    )

    sub = parser.add_subparsers(dest="cmd", required=False)
    init_cmd = sub.add_parser("init-db", help="Create tables & indexes")
    init_cmd.add_argument("--dsn")

    parser.add_argument("--dsn", help="DSN connection string")
    parser.add_argument("--batch-size", type=int, help="Batch size for DB insertion (defaults to 5000)")

    return parser.parse_args()