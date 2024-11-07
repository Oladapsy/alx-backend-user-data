#!/usr/bin/env python3
""" a function called filter_datum that returns the log message obfuscated:"""
import re


def filter_datum(fields, redaction, message, separator) -> str:
    """
         returns the log message obfuscated:
    """
    pattern = '|'.join([f'(?<={field}=)[^{separator}]*' for field in fields])
    return re.sub(pattern, redaction, message)
