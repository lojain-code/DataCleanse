"""Helper functions of DataCleanse (given by the instructor - read them and be ready to explain them)."""
import pandas as pd


def quality_report(raw, cleaned):
    """Simple data quality numbers before and after cleaning."""
    return {
        "rows_before": len(raw),
        "rows_after": len(cleaned),
        "rows_removed": len(raw) - len(cleaned),
        "missing_before": int(raw.isna().sum().sum()),
        "missing_after": int(cleaned.isna().sum().sum()),
        "duplicates_before": int(raw.duplicated().sum()),
    }
