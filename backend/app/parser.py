"""Name extraction from spreadsheets, CSV files and plain text."""

from __future__ import annotations

import io
import logging

import pandas as pd

from .utils import (
    AppError,
    MSG_BAD_SHEET,
    MSG_EMPTY_SHEET,
    clean_name,
    dedupe_names,
    enforce_name_limit,
)

logger = logging.getLogger(__name__)

NAME_COLUMN = "name"


def parse_manual_names(text: str) -> list[str]:
    """One name per line."""
    names = [clean_name(line) for line in (text or "").splitlines()]
    return enforce_name_limit([name for name in names if name])


def _read_csv(data: bytes) -> pd.DataFrame:
    last_error: Exception | None = None
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return pd.read_csv(io.BytesIO(data), encoding=encoding, dtype=str)
        except (UnicodeDecodeError, pd.errors.ParserError) as error:
            last_error = error
    if last_error is not None:
        logger.info("CSV read failed for all encodings: %s", last_error)
    return pd.DataFrame()


def _read_xlsx(data: bytes) -> pd.DataFrame:
    return pd.read_excel(io.BytesIO(data), dtype=str, engine="openpyxl")


def _read_any(data: bytes, extension: str) -> pd.DataFrame:
    try:
        if extension == ".csv":
            if _looks_like_tab_separated(data):
                frame = pd.read_csv(
                    io.BytesIO(data), sep="\t", dtype=str, encoding="utf-8-sig"
                )
            else:
                frame = _read_csv(data)
        else:
            frame = _read_xlsx(data)
    except AppError:
        raise
    except Exception as error:  # noqa: BLE001 - surfaced as a friendly message
        logger.warning("Could not read uploaded spreadsheet: %s", error)
        raise AppError(MSG_BAD_SHEET) from None
    if isinstance(frame, pd.DataFrame) and not frame.empty and frame.columns.empty:
        raise AppError(MSG_BAD_SHEET)
    return frame if isinstance(frame, pd.DataFrame) else pd.DataFrame()


def _looks_like_tab_separated(data: bytes) -> bool:
    """Tab separated files are common exports of Indian school software."""
    head = data[:4096]
    if b"\t" not in head:
        return False
    try:
        text = head.decode("utf-8-sig", errors="ignore")
    except Exception:  # noqa: BLE001
        return False
    first_line = text.splitlines()[0] if text.splitlines() else ""
    return first_line.count("\t") >= 1 and first_line.count(",") == 0


def _select_name_column(columns: list[object]) -> object:
    """Prefer a case-insensitive 'name' column, otherwise the first column."""
    for column in columns:
        if str(column).strip().strip("﻿").lower() == NAME_COLUMN:
            return column
    for column in columns:
        cleaned = str(column).strip().strip("﻿").lower()
        if cleaned in {"name", "names", "full name", "fullname", "student name"}:
            return column
    return columns[0]


def _column_values(frame: pd.DataFrame, column: object) -> list[str]:
    values = frame[column].tolist()
    non_empty = [value for value in values if clean_name(value)]
    if len(values) == 1 and len(non_empty) == 1:
        # A single cell holding a pasted block of names, one per line.
        text = str(values[0])
        if "\n" in text or "\r" in text:
            return [clean_name(line) for line in text.splitlines()]
    return [clean_name(value) for value in values]


def extract_names_from_file(data: bytes, extension: str) -> list[str]:
    """Return the cleaned, de-duplicated names contained in a file."""
    frame = _read_any(data, extension)

    if frame.empty or len(frame.columns) == 0:
        raise AppError(MSG_EMPTY_SHEET)

    column = _select_name_column(list(frame.columns))
    names = [name for name in _column_values(frame, column) if name]

    # A header row is the only way a 'name' column can be off by one.
    if names and names[0].casefold() == NAME_COLUMN:
        names = names[1:]

    names = dedupe_names(names)
    if not names:
        raise AppError(MSG_EMPTY_SHEET)
    return enforce_name_limit(names)
