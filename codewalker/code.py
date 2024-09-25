import os
from typing import List, Self
import networkx as nx
import ast

from codewalker.edge_kinds import EdgeKind
from codewalker.exception_base import CodewalkerException
from codewalker.node_kinds import NodeKind


class FileAlreadyAddedToGraph(CodewalkerException):
    def __init__(self, path: str, *args: object) -> None:

        self.path = path

        super().__init__(*args)


class Code:
    def __init__(self, root: str = ""):
        """
        Initialize a Code object.

        Parameters
        ----------
        root : str
            The starting point of the code graph. This is the root of the project for paths.
        """

        self.__g = nx.MultiDiGraph()

        self.__g.add_node(root, root=True, kind=NodeKind.PROJECT)
        self.__root = root

    @property
    def root(self) -> str:
        """
        The root of the project.

        Returns
        -------
        str
            The path to the root of the project.
        """
        return self.__root

    def add_file(self, path: str) -> Self:
        """
        Add a file to the graph.

        Parameters
        ----------
        path : str
            The path to the file to add relative to the root of the project.
        """
        # Normalize input path
        path = os.path.normpath(os.path.join(self.__root, path))

        if path in self.__g:
            raise FileAlreadyAddedToGraph(path)

        # Create a path parts for each subdirectory in the path
        path_parts = []
        for i in range(len(path.split(os.sep))):
            path_parts.append(os.sep.join(path.split(os.sep)[: i + 1]))

        # For each one of those create a directory-like node
        for i, part in enumerate(path_parts):
            if part not in self.__g and i < len(path_parts) - 1:
                self.__g.add_node(
                    part, kind=NodeKind.MODULE_DIR, name=os.path.basename(part)
                )

            if i == len(path_parts) - 1:
                filename = os.path.basename(path)

                # Add the last node for the file
                self.__g.add_node(
                    path,
                    kind=NodeKind.MODULE_FILE,
                    filename=filename,
                    name=os.path.splitext(filename)[0],
                    ext=os.path.splitext(filename)[1],
                    ast=ast.parse(
                        source=(open(path).read()), filename=path, type_comments=True
                    ),
                )

            if i > 0:
                # Add an edge from the previous part to the current part
                self.__g.add_edge(path_parts[i - 1], part, key=EdgeKind.CONTAINS)
                # Add the symmetrical edge
                self.__g.add_edge(
                    part,
                    path_parts[i - 1],
                    key=EdgeKind.PART_OF,
                )

    def resolve_path(self, path: str) -> ast.AST:
        return self.__g.nodes[os.path.normpath(path)]
