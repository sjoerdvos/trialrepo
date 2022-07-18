#!/usr/bin/env python3
# Import system packages
from glob import glob
import json
import numpy as np
import os
import pandas as pd
import pytest
# Import from local
from trialrepo.proc import convert_json_to_dcm_format, jsons_to_excel, str_len


# Define directories
this_dir = os.path.dirname(os.path.realpath(__file__))
test_data_dir = os.path.join(this_dir, "test_data")
test_db_dir = os.path.join(test_data_dir, "db")
xlsx_db_file = os.path.join(test_db_dir, "data.xlsx")


@pytest.mark.parametrize(
    "inp, outcome",
    [("test", 4),
    ("testing", 7)],
)
def test_str_len(inp, outcome):
    """
    Function to test str_len function against saved output

    :Parameters:
      - `inp`:      string
      - `outcome`:  expected length of string
    """

    # Assert correct
    assert str_len(inp) == outcome
# End of function test_str_len()


@pytest.mark.parametrize(
    "fn_test, fn_validate",
    [(os.path.join(test_db_dir, "patient_001.json"), os.path.join(test_db_dir, "validate_001.json")),
    (os.path.join(test_db_dir, "patient_007.json"), os.path.join(test_db_dir, "validate_007.json"))],
)
def test_convert_json_to_dcm_format(fn_test, fn_validate):
    """
    Function to test convert_json_to_dcm_format function against saved output

    :Parameters:
      - `fn_test`:      filename of the dicom worklist query to use
      - `fn_validate`:  filename of response dicom-file to use to validate against
    """

    # Load json as validation
    with open(fn_validate) as tmp:
        json_validate_data = json.load(tmp)

    # Load json for testing
    with open(fn_test) as tmp:
        json_test_data = json.load(tmp)
    # Run function to be tested
    json_test_data = convert_json_to_dcm_format(json_test_data)

    # Commented code to save validated output to file as comparison
    with open(fn_validate, 'w', encoding='utf-8') as f:
        json.dump(json_test_data, f, ensure_ascii=False, indent=4)

    # Assert correct
    assert sorted(json_validate_data.items()) == sorted(json_test_data.items())
# End of function test_convert_json_to_dcm_format()


def test_jsons_to_excel():
    """
    Function to test jsons_to_excel function against saved output
    """

    # Load excel file as validation
    df = pd.read_excel(xlsx_db_file)
    
    # Define testing output filename and remove if it exists
    test_output = os.path.join(test_db_dir, "test_data.xlsx")
    if os.path.exists(test_output):
        os.remove(test_output)
    
    # Run function to be tested
    jsons_to_excel(test_output, test_db_dir)
    
    if os.path.exists(test_output):
        # Load newly generated file
        df_test = pd.read_excel(test_output)
        # Compare datasheets
        outcome = df.compare(df_test)
        # Remove newly created file
        os.remove(test_output)
        # Assert correct
        assert outcome.empty
    else:
        # Wrong
        assert True == False
# End of function test_jsons_to_excel()
