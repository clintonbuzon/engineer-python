import random

from src.runner import Runner

N = 1_000_000
MULTIPLIER = 10


class TestPerformanceRequirementsClass:
    """
    This class tests the performance requirements of the Runner class.
    The operations GET, SET, DELETE, and COUNT are expected to run in constant time, O(1),
    which is better than O(log n). This is because these operations are implemented using a Python dictionary,
    which has an average case time complexity of O(1) for these operations.
    """

    def setup_method(self):
        """
        Setup method for the tests. Initializes the Runner and sets a key-value pair.
        """
        self.runner = Runner()
        self.runner._run_command("SET a foo")

    def _setup_db_with_n_records(self):
        """
        Helper method to setup a database with n records for testing.
        """
        for i in range(N):
            self.runner._run_command(f"SET a{i} foo")

    def test_efficient_operations_get(self):
        """
        Tests the GET operation. The runtime of the GET operation should not increase significantly
        even as the number of records increases, demonstrating O(1) performance.
        """
        i_time = self.runner._run_command("GET a", return_runtime=True)
        self._setup_db_with_n_records()
        f_time = self.runner._run_command("GET a", return_runtime=True)
        assert f_time < (i_time * MULTIPLIER)

    def test_efficient_operations_set(self):
        """
        Tests the SET operation. The runtime of the SET operation should not increase significantly
        even as the number of records increases, demonstrating O(1) performance.
        """
        i_time = self.runner._run_command("SET a foo", return_runtime=True)
        self._setup_db_with_n_records()
        random_key = f"a{random.randint(0, N-1)}"
        f_time = self.runner._run_command(f"SET {random_key} foo", return_runtime=True)
        assert f_time < (i_time * MULTIPLIER)

    def test_efficient_operations_delete(self):
        """
        Tests the DELETE operation. The runtime of the DELETE operation should not increase significantly
        even as the number of records increases, demonstrating O(1) performance.
        """
        i_time = self.runner._run_command("DELETE a", return_runtime=True)
        self._setup_db_with_n_records()
        random_key = f"a{random.randint(0, N-1)}"
        f_time = self.runner._run_command(f"DELETE {random_key}", return_runtime=True)
        assert f_time < (i_time * MULTIPLIER)

    def test_efficient_operations_count(self):
        """
        Tests the COUNT operation. The runtime of the COUNT operation should not increase significantly
        even as the number of records increases, demonstrating O(1) performance.
        """
        i_time = self.runner._run_command("COUNT foo", return_runtime=True)
        self._setup_db_with_n_records()
        f_time = self.runner._run_command("COUNT foo", return_runtime=True)
        assert f_time < (i_time * MULTIPLIER)

    def test_transaction_memory_usage(self):
        """
        Tests the memory usage of transactions. The memory usage should not increase significantly
        even as the number of transactions increases, demonstrating O(1) performance. This is to ensure
        that initiating multiple transactions does not lead to a significant increase in memory usage,
        which could potentially degrade the performance of the system.
        """
        self._setup_db_with_n_records()
        i_mem = self.runner._get_memory_usage()
        for _ in range(N):
            self.runner._run_command("BEGIN")
        f_mem = self.runner._get_memory_usage()
        assert f_mem < (i_mem * MULTIPLIER)
