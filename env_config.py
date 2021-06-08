# -*- coding: utf-8 -*-
import logging
import os
import yaml

from pathlib import Path
from typing import Dict, List, Iterable, Union, Optional

from yaml_object_merger import merge


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class ConfigParser:
    """Extracts the data from the configuration file given."""
    def __new__(cls, path) -> Optional[Union[Dict, List]]:
        if not Path(path).exists():
            log.error(f'Given path: {path} does not exist. Skip it and return None')
            return None
        with open(path, 'r') as f:
            contents = f.read()
            return yaml.safe_load(contents)


def merge_config_files_from_envvars(
        envvars: Iterable[str],
        strict: bool = False
) -> Optional[Union[Dict, List]]:
    """
    Merge config files defined in environment variables

    config files must have similar same root structure

    :param envvars: iterable containing the names of environment variables
    which represent a path to yaml configs to be merged
    :param strict: if set to True, throws an exception in case given envvar
    is not defined or contains invalid file path

    :return: merged config as Dict or List

    :raises: EnvironmentError, ValueError
    """

    return merge_yamls(_validated_envvar_values(envvars, strict))


def _validated_envvar_values(envvars: Iterable[str], strict: bool) -> Iterable[str]:
    """
    Yields values of validated envvars

    :param envvars: iterable containing the names of environment variables
    which represent a path to yaml configs to be merged
    :param strict: if set to True, throws an exception in case given envvar
    is not defined or contains invalid file path

    :return: an iterator over validated values of envvars

    :raises: EnvironmentError, ValueError
    """
    for envvar_name in envvars:
        envvar_value = os.getenv(envvar_name)

        if not envvar_value:
            msg = f'Environment variable {envvar_name} is not defined!'
            log.error(msg)
            if strict:
                raise EnvironmentError(msg)
            continue

        if not Path(envvar_value).exists():
            msg = ' '.join((
                f'Path {envvar_value} declared in Environment variable',
                f'{envvar_name} does not exist!'
            ))
            log.error(msg)
            if strict:
                raise ValueError(msg)
            continue

        yield envvar_value


def merge_yamls(file_paths: Iterable[Union[Path, str]], func=None) -> Optional[Union[Dict, List]]:
    """
    Merge yaml files by given file paths

    :param file_paths: iterable containing file paths
    :param func: function used for merging. Must take 2 params and return their merge

    :return: yaml-like object that represents the merge of valid given yaml files
    using merge function
    """
    if func is None:
        func = merge
    main, complement = None, None

    for file_path in file_paths:
        if not main:
            main = ConfigParser(file_path)
            log.info(f'Main config is taken from: {file_path}.')
            continue

        complement = ConfigParser(file_path)
        main = func(main, complement)
    return main
