# Yaml configuration reader and merger
Small reusable solution for yaml config management
- [What it does](#what-it-does)
- [Usage](#usage)


## What it does
- takes the name of given environment variables (expected valid paths to yaml files)
- parses yaml files into yaml-like objects and merges them using given algorithm
- smart recursive merge function which allows replacing and extending the data there

## Usage
```python
from env_config import merge_config_files_from_envvars

CONFIG_FILE_ENVVAR_NAMES = ('GLOBAL_CONFIG', 'LOCAL_CONFIG')

config = merge_config_files_from_envvars(CONFIG_FILE_ENVVAR_NAMES)
```
