import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    rows_before = len(df)

    df = df.drop_duplicates()

    rows_removed = rows_before - len(df)

    logger.debug(f"remove_duplicates: removed {rows_removed} rows")

    return df

def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""

    if axis == "rows":
        before = len(df)
        df = df.dropna(axis=0)
        removed = before - len(df)

    elif axis == "columns":
        before = len(df.columns)
        df = df.dropna(axis=1)
        removed = before - len(df.columns)

    else:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupported axis: {axis}")

    logger.debug(f"handle_missing: removed {removed} {axis}")

    return df


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from specified numeric columns."""

    if method not in ["iqr", "zscore"]:
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")

    for col in columns:
        if col not in df.columns:
            logger.warning(f"Column not found: {col}")
            continue

        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning(f"Column is not numeric: {col}")
            continue

        before = len(df)

        if method == "iqr":
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1

            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr

            df = df[(df[col] >= lower) & (df[col] <= upper)]

        elif method == "zscore":
            mean = df[col].mean()
            std = df[col].std()

            if std == 0:
                continue

            z = (df[col] - mean) / std
            df = df[z.abs() <= threshold]

        removed = before - len(df)
        logger.debug(
            f"{col}: method={method}, threshold={threshold}, "
            f"removed={removed}"
        )

    return df

def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""

    settings = config["processing"]

    if settings["remove_duplicates"]:
        df = remove_duplicates(df)

    if settings["missing"]["enabled"]:
        df = handle_missing(
            df,
            axis=settings["missing"]["axis"]
        )

    if settings["outliers"]["enabled"]:
        df = remove_outliers(
            df,
            columns=settings["outliers"]["columns"],
            method=settings["outliers"]["method"],
            threshold=settings["outliers"]["threshold"]
        )

    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""

    report = {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "columns_removed": len(df_before.columns) - len(df_after.columns)
    }

    return report