from enum import StrEnum


class NodeKind(StrEnum):
    SYMBOL = "symbol"
    MODULE_FILE = "file"
    MODULE_DIR = "dir"
    PROJECT = "project"
