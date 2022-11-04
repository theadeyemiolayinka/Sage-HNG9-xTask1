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
    last_team = ''
    line = 0

    with open(file_name, 'r') as f:
        reader = csv.reader(f)
            
        for row in reader:
            line = line + 1
            if line == 1:
                continue
            else:
                team = row[0]
                series_number = row[1]
                filename = row[2]
                name= row[3]
                description= row[4]
                gender = row[5]
                attributes = row[6]
                uuid = row[7]

                if team == None or team == '':
                    team = last_team 
                else:
                    team = team

                try:
                    dic_attr = dict((x.strip(), y.strip())
                    for x, y in (element.split(':') 
                    for element in attributes.split('; ')))
                except:
                    print('Parse Error for attributes at series number '+ str(series_number))

                fin_attr = [
                    {
                        "trait_type": "gender",
                        "value": gender
                    }
                ]

                for key in dic_attr:
                    fin_attr.append({
                        "trait_type": key,
                        "value": dic_attr[key]
                    })

                # nft template
                nft = {
                    "format": "CHIP-0007",
                    "name": name,
                    "description": description,
                    "minting_tool": team,
                    "sensitive_content": False,
                    "series_number": series_number,
                    "series_total": 420,
                    "attributes": fin_attr,
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
        csv_input['HASH'] = hash_list
    
        csv_input.to_csv('filename.output.csv', index=False)


if __name__ == "__main__":
    # Starting point
    main()
        

        