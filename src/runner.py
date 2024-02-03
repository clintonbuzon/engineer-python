import logging
import textwrap
import time

from inmemdb import InMemDB

logger = logging.getLogger()


class Runner:
    """
    Runner class for In-Memory Database simulator.
    """

    def __init__(self):
        """
        Initialize Runner with an instance of InMemDB.
        """
        self.session_db = InMemDB()

    def _calculate_runtime(self, start_time, end_time):
        """
        Calculate and return the runtime of a process.

        Args:
            start_time (float): The start time of the process.
            end_time (float): The end time of the process.

        Returns:
            float: The runtime of the process.
        """
        return end_time - start_time

    def _get_memory_usage(self):
        """
        Get the memory usage of the session database.

        Returns:
            int: The memory usage of the session database.
        """
        return self.session_db._get_memory_usage()

    def _run_command(self, input, return_runtime=False):
        """
        Run a command on the session database and optionally return its runtime.

        Args:
            input (str): The command to run.
            return_runtime (bool, optional): Whether to return the runtime of the command. Defaults to False.

        Returns:
            str: The output of the command.
            float: The runtime of the command, if return_runtime is True.
        """
        start_time = time.time()

        output = self.session_db.run_command(input, return_runtime)
        if output is not None:
            logger.info(output)

        if return_runtime:
            end_time = time.time()
            return self._calculate_runtime(start_time, end_time)

        return output

    def start(self):
        """
        Start the In-Memory Database simulator.
        """
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        print("#################################################################")
        print("#         Welcome to the In-Memory Database simulator!          #")
        print("#################################################################")
        print(
            textwrap.dedent(
                """
            ----------------------- Command list ----------------------------
            SET [name] [value]: Sets the value associated with the given name in the database.
            GET [name]:         Retrieves and prints the value for the specified name. If the name is not in the database, print "NULL."
            DELETE [name]:      Deletes the value associated with the specified name from the database.
            COUNT [value]:      Returns the count of names that have the given value assigned to them. If the value is not assigned to any name, print "0."
            BEGIN:              Starts a new transaction.
            ROLLBACK:           Rolls back the most recent transaction. If there is no transaction to rollback, print "TRANSACTION NOT FOUND."
            COMMIT:             Commits all open transactions and makes changes permanent.
            END:                Exits the database. 
            -----------------------------------------------------------------
        """
            )
        )
        command_output = ""
        while command_output != "EXIT":
            print("-----------------------------------------------------------------")
            input_value = input("Please enter command: ")
            command_output = self._run_command(input_value.strip())


if __name__ == "__main__":
    runner = Runner()
    runner.start()
