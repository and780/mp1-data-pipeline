import argparse
import logging
import sys
from pathlib import Path
from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)



def setup_logging(verbose=False):

    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
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

    parser.add_argument(
    "--config",
    required=True,
    help="Path to the YAML configuration file"
    )
    
    #requires an output file
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Path to the output file"
    )

    #format: default set to csv


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
        f"output={args.output}, config={args.config}"
    )
    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)
        
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # Save a copy of the original data
    df_before = data.copy()

    # Process the data
    try:
        cleaned_data = process_data(data, config)
    except ValueError:
        sys.exit(1)
    # Create and print the cleaning report
    report = create_cleaning_report(df_before, cleaned_data)
    print(report)

    # Log processing results
    logger.info(
        f"Processing complete: {len(df_before)} → {len(cleaned_data)} rows"
    )

    # Save the cleaned data
    cleaned_data.to_csv(args.output, index=False)

    # Log saving results
    logger.info(f"Saved cleaned data to {args.output}")

    

if __name__ == "__main__":
    main()