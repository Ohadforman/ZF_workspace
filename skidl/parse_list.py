import os
import csv


def list_symbols_in_lib(library_path):
    """
    This function lists the symbols in a given KiCad symbol library file (.kicad_sym).
    Args:
        library_path: The file path to the KiCad symbol library.
    Returns:
        A list of symbol names found in the library.
    """
    symbol_names = []
    try:
        with open(library_path, 'r') as file:
            contents = file.read()
            # Split the file content into symbols blocks
            symbols = contents.split('(symbol ')[1:]
            for symbol in symbols:
                # Extract the symbol name, which immediately follows '(symbol ' line
                symbol_name_line = symbol.split('\n')[0]
                symbol_name = symbol_name_line.split(' ')[0].strip()
                symbol_names.append(symbol_name)
    except FileNotFoundError:
        print(f"File not found: {library_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return symbol_names


# Example usage: Adjust the directory to point to where your .kicad_sym files are located.
directory = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols"

# Create a CSV file to store the symbol information
csv_file = "symbols.csv"

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Library Folder", "Symbol"])

    # List all .kicad_sym files in the directory
    lib_files = [f for f in os.listdir(directory) if f.endswith('.kicad_sym')]

    # Write symbol information to CSV file
    for lib_file in lib_files:
        symbols = list_symbols_in_lib(os.path.join(directory, lib_file))
        for symbol in symbols:
            writer.writerow([lib_file, symbol])

print(f"CSV file '{csv_file}' created successfully!")
