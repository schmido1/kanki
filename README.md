# Installation

Download poetry package manager
```
pipx install poetry
```

Initialise it in the repository's root directory
```
poetry init
```
Install dependencies
```
poetry install
```
Add environment variable for config directory
```
nano ~/.bashrc
export SERVICE_CONFIG_DIR="directory/to/config/files"
```
Add environment variable for deck directory
```
nano ~/.bashrc
export KANKI_DECK_DIR="directory/to/config/files"


```
# Deployment
```
 poetry run python -m "kanki_server"
```