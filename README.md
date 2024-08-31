# Preprocessing-Tool  
This project provides a FastAPI application for processing CSV files with various operations on specified columns. You can upload a CSV file and apply multiple transformations to it using different query parameters.  

## Installation

To set up the project, follow these steps:

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

    - `main` refers to the filename where your FastAPI app is defined.
    - `app` is the instance of FastAPI in the code.

2. Access the API at `http://127.0.0.1:8000` or `http://127.0.0.1:8000/docs` for a better visualization.

3. You can use tools like `curl`, Postman, or the interactive Swagger UI provided by FastAPI to interact with the API.

This is how you will see when you start your server on `http://127.0.0.1:8000/docs`:  

![file_2024-08-31_15 07 22 1](https://github.com/user-attachments/assets/f34e49f2-1a35-49d8-b5fa-206ccc2170dc)  


#### Methods

- `file`: The CSV file to be uploaded (required).
- `column_name`: The column to process (required).
- `string_to_replace_with`: String to replace specified characters (optional).
- `to_remove_spaces`: Flag to remove spaces from the column (optional).
- `to_remove_nulls`: Flag to remove null values from the column (optional).
- `to_replace_chars`: List of characters to replace in the column (optional).
- `to_remove_chars`: List of characters to remove from the column (optional).
- `to_uppercase`: Flag to convert the column to uppercase (optional).
- `to_lowercase`: Flag to convert the column to lowercase (optional).
- `to_title_format`: Flag to convert the column to title format (optional).
- `to_remove_duplicate_rows`: Flag to remove duplicate rows (optional).
- `to_remove_duplicate_columns`: Flag to remove duplicate columns (optional).
- `to_remove_empty_row`: Flag to remove empty rows (optional).
- `to_remove_empty_column`: Flag to remove empty columns (optional).
- `to_remove_negative_values`: Flag to remove negative values (optional).
- `to_arrange_column_ascending`: Flag to sort column values in ascending order (optional).
- `to_arrange_column_descending`: Flag to sort column values in descending order (optional).
- `to_remove_punctuation`: Flag to remove punctuation (optional).
- `to_remove_numerical_characters`: Flag to remove numerical characters (optional).
- `to_remove_alphabetical_characters`: Flag to remove alphabetical characters (optional).
- `to_remove_non_alphanumeric`: Flag to remove non-alphanumeric characters (optional).
- `to_remove_html_tags`: Flag to remove HTML tags (optional).
- `to_remove_urls`: Flag to remove URLs (optional).
- `to_check_spelling`: Flag to check and correct spelling (optional).
- `to_remove_out_of_range_values`: Flag to remove out-of-range values (optional).
- `min_value_of_range`: Minimum value of the range for out-of-range removal (optional).
- `max_value_of_range`: Maximum value of the range for out-of-range removal (optional).
- `to_shorten_hindi_long_vowel`: Flag to shorten long vowels in Hindi (optional).
- `letter_to_shorten`: Letter to shorten its vowel sound (optional).

This is how the methods can be seen on the browser:  
  
![file_2024-08-31_15 16 13 1](https://github.com/user-attachments/assets/5ccf075b-7ceb-4ba5-98fd-46052aaa7c81)  


### Response
  
The final response of methods applied on columns will be as follows:  
  
![file_2024-08-31_15 34 10 2](https://github.com/user-attachments/assets/897908fe-550c-49c1-b0ba-31fd6bf52c57)
