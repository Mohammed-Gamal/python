"""
    Inspect how different encodings represent text.
    Show byte, hex, and binary forms of text under a given encoding.

    Run interactively:
        python encode_view.py
    
    Run from command line with args:
        python encode_view.py "Hello, 世界" -e utf-16
        python encode_view.py "€"  -e ascii   -r replace
        python encode_view.py "𓀀"  -e utf-16

    Available Encodings:
        ascii
        latin-1
        utf-8
        utf-16
        utf-16-le
        utf-16-be
        utf-32
        utf-32-le
        utf-32-be
        cp1252
        shift_jis
"""

import binascii
import unicodedata
import sys


def bytes_to_hex(b: bytes) -> str:
    """
    Convert bytes to a spaced hex string for readability.
    """
    hx = binascii.hexlify(b).decode("ascii")
    return " ".join(hx[i:i+2] for i in range(0, len(hx), 2))


def bytes_to_binary(b: bytes) -> str:
    """
    Convert bytes to a spaced binary string for readability.
    """
    return " ".join(f"{byte:08b}" for byte in b)


def char_info(ch: str) -> str:
    """
    Get character info: char, code point, and Unicode name.\n
    Example: 'A' U+0041 LATIN CAPITAL LETTER A
    """
    cp = ord(ch)
    try:
        name = unicodedata.name(ch)
    except ValueError:
        name = "<unassigned>"
    return f"'{ch}' U+{cp:04X} {name}"


def encode_text(text: str, encoding: str, errors: str = "strict") -> bytes:
    """
    Encode the entire text string with the specified encoding and error policy.
    """
    return text.encode(encoding, errors=errors)


def per_char_encoding(text: str, encoding: str, errors: str = "strict"):
    """
    Encode each character individually and return a list of tuples with details.\n
    Each tuple contains: (char_info, byte_length, hex_representation, binary_representation)
    """
    rows = []
    for ch in text:
        try:
            eb = ch.encode(encoding, errors=errors)
            rows.append((char_info(ch), len(eb), bytes_to_hex(eb), bytes_to_binary(eb)))
        except UnicodeEncodeError as e:
            rows.append((char_info(ch), 0, "<encode error>", "<encode error>"))
    return rows


def format_table(rows, headers):
    """
    Format a list of rows (tuples) into a simple table string with headers.
    """
    col_widths = [max(len(str(x[i])) for x in ([headers] + rows)) for i in range(len(headers))]
    def fmt_row(r):
        return " | ".join(str(r[i]).ljust(col_widths[i]) for i in range(len(headers)))
    line = "-+-".join("-" * w for w in col_widths)
    return "\n".join([fmt_row(headers), line] + [fmt_row(r) for r in rows])


def list_encodings() -> list[str]:
    """
    Return a list of notable encodings.
    """
    return [
        "ascii", "latin-1", "utf-8",
        "utf-16", "utf-16-le", "utf-16-be",
        "utf-32", "utf-32-le", "utf-32-be",
        "cp1252", "shift_jis"
    ]


def list_errors_policies() -> list[str]:
    """
    Return a list of error handling policies.
    """
    return [
        "strict", "replace", "ignore",
        "backslashreplace", "namereplace"
    ]


def display_options_menu(menu_type: str = "encoding") -> str:
    """
    Display a menu for selecting encoding or error policy.
    Returns the selected option or a default if input is invalid.
    """
    if menu_type == "encoding":
        all_types = list_encodings()
        default = all_types[2]  # utf-8
    elif menu_type == "error":
        all_types = list_errors_policies()
        default = all_types[0]  # strict
    else:
        raise ValueError("Unknown type for options menu.")

    print(f"\nSelect {menu_type} type:")
    for i, t in enumerate(all_types, 1):
        print(f"  {i}. {t}")

    choice = input(f"\nEnter {menu_type} number (default: {default}): ")

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(all_types):
            return all_types[index]

    print(f"Invalid input, defaulting to {default}.\n")
    return default


def print_results(text: str, encoding: str, errors: str):
    """
    Print the encoding results for the given text, encoding, and error policy.
    """
    # Encode once (whole string)
    try:
        out = encode_text(text, encoding, errors=errors)
    except UnicodeEncodeError as e:
        # still print partial info; per-char table will show problem areas
        print(f"Note: some characters failed with 'strict'; showing bytes with '{errors}'.")
        out = text.encode(encoding, errors=errors)

    print(f"\nText: {text}")
    print(f"Encoding: {encoding}  |  Errors policy: {errors}")
    print(f"Byte length: {len(out)}")
    print(f"Bytes (hex): {bytes_to_hex(out) or '<empty>'}")
    print(f"Bytes (bin): {bytes_to_binary(out) or '<empty>'}")

    rows = per_char_encoding(text, encoding, errors=errors)
    print("\nPer-character encoding:")
    print(format_table(rows, headers=("Char / Code Point", "Bytes", "Hex", "Binary")))
    print()


def use_interactive_input():
    """
    Use interactive input to get text, encoding, and error policy.
    """
    text     = input("Enter text to encode (default: 'Hello, 世界'): ") or "Hello, 世界"
    encoding = display_options_menu("encoding")
    errors   = display_options_menu("error")
    print_results(text, encoding, errors)


def use_argparse():
    """
    Use argparse to get command line arguments.
    """
    import argparse
    import textwrap

    parser = argparse.ArgumentParser(
        description="Show byte, hex, and binary forms of text under a given encoding.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(f"""\
            Notable encodings: {list_encodings()}
            Errors policy: {list_errors_policies()}
        """)
    )
    parser.add_argument("text", help="The text to encode (quote it if it has spaces).")
    parser.add_argument("--encoding", "-e", default="utf-8", help="Target encoding (e.g., utf-8, ascii, utf-16-le).")
    parser.add_argument("--errors", "-r", default="strict", help="Encoding error policy.")
    args = parser.parse_args()

    print_results(args.text, args.encoding, args.errors)


def main():
    # If args were provided, run CLI; otherwise fall back to interactive
    if len(sys.argv) > 1:
        use_argparse()
    else:
        use_interactive_input()


if __name__ == "__main__":
    main()
