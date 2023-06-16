import pytest
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Query
from fastapi.testclient import TestClient
from fastapi.responses import HTMLResponse
from typing import List, Optional, Union, Annotated
from pydantic import BaseModel
from spellchecker import SpellChecker
import string
import os
import csv
import io
import re
from main import app

client = TestClient(app)


#remove multiple spaces and unnecessary spaces
def remove_spaces(df: pd.DataFrame = None, column_name: str = None):
    #removing multiple spaces in a string
    df[column_name] = df[column_name].str.replace(r'\s+', ' ', regex = True)
    #removing single space before a full stop
    df[column_name] = df[column_name].str.replace(r'(\s+)\.', '.', regex = True)
    #removing mulltiple spaces at the end of the string
    df[column_name] = df[column_name].str.replace(r'\s+$', '', regex = True)
    return df


#remove null values
def remove_nulls(df: pd.DataFrame = None, column_name: str = None):
    df[column_name].fillna('', inplace=True)
    return df


#replace certain charecters
def replace_chars(
        df: pd.DataFrame = None,
        column_name: str = None,
        chars_to_be_replaced: Annotated[list[str] | None, Query()] = None,
        char_to_replace: str = None
):
    print("df:", df)
    print("column_name:", column_name)
    print("chars_to_be_replaced:", chars_to_be_replaced)
    print("char_to_replace:", char_to_replace)

    for char in chars_to_be_replaced:
        df[column_name] = df[column_name].str.replace(char, char_to_replace)
    return df


#remove certain charecters
def remove_chars(
        df: pd.DataFrame = None,
        column_name: str = None,
        chars_to_be_removed: Annotated[list[str] | None, Query()] = None
):
    for char in chars_to_be_removed:
        df[column_name] = df[column_name].str.replace(char, '')
    return df


#change the text to lowercase
def to_lower(df: pd.DataFrame = None, column_name: str = None):
    df[column_name] = df[column_name].str.lower()
    return df


#change the text to uppercase
def to_upper(df: pd.DataFrame = None, column_name: str = None):
    df[column_name] = df[column_name].str.upper()
    return df


#change the text to title format
def to_title(df: pd.DataFrame = None, column_name: str = None):
    df[column_name] = df[column_name].str.title()
    return df


#remove duplicate rows
def remove_duplicate_rows(df: pd.DataFrame = None):
    df.drop_duplicates(inplace=True)
    return df


#remove duplicate coloumns
def remove_duplicate_columns(df: pd.DataFrame = None):
    df = df.loc[:, ~df.columns.duplicated()]
    return df


#removing empty rows
def remove_empty_rows(df: pd.DataFrame = None):
    df.dropna(axis=0, how='all', inplace=True)
    return df


#removing empty coloumns
def remove_empty_columns(df: pd.DataFrame = None):
    df.dropna(axis=1, how='all', inplace=True)
    return df


#remove negative values
def remove_negative_values(df: pd.DataFrame = None, column_name: str = None):
    df[column_name] = df[column_name].apply(lambda x: x if x >= 0 else None)
    return df


#sort in ascending order of coloumn name
def arrange_column_ascending(df: pd.DataFrame = None, column_name: str = None):
    df[column_name] = df[column_name].sort_values(ascending = True)
    return df


#sort in decending order of coloumn name
def arrange_column_descending(df: pd.DataFrame = None, column_name: str = None):
    df[column_name] = df[column_name].sort_values(ascending = False)
    return df


#remove out of range values
def remove_out_of_range_values(df: pd.DataFrame = None, column_name: str = None, min_value: float = None, max_value: float = None):
    df.loc[(df[column_name] < min_value) | (df[column_name] > max_value), column_name] = None
    return df


#remove punctuations
def remove_punctuation(df: pd.DataFrame = None, column_name: str = None):
    df[column_name] = df[column_name].apply(lambda x: ''.join([c for c in x if c not in string.punctuation]))
    return df


#remove numerical charecters
def remove_numerical_characters(df: pd.DataFrame = None, column_name: str = None):
    df[column_name] = df[column_name].apply(lambda x: ''.join([c for c in x if not c.isdigit()]))
    return df


