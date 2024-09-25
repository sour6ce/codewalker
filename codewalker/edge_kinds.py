from enum import StrEnum


class EdgeKind(StrEnum):
    PART_OF = "in"
    CONTAINS = "contains"
    IMPORTS = "imports"
    IMPORTED_BY = "imported"
    USES = "uses"
    USED_BY = "used"
