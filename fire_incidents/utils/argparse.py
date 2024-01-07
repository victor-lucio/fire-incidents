import argparse


def get_default_args() -> argparse.Namespace:
    """
    Get arguments from command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run_date", type=str, help="Run date for data", required=True
    )
    args = parser.parse_args()
    return args
