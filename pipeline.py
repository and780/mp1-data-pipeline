import argparse
import logging
import sys
from pathlib import Path
from src.data_loaders import load_data
from src.data_processor import process_data, create_cleaning_report
from src.utils import setup_logging, validate_input

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)
logger = logging.getLogger(__name__)





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

    validation = config.get("validation", {})

    required_columns = validation.get("required_columns", [])
    numeric_columns = validation.get("numeric_columns", [])

    rows_before = len(data)

    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)

    logger.info(f"Validation complete: {rows_before} -> {len(data)} rows")

    #save a copy of the original data
    df_before = data.copy()

    try:
        cleaned_data = process_data(data, config)
    except ValueError:
        sys.exit(1)
    report = create_cleaning_report(df_before, cleaned_data)

    logger.info(
        f"Processing complete: {len(df_before)} → {len(cleaned_data)} rows"
    )

    output_path = save_data(cleaned_data, args.output)

    logger.info(f"Saved cleaned data to {output_path}")

    print("\nCleaning report:")
    print(report)

    

if __name__ == "__main__":
    main()