import pytest
from pathlib import Path
import yaml

yml_file = Path('.').parent / 'resolvers.yml'

def file_exists():
    return yml_file.exists()

def valid_YML():
    with open(yml_file) as file:
        resolvers = yaml.load(file, Loader=yaml.FullLoader)
        return resolvers

def test_file():
    assert file_exists() == True

def test_YML():
    assert valid_YML()
