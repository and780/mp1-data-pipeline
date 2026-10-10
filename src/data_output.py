import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def save_data(df, filepath):
    """Save a DataFrame as a CSV file."""

    path = Path(filepath)

    # Create output directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Save CSV without the index
    df.to_csv(path, index=False)

    # Log the result
    logger.debug(f"Saved {len(df)} rows to {path}")

    return path