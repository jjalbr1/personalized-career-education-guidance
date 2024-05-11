import os
import pytest
from unittest.mock import patch
from io import StringIO
from resume_advice import read_file, generate_resume_hash, truncate_resume_content, make_api_request_with_backoff

@pytest.fixture
def docx_file_path(tmp_path):
    file_path = tmp_path / "test.docx"
    with open(file_path, 'w') as file:
        file.write("This is a test document.")
    return str(file_path)

@pytest.fixture
def txt_file_path(tmp_path):
    file_path = tmp_path / "test.txt"
    with open(file_path, 'w') as file:
        file.write("This is a test text file.")
    return str(file_path)

def test_read_file_docx(docx_file_path):
    assert read_file(docx_file_path) == "This is a test document."

def test_read_file_txt(txt_file_path):
    assert read_file(txt_file_path) == "This is a test text file."

def test_read_file_nonexistent():
    with pytest.raises(FileNotFoundError):
        read_file("nonexistent.txt")

def test_generate_resume_hash():
    assert generate_resume_hash("Test") == generate_resume_hash("Test")

def test_truncate_resume_content():
    assert truncate_resume_content("123456789", max_tokens=5) == "12345"

@patch('sys.stdout', new_callable=StringIO)
def test_make_api_request_with_backoff_rate_limit(mock_stdout):
    messages = [{"role": "system", "content": "System message"}, {"role": "user", "content": "User message"}]
    with patch('resume_advice.openai.ChatCompletion.create') as mock_create:
        mock_create.side_effect = [Exception("Rate limit error"), "Response"]
        make_api_request_with_backoff(messages)
    assert "Rate limit error occurred" in mock_stdout.getvalue()

@patch('sys.stdout', new_callable=StringIO)
def test_make_api_request_with_backoff_invalid_request(mock_stdout):
    messages = [{"role": "system", "content": "System message"}, {"role": "user", "content": "User message"}]
    with patch('resume_advice.openai.ChatCompletion.create') as mock_create:
        mock_create.side_effect = [Exception("Invalid request error"), "Response"]
        make_api_request_with_backoff(messages)
    assert "Invalid request error" in mock_stdout.getvalue()

@patch('sys.stdout', new_callable=StringIO)
def test_make_api_request_with_backoff_unexpected_error(mock_stdout):
    messages = [{"role": "system", "content": "System message"}, {"role": "user", "content": "User message"}]
    with patch('resume_advice.openai.ChatCompletion.create') as mock_create:
        mock_create.side_effect = [Exception("Unexpected error"), "Response"]
        make_api_request_with_backoff(messages)
    assert "An unexpected error occurred" in mock_stdout.getvalue()
