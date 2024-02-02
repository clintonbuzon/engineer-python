from src.runner import Runner


class TestCasesClass:
    def test_case_1_basic_commands(self):
        test_runner = Runner()

        assert test_runner._run_command("GET a") == "NULL"
        assert test_runner._run_command("SET a foo") is None
        assert test_runner._run_command("SET b foo") is None
        assert test_runner._run_command("COUNT foo") == 2
        assert test_runner._run_command("COUNT bar") == 0
        assert test_runner._run_command("DELETE a") is None
        assert test_runner._run_command("COUNT foo") == 1
        assert test_runner._run_command("SET b baz") is None
        assert test_runner._run_command("COUNT foo") == 0
        assert test_runner._run_command("GET b") == "baz"
        assert test_runner._run_command("GET B") == "NULL"
        assert test_runner._run_command("END") == "EXIT"

    def test_case_2_multiple_transactions(self):
        test_runner = Runner()

        assert test_runner._run_command("SET a foo") is None
        assert test_runner._run_command("SET a foo") is None
        assert test_runner._run_command("COUNT foo") == 1
        assert test_runner._run_command("GET a") == "foo"
        assert test_runner._run_command("DELETE a") is None
        assert test_runner._run_command("GET a") == "NULL"
        assert test_runner._run_command("COUNT foo") == 0
        assert test_runner._run_command("END") == "EXIT"

    def test_case_3_nested_transactions(self):
        test_runner = Runner()

        assert test_runner._run_command("BEGIN") is None
        assert test_runner._run_command("SET a foo") is None
        assert test_runner._run_command("GET a") == "foo"
        assert test_runner._run_command("BEGIN") is None
        assert test_runner._run_command("SET a bar") is None
        assert test_runner._run_command("GET a") == "bar"
        assert test_runner._run_command("SET a baz") is None
        assert test_runner._run_command("ROLLBACK") is None
        assert test_runner._run_command("GET a") == "foo"
        assert test_runner._run_command("ROLLBACK") is None
        assert test_runner._run_command("GET a") == "NULL"
        assert test_runner._run_command("END") == "EXIT"

    def test_case_4_nested_transactions_with_commit(self):
        test_runner = Runner()

        assert test_runner._run_command("SET a foo") is None
        assert test_runner._run_command("SET b baz") is None
        assert test_runner._run_command("BEGIN") is None
        assert test_runner._run_command("GET a") == "foo"
        assert test_runner._run_command("SET a bar") is None
        assert test_runner._run_command("COUNT bar") == 1
        assert test_runner._run_command("BEGIN") is None
        assert test_runner._run_command("COUNT bar") == 1
        assert test_runner._run_command("DELETE a") is None
        assert test_runner._run_command("GET a") == "NULL"
        assert test_runner._run_command("COUNT bar") == 0
        assert test_runner._run_command("ROLLBACK") is None
        assert test_runner._run_command("GET a") == "bar"
        assert test_runner._run_command("COUNT bar") == 1
        assert test_runner._run_command("COMMIT") is None
        assert test_runner._run_command("GET a") == "bar"
        assert test_runner._run_command("GET b") == "baz"
        assert test_runner._run_command("END") == "EXIT"