#remove alphabetical charecters
def remove_alphabetical_characters(df: pd.DataFrame = None, column_name: str = None):
    df[column_name] = df[column_name].apply(lambda x: ''.join([c for c in x if not c.isalpha()]))
    return df


#removing non-alphanumeric characters
def remove_non_alphanumeric(df: pd.DataFrame, column_name: str):
    df[column_name] = df[column_name].apply(lambda x: ''.join(c for c in x if c.isalnum()))
    return df


#remove HTML tags
def remove_html_tags(df: pd.DataFrame, column_name: str):
    df[column_name] = df[column_name].apply(lambda x: re.sub(r'<.*?>', '', x))
    return df


#remove URL's
def remove_urls(df: pd.DataFrame, column_name: str):
    df[column_name] = df[column_name].apply(lambda x: re.sub(r'http\S+|www\S+', '', x))
    return df


#checking pellings and correcting them
def check_spelling(df: pd.DataFrame, column_name: str):
    spell = SpellChecker()
    df[column_name] = df[column_name].apply(lambda x: ' '.join(spell.correction(word) for word in x.split()))
    return df


def replace_long_vowel(df: pd.DataFrame, column_name: str, letter: str):
    replacements = {
        'ा': '',  # 'aa' sound
        'ी': 'ि',  # 'ii' sound
        'ू': 'ु',  # 'uu' sound
        'ॅ': 'े',  # 'ei' sound
        'े': 'े',  # 'ee' sound
        'ै': 'े',  # 'ai' sound
        'ो': 'ो',  # 'oo' sound
        'ौ': 'ो',  # 'au' sound
    }

    if letter in replacements:
        pattern = re.escape(letter)
        df[column_name] = df[column_name].str.replace(pattern, replacements[letter])
    return df


@pytest.fixture
def csv_file():
    csv_data = "id,name\n1,'John Doe'\n2,'Jane Smith'\n3,'Michael Brown'"
    with open("sample_data.csv", "w") as file:
        file.write(csv_data)
    yield "sample_data.csv"
    os.remove("sample_data.csv")


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Home page": "Welcome"}


def test_upload_file(csv_file):
    file_path = csv_file
    payload = {
        "column_name": "name",
        "string_to_replace_with": "REPLACED",
        "to_remove_spaces": True,
        "to_remove_nulls": True,
        "to_replace_chars": ["o", "i"],
        "to_remove_chars": ["J"],
        "to_uppercase": True,
        "to_lowercase": False,
    }
    with open(csv_file, "rb") as test_file:
        response = client.post(
            "/upload/",
            files={"file": test_file},
            data = payload
        )
    print(test_file)
    assert response.json() == {"success": True}
    assert response.status_code == 200


@pytest.mark.skip
def test_remove_spaces():
    sample_data = {
        "id": [1, 2, 3],
        "name": ["William Shakespeare   .", "John   Clinton", "  Mike  "],
    }
    expected_data = {
        "id": [1, 2, 3],
        "name": ["William Shakespeare", "John Clinton", "Mike"],
    }
    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)

    processed_df = remove_spaces(df, "name")
    print(df)
    print(processed_df)
    assert processed_df.equals(expected_df)


def test_remove_nulls():
    sample_data = {
        "id": [1, 2, 3],
        "name": ["John Clinton", None, "Mike"]
    }
    expected_data = {
        "id": [1, 2, 3],
        "name": ["John Clinton", "", "Mike"]
    }
    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)

    processed_df = remove_nulls(df, "name")

    assert processed_df.equals(expected_df)


