# Description: command line python script to ingest delimited data file and output to a file one or more field names (specified as comma seperated list), with an option to deduplicate to only show unique field values
import pandas as pd
import sys

def get_delimiter(message):
    while True:
        delimiter = input(message)
        if len(delimiter) == 1:
            return delimiter
        else:
            print("Delimiter must be a single character.")

def main():
    
    # Check if correct number of command line arguments provided
    if len(sys.argv) not in [4, 5]:
        print("Usage: python script.py import_filename (field_names seperated by commas) output_filename [--dedup]")
        sys.exit(1)

    # Extract command line arguments
    import_filename = sys.argv[1]
    field_names = sys.argv[2].split(',')
    output_filename = sys.argv[3]
    dedup = "--dedup" in sys.argv

    try:
        # Read import file into pandas dataframe
        import_delimiter = get_delimiter("Enter the delimiter for import file and press enter: ")
        df = pd.read_csv(import_filename, delimiter=import_delimiter, on_bad_lines='skip', dtype=str)
    except FileNotFoundError:
        print("Import file not found.")
        sys.exit(1)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

    # Drop fields not specified in field_names
    df = df[field_names]
    
    # Sort DataFrame by the first field
    df.sort_values(by=field_names[0], inplace=True)

    # Deduplicate dataframe if --dedup option is provided
    if dedup:
        df = df.drop_duplicates()

    try:
        # Prompt user for output delimiter
        output_delimiter = get_delimiter("Enter the delimiter for output file and press enter: ")

        # Write dataframe to output file
        df.to_csv(output_filename, sep=output_delimiter, index=False)
        print(f"Output file '{output_filename}' successfully created.")
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
