import pytest

from src.runner import Runner


class TestInputClass:
    """
    This class contains unit tests for the Runner class.
    """

    def setup_method(self):
        """
        Setup method that is run before each test. Initializes a Runner instance.
        """
        self.runner = Runner()

    @pytest.mark.parametrize(
        "command", ["ASDF", "GET a b", "SET a", "DELETE", "COUNT", "BEGIN END ROLLBACK"]
    )
    def test_invalid_command(self, command):
        """
        Test to check if the Runner class correctly handles invalid commands.

        Args:
            command (str): The command to test.
        """
        output = self.runner._run_command(command)
        assert output == "INVALID COMMAND"
