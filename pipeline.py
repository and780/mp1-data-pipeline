import argparse
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):

    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S"
    )

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Data Processing Pipeline"
    )

    #requires an input file
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the input file"
    )

    #requires an output file
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path to the output file"
    )

    #format: default set to csv
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format"
    )

    #show more details log when type -v
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file."""

    #check if is a file
    if Path(filepath).is_file():
        logger.info(f"Input file validated: {filepath}")
        return True
        #if not, give an error, return false
    else:
        logger.error(f"Input file not found: {filepath}")
        return False


def main():
    """Main pipeline function."""
    args = parse_arguments()

    setup_logging(args.verbose)

    logger.debug(
        f"Arguments parsed: input={args.input}, "
        f"output={args.output}, format={args.format}"
    )
    if not validate_input(args.input):
        sys.exit(1)

if __name__ == "__main__":
    main()