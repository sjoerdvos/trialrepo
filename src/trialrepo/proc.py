#!/usr/bin/env python3
# Import system packages
import argparse
from glob import glob
import json
import numpy as np
import os
import pandas as pd
import sys


def convert_json_to_dcm_format(input):
    """
    Function to convert json dict info to dicom formatting

    :Parameters:
      - `input`:  input json dict

    :Returns:
      - `input`:  modified json dict
    """

    # Patient name (SURNAME^FIRSTNAME)
    pat_name_split = input["PatientName"].split(" ")
    pat_name_dcm = pat_name_split[-1]
    for name in pat_name_split[0:-1]:
        pat_name_dcm = "%s^%s" % (pat_name_dcm, name)
    input["PatientName"] = pat_name_dcm
    # lead clinician name (SURNAME^FIRSTNAME)
    clin_name_split = input["LeadClinicianName"].split(" ")
    clin_name_dcm = clin_name_split[-1]
    for name in clin_name_split[0:-1]:
        clin_name_dcm = "%s^%s" % (clin_name_dcm, name)
    input["LeadClinicianName"] = clin_name_dcm
    # DOB (YYYYMMDD)
    date_split = input["PatientDOB"].split("-")
    date_dcm = "%s%s%s" % (date_split[2], date_split[1], date_split[0])
    input["PatientDOB"] = date_dcm
    # Scan date (YYYYMMDD)
    date_split = input["ScanDate"].split("-")
    date_dcm = "%s%s%s" % (date_split[2], date_split[1], date_split[0])
    input["ScanDate"] = date_dcm
    # Scan time (HHMMSS)
    input["ScanTime"] = "%s%s00" % (input["ScanTime"][0:2], input["ScanTime"][-2:])

    return input
# End of function convert_json_to_dcm_format()


def jsons_to_excel(xlsx_file, db_dir):
    """
    Function to load all the database json-files and save as excel spreadsheet

    :Parameters:
      - `xlsx_file`:  Excel spreadsheet to write to
      - `db_dir`:     database dir with all json-files in it
    """

    # Check database folder exists
    if not os.path.exists(db_dir):
        sys.exit("Database folder (%s) doesn't exist" % db_dir)

    # Load all json-files
    all_jsons = sorted(glob(os.path.join(db_dir, "patient*.json")))
    
    # For each, load and add
    for i,json_file in enumerate(all_jsons):
        # Load json
        with open(json_file) as tmp:
            json_data = json.load(tmp)
            
        # Convert to dicom formatting
        data = convert_json_to_dcm_format(json_data)

        # If first, create dataframe - otherwise just add row
        if i==0:
            df = pd.json_normalize(data)
        else:
            df = df.append(pd.json_normalize(data), ignore_index=True)
            
    # Write to file
    df.to_excel(xlsx_file)
# End of function jsons_to_excel()


def main():
    # Main function for taking command-line input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', dest='in_dir', help="Directory with input jsons to convert to excel", required=True)
    parser.add_argument('--out', dest='out_file', help="Output filename (*.xlsx) to save to", default=None, required=False)
    args = parser.parse_args()

    # Check input folder exists
    if not os.path.exists(args.in_dir):
        sys.exit("Input folder (%s) doesn't exist" % (args.in_dir))

    # Create output filename if not given
    if args.out_file is None:
        out_file = os.path.join(args.in_dir, "data.xlsx")
    else:
        out_file = os.path.abspath(args.out_file)

    # Convert json database to excel
    jsons_to_excel(out_file, args.in_dir)


if __name__ == "__main__":
    main()
