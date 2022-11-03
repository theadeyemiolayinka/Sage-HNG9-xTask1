"""
Copyright 2022 @theadeyemiolayinka
- Collect team values from CSV input
- Generate a CHIP-007 JSON file for each row
- Create sha256 encryption for each json file
- Append the sha256 hash to each line in a new csv (filename.output.csv)
"""

import os

import argparse
import csv 
import hashlib
import json
import pandas as pd


# constants
FILETYPE_INVALID = "Error: Whoops. Invalid file format. %s must be a .csv file."
PATH_INVALID = "Error: Whoops. Invalid file/path name. Path %s does not exist."

def check_file(file_name):
    if not valid_filetype(file_name):
        print(PATH_INVALID%(file_name))
        print("If it does, it sure doesn't look like a CSV file. Please try again")
        quit()
    return

def valid_filetype(file_name):
    # Validate file type
    return file_name.endswith('.csv')

def valid_path(path):
    # Create or/and check path
    if not os.path.isdir(path):
        os.mkdir(path)
    return os.path.exists(path)


def main():
    # Initialize helper
    helper = argparse.ArgumentParser(description='CSV Processor')
    # Defining argument(s)
    helper.add_argument("file", type=str, nargs=1, help="Read CSV input => jsonify => hash => return output",
    metavar="file_name", default=None)

    args = helper.parse_args()

    if args.file != None:
        check_file(args.file[0])
        file_name = args.file[0]

    hash_list = []

    with open(file_name, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            series_number = row[0]
            filename = row[1]
            name= row[2]
            description= row[3]
            gender = row[4]
            attributes = row[5]
            uuid = row[6]

            # nft template
            nft = {
                "format": "CHIP-0007",
                "name": name,
                "description": description,
                "minting_tool": "HNG Minting Tool",
                "sensitive_content": False,
                "series_number": series_number,
                "series_total": 420,
                "attributes": [
                    {
                        "trait_type": "gender",
                        "value": gender
                    }
                ],
                "collection": {
                    "name": "Zuri NFT tickets for free lunch",
                    "id": uuid,
                    "attributes": [
                        {
                            "type": "description",
                            "value": "Rewards for accomplishments during HNGi9"
                        }
                    ]
                },
            }

            # Create JSON Object
            with open("output/{}.json".format(filename), 'w') as outfile:
                json.dump(nft, outfile, indent=4, separators=(", ", ": "))
                outfile.close()

            if filename == "Filename":
                pass
            else:
                with open("output/{}.json".format(filename), "rb") as f:
                    bytes = f.read()
                    readable_hash = hashlib.sha256(bytes).hexdigest()
                    hash_list.append(readable_hash)
                    f.close()
        
        # Add Hash to filename.output.csv
        csv_input = pd.read_csv(file_name)
        csv_input['Hash'] = hash_list
    
        csv_input.to_csv('filename.output.csv', index=False)


if __name__ == "__main__":
    # Starting point
    main()
        

        