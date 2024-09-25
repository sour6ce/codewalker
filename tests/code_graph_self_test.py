from ast import Module
import pytest


class TestCodeGraphSelfTest:
    def test_code_graph_basic_self_test(self):
        """Test that the code graph can parse its own test file.

        This test checks that the code graph can parse its own test file.
        It does this by creating a code graph, adding this test file to it,
        resolving the path to this test file, and asserting that the
        resulting node has an "ast" attribute that is a Module.

        """
        import codewalker

        code = codewalker.Code()

        code.add_file("tests/code_graph_self_test.py")

        node = code.resolve_path("tests/code_graph_self_test.py")

        ast = node["ast"]

        assert isinstance(ast, Module)
