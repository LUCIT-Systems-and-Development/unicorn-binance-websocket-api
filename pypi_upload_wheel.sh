#!/usr/bin/env bash
# ~/.pypirc
#[distutils]
#index-servers=pypi
#[pypi]
#repository = https://upload.pypi.org/legacy/
#username =unicorn_data_analysis

python -m twine upload dist/*
