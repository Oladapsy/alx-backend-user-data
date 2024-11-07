#!/usr/bin/env python3
""" a function called filter_datum that returns the log message obfuscated:"""
from re import sub


def filter_datum(fields, redaction, message, separator) -> str:
    """returns the log message obfuscated:"""
    pattern = '|'.join([f'(?<={field}=)[^{separator}]*' for field in fields])
    return sub(pattern, redaction, message)