def test_replace_chars():
    sample_data = {
        "id": [1, 2, 3],
        "name": ["John Clinton", "Michael Jackson", "Mike"]
    }
    chars_to_get_replaced = ["J", "M"]
    string_gets_replaced = "yes"
    expected_data = {
        "id": [1, 2, 3],
        "name": ["yesohn Clinton", "yesichael yesackson", "yesike"]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = replace_chars(df, "name", chars_to_get_replaced, string_gets_replaced)

    assert processed_df.equals(expected_df)


def test_remove_chars():
    sample_data = {
        "id": [1, 2, 3],
        "name": ["John Clinton", "Michael Jackson", "Mike"]
    }
    chars_to_get_replaced = ["i", "o"]
    expected_data = {
        "id": [1, 2, 3],
        "name": ["Jhn Clntn", "Mchael Jacksn", "Mke"]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = remove_chars(df, "name", chars_to_get_replaced)

    assert processed_df.equals(expected_df)


def test_to_upper():
    sample_data = {
        "id": [1, 2, 3],
        "name": ["John Clinton", "Michael Jackson", "Mike"]
    }
    expected_data = {
        "id": [1, 2, 3],
        "name": ["JOHN CLINTON", "MICHAEL JACKSON", "MIKE"]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = to_upper(df, "name")

    assert processed_df.equals(expected_df)


def test_to_lower():
    sample_data = {
        "id": [1, 2, 3],
        "name": ["John Clinton", "Michael Jackson", "Mike"]
    }
    expected_data = {
        "id": [1, 2, 3],
        "name": ["john clinton", "michael jackson", "mike"]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = to_lower(df, "name")

    assert processed_df.equals(expected_df)

def test_to_title():
    sample_data = {
        "id": [1, 2, 3],
        "name": ["john clinton", "michael jackson", "mike"]
    }
    expected_data = {
        "id": [1, 2, 3],
        "name": ["John Clinton", "Michael Jackson", "Mike"]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = to_title(df, "name")

    assert processed_df.equals(expected_df)


def test_remove_duplicate_rows():
    sample_data = {
        "id": [1, 2, 3, 2],
        "name": ["John Doe", "Jane Smith", "Michael Brown", "Jane Smith"]
    }
    expected_data = {
        "id": [1, 2, 3],
        "name": ["John Doe", "Jane Smith", "Michael Brown"]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = remove_duplicate_rows(df)

    assert processed_df.equals(expected_df)


def test_remove_duplicate_columns():
    sample_data = {
        "id": [1, 2, 3],
        "name": ["John Doe", "Jane Smith", "Michael Brown"],
        "name": ["John Doe", "Jane Smith", "Michael Brown"]
    }
    expected_data = {
        "id": [1, 2, 3],
        "name": ["John Doe", "Jane Smith", "Michael Brown"]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = remove_duplicate_columns(df)

    assert processed_df.equals(expected_df)


def test_remove_empty_rows():
    sample_data = {
        "id": [1, None, 3],
        "name": ["John Clinton", None, "Mike"]
    }
    expected_data = {
        "id": [1, 3],
        "name": ["John Clinton", "Mike"]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = remove_empty_rows(df)
    print(df)
    print(processed_df)
    assert processed_df.equals(expected_df)


def test_remove_empty_columns():
    sample_data = {
        "id": [1, 2, 3],
        "name": [None, None, None],
        "age": [20, 30, 40]
    }
    expected_data = {
        "id": [1, 2, 3],
        "age": [20, 30, 40]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = remove_empty_columns(df)
    print(df)
    print(processed_df)
    assert processed_df.equals(expected_df)



def test_remove_negative_values():
    sample_data = {
        "id": [1, 2, 3],
        "value": [10, -5, 0]
    }
    expected_data = {
        "id": [1, 2, 3],
        "value": [10, None, 0]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = remove_negative_values(df, "value")

    assert processed_df.equals(expected_df)


def test_arrange_column_ascending():
    sample_data = {
        "id": [3, 1, 2],
        "name": ["Michael Brown", "John Doe", "Jane Smith"]
    }
    expected_data = {
        "id": [1, 2, 3],
        "name": ["John Doe", "Jane Smith", "Michael Brown"]
    }

    df = pd.DataFrame(sample_data)
    expected_df = pd.DataFrame(expected_data)
    processed_df = arrange_column_ascending(df, "id")
    print(df)
    print(processed_df)
    assert processed_df.equals(expected_df)





if __name__ == "__main__":
    pytest.main()
