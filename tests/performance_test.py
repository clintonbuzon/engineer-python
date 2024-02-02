import pytest

from src.runner import Runner

pytest.n = 1_000_000


class TestPerformanceRequirementsClass:
    def test_efficient_operations_get(self):
        test_runner = Runner()
        test_runner._run_command("SET a foo")
        normal_runtime = test_runner._run_command("GET a", return_runtime=True)

        for i in range(pytest.n):
            test_runner._run_command(f"SET a{i} foo")

        abnormal_runtime = test_runner._run_command("GET a", return_runtime=True)

        assert abnormal_runtime < (normal_runtime * 1000)

    def test_efficient_operations_set(self):
        test_runner = Runner()
        normal_runtime = test_runner._run_command("SET a foo", return_runtime=True)

        for i in range(pytest.n):
            test_runner._run_command(f"SET a{i} foo")

        abnormal_runtime = test_runner._run_command(
            "SET a456789 foo", return_runtime=True
        )

        assert abnormal_runtime < (normal_runtime * 1000)

    def test_efficient_operations_delete(self):
        test_runner = Runner()
        test_runner._run_command("SET a foo")
        normal_runtime = test_runner._run_command("DELETE a", return_runtime=True)

        for i in range(pytest.n):
            test_runner._run_command(f"SET a{i} foo")

        abnormal_runtime = test_runner._run_command(
            "DELETE a456789", return_runtime=True
        )

        assert abnormal_runtime < (normal_runtime * 1000)

    def test_efficient_operations_count(self):
        test_runner = Runner()
        test_runner._run_command("SET a foo")
        normal_runtime = test_runner._run_command("COUNT foo", return_runtime=True)

        for i in range(pytest.n):
            test_runner._run_command(f"SET a{i} foo")

        abnormal_runtime = test_runner._run_command("COUNT foo", return_runtime=True)

        assert abnormal_runtime < (normal_runtime * 1000)

    def test_transaction_memory_usage(self):
        test_runner = Runner()
        for i in range(pytest.n):
            test_runner._run_command(f"SET a{i} foo")

        normal_memory_usage = test_runner._get_memory_usage()

        for i in range(pytest.n):
            test_runner._run_command("BEGIN")

        abnormal_memory_usage = test_runner._get_memory_usage()

        assert abnormal_memory_usage < (normal_memory_usage * 1000)

    def test_invalid_command(self):
        test_runner = Runner()

        output = test_runner._run_command("ASDF")
        assert output == "INVALID COMMAND"

    def test_valid_command_invalid_parameter_count(self):
        test_runner = Runner()

        output = test_runner._run_command(
            "GET a b c d e f g h i j k l m n o p q r s t u v w x y z"
        )
        assert output == "INVALID COMMAND"
