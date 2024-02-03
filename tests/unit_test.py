from src.runner import Runner


class TestCasesClass:
    def setup_method(self):
        """
        Setup method for the test cases. Initializes the Runner object.
        """
        self.test_runner = Runner()

    def test_case_1_basic_commands(self):
        """
        Test case for basic commands like GET, SET, COUNT, DELETE, and END.
        """
        assert self.test_runner._run_command("GET a") == "NULL"
        assert self.test_runner._run_command("SET a foo") is None
        assert self.test_runner._run_command("SET b foo") is None
        assert self.test_runner._run_command("COUNT foo") == 2
        assert self.test_runner._run_command("COUNT bar") == 0
        assert self.test_runner._run_command("DELETE a") is None
        assert self.test_runner._run_command("COUNT foo") == 1
        assert self.test_runner._run_command("SET b baz") is None
        assert self.test_runner._run_command("COUNT foo") == 0
        assert self.test_runner._run_command("GET b") == "baz"
        assert self.test_runner._run_command("GET B") == "NULL"
        assert self.test_runner._run_command("END") == "EXIT"

    def test_case_2_multiple_transactions(self):
        """
        Test case for handling multiple transactions.
        """
        assert self.test_runner._run_command("SET a foo") is None
        assert self.test_runner._run_command("SET a foo") is None
        assert self.test_runner._run_command("COUNT foo") == 1
        assert self.test_runner._run_command("GET a") == "foo"
        assert self.test_runner._run_command("DELETE a") is None
        assert self.test_runner._run_command("GET a") == "NULL"
        assert self.test_runner._run_command("COUNT foo") == 0
        assert self.test_runner._run_command("END") == "EXIT"

    def test_case_3_nested_transactions(self):
        """
        Test case for handling nested transactions.
        """
        assert self.test_runner._run_command("BEGIN") is None
        assert self.test_runner._run_command("SET a foo") is None
        assert self.test_runner._run_command("GET a") == "foo"
        assert self.test_runner._run_command("BEGIN") is None
        assert self.test_runner._run_command("SET a bar") is None
        assert self.test_runner._run_command("GET a") == "bar"
        assert self.test_runner._run_command("SET a baz") is None
        assert self.test_runner._run_command("ROLLBACK") is None
        assert self.test_runner._run_command("GET a") == "foo"
        assert self.test_runner._run_command("ROLLBACK") is None
        assert self.test_runner._run_command("GET a") == "NULL"
        assert self.test_runner._run_command("END") == "EXIT"

    def test_case_4_nested_transactions_with_commit(self):
        """
        Test case for handling nested transactions with commit.
        """
        assert self.test_runner._run_command("SET a foo") is None
        assert self.test_runner._run_command("SET b baz") is None
        assert self.test_runner._run_command("BEGIN") is None
        assert self.test_runner._run_command("GET a") == "foo"
        assert self.test_runner._run_command("SET a bar") is None
        assert self.test_runner._run_command("COUNT bar") == 1
        assert self.test_runner._run_command("BEGIN") is None
        assert self.test_runner._run_command("COUNT bar") == 1
        assert self.test_runner._run_command("DELETE a") is None
        assert self.test_runner._run_command("GET a") == "NULL"
        assert self.test_runner._run_command("COUNT bar") == 0
        assert self.test_runner._run_command("ROLLBACK") is None
        assert self.test_runner._run_command("GET a") == "bar"
        assert self.test_runner._run_command("COUNT bar") == 1
        assert self.test_runner._run_command("COMMIT") is None
        assert self.test_runner._run_command("GET a") == "bar"
        assert self.test_runner._run_command("GET b") == "baz"
        assert self.test_runner._run_command("END") == "EXIT"
