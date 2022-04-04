# Overview

Simple scripts for using PyGithub to work with the GitHub API

## Usage

Create a virtual environment
`python3 -m venv ./venv`

Activate it
`. ./venv/bin/activate`

Install dependencies
`pip3 install -r requirements.txt`

Run your script
`./setup-collab-repos.py -t engineering`

## GitHub Token

To use the GitHub API you will need to setup a Personal Access Token. By default scripts will read this out of the environment variable `GITHUB_ACCESS_TOKEN` or you can pass it via command line argument `--token`.

