from fastapi import FastAPI, File, UploadFile, Query, Form
from fastapi.responses import HTMLResponse
from typing import List, Optional, Union, Annotated
from pydantic import BaseModel, Field
from spellchecker import SpellChecker
import pandas as pd
import string
import csv
import io
import re


app = FastAPI()


class UploadRequest(BaseModel):
    file: UploadFile = File(description="CSV file to upload")
    column_name: str = Field(str, description="Name of the column to process")
    string_to_replace_with: str = Field(
        None, description="String to replace characters with"
    )
    to_remove_spaces: bool = Field(
        None, description="Flag to remove spaces from the column"
    )
    to_remove_nulls: bool = Field(
        None, description="Flag to remove null values from the column"
    )
    to_replace_chars: List[str] = Field(
        None, description="List of characters to replace in the column"
    )
    to_remove_chars: List[str] = Field(
        None, description="List of characters to remove from the column"
    )
    to_uppercase: bool = Field(
        None, description="Flag to convert the column to uppercase"
    )
    to_lowercase: bool = Field(
        None, description="Flag to convert the column to lowercase"
    )


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



@app.get("/")
def index():
    return {"Home page": "Welcome"}


@app.post("/upload/")
async def upload_file(
    file: UploadFile,
    column_name: str = Form("filename"),
    string_to_replace_with: Annotated[str | None, Query(description = "Enter the string to replace with")] = None,
    to_remove_spaces: Annotated[bool | None, Query(description = "Enter true or false for removing spaces")] = None,
    to_remove_nulls: Annotated[bool | None, Query(description = "Enter true or false for removing nulls")] = None,
    to_replace_chars: Annotated[list | None, Query(description = "Enter the list of charecters to replace")] = None,
    to_remove_chars: Annotated[list | None, Query(description = "Enter the list of charecters to remove")] = None,
    to_uppercase: Annotated[bool | None, Query(description = "Enter true or false for changing to uppercase")] = None,
    to_lowercase: Annotated[bool | None, Query(description = "Enter true or false for changing to lowercase")] = None,
    to_title_format: Annotated[bool | None, Query(description = "Enter true or false for changing to title format")] = None,
    to_remove_duplicate_rows: Annotated[bool | None, Query(description = "Enter true or false for removing duplicate rows in the specified coloumn")] = None,
    to_remove_duplicate_columns: Annotated[bool | None, Query(description = "Enter true or false for removing duplicate coloumns in the specified coloumn")] = None,
    to_remove_empty_row: Annotated[bool | None, Query(description = "Enter true or false for removing empty rows in the specified coloumn")] = None,
    to_remove_empty_column: Annotated[bool | None, Query(description = "Enter true or false for removing empty coloums in the specified coloumn")] = None,
    to_remove_negative_values: Annotated[bool | None, Query(description = "Enter true or false for removing negative values in the specified coloumn")] = None,
    to_arrange_column_ascending: Annotated[bool | None, Query(description = "Enter true or false for arranging elements in ascending order of a specified coloumn")] = None,
    to_arrange_column_descending: Annotated[bool | None, Query(description = "Enter true or false for arranging elements in descending order of a specified coloumn")] = None,
    to_remove_punctuation: Annotated[bool | None, Query(description = "Enter true or false for removing punctuations in the specified coloumn")] = None,
    to_remove_numerical_characters: Annotated[bool | None, Query(description = "Enter true or false for removing numerical charecters in the specified coloumn")] = None,
    to_remove_alphabetical_characters: Annotated[bool | None, Query(description = "Enter true or false for removing alphabetical charecters in the specified coloumn")] = None,
    to_remove_non_alphanumeric: Annotated[bool | None, Query(description = "Enter true or false for removing alpha-numeric charecters in the specified coloumn")] = None,
    to_remove_html_tags: Annotated[bool | None, Query(description = "Enter true or false for removing HTML tags in the specified coloumn")] = None,
    to_remove_urls: Annotated[bool | None, Query(description = "Enter true or false for removing URL's in the specified coloumn")] = None,
    to_check_spelling: Annotated[bool | None, Query(description = "Enter true or false for checking spellings in the specified coloumn")] = None,
    to_remove_out_of_range_values: Annotated[bool | None, Query(description = "Enter true or false for removing out of range values in the specified coloumn")] = None,
    min_value_of_range: Annotated[float | None, Query(description = "Enter the minimum value of the range")] = None,
    max_value_of_range: Annotated[float | None, Query(description = "Enter the maximum value of the range")] = None,
    to_shorten_hindi_long_vowel: Annotated[bool | None, Query(description = "Enter true or false for shortening the long vowels in hindi in the specified coloumn")] = None,
    letter_to_shorten: Annotated[str | None, Query(description = "Enter the letter to shorten its vowel sound")] = None,
    ):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    print(
        file.filename,
        column_name,
        string_to_replace_with,
        to_remove_spaces,
        to_remove_nulls,
        to_replace_chars,
        to_remove_chars,
        to_lowercase,
        to_uppercase
    )

    if to_remove_spaces:  
        df = remove_spaces(df, column_name)
    
    if to_remove_nulls:
        df = remove_nulls(df, column_name)
    
    if to_replace_chars is not None:
        df = replace_chars(df, column_name, to_replace_chars, string_to_replace_with)
    
    if to_remove_chars is not None:
        df = remove_chars(df, column_name, to_remove_chars)
    
    if to_lowercase and not to_uppercase:
        df = to_lower(df, column_name)
    elif to_uppercase and not to_lowercase:
        df = to_upper(df, column_name)

    if to_title_format:
        df = to_title(df, column_name)
    
    if to_remove_duplicate_rows:
        df = remove_duplicate_rows(df)
    
    if to_remove_duplicate_columns:
        df  = remove_duplicate_columns(df)
    
    if to_remove_empty_row:
        df = remove_empty_rows(df)
    
    if to_remove_empty_column:
        df = remove_empty_columns(df)
    
    if to_remove_negative_values:
        df = remove_negative_values(df, column_name)
    
    if to_arrange_column_ascending:
        df = arrange_column_ascending(df, column_name)
    
    if to_arrange_column_descending:
        df = arrange_column_descending(df, column_name)

    if to_remove_punctuation:
        df = remove_punctuation(df, column_name)

    if to_remove_numerical_characters:
        df = remove_numerical_characters(df, column_name)
    
    if to_remove_alphabetical_characters:
        df = remove_alphabetical_characters(df, column_name)
    
    if to_remove_non_alphanumeric:
        df = remove_non_alphanumeric(df, column_name)
    
    if to_remove_html_tags:
        df = remove_html_tags(df, column_name)
    
    if to_remove_urls:
        df = remove_urls(df, column_name)

    if to_check_spelling:
        df = check_spelling(df, column_name)
    
    if to_remove_out_of_range_values:
        df = remove_out_of_range_values(df, column_name, min_value_of_range, max_value_of_range)

    if to_shorten_hindi_long_vowel:
        df = replace_long_vowel(df, column_name, letter_to_shorten)

    value = df.to_dict()
    print(value)
    print(
        type(df),
        type(column_name),
        type(to_replace_chars),
        type(string_to_replace_with),
        type(to_remove_chars)
        )
    
    print(to_replace_chars)
    
    return {"success": True}

    
    '''
    request: UploadRequest):
    file = request.file
    column_name = request.column_name
    string_to_replace_with = request.string_to_replace_with
    to_remove_spaces = request.to_remove_spaces
    to_remove_nulls = request.to_remove_nulls
    to_replace_chars = request.to_replace_chars
    to_remove_chars = request.to_remove_chars
    to_uppercase = request.to_uppercase
    to_lowercase = request.to_lowercase
    '''



#POS Tagging
#text chunking
#unchunking if possible
#removing emojis
#remove rare words to reduce noise and dimentionality