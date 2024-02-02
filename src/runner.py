import logging
import textwrap
import time

from inmem_db import InMemDB

logger = logging.getLogger()


class Runner:
    def __init__(self):
        self.session_db = InMemDB()
        self.runner_command = None

    def _calculate_runtime(self, start_time, end_time):
        return end_time - start_time

    def _get_memory_usage(self):
        return self.session_db._get_memory_usage()

    def _run_command(self, input, return_runtime=False):
        start_time = time.time()

        output = self.session_db.run_command(input, return_runtime)
        if output is not None:
            logger.info(output)

        if return_runtime:
            end_time = time.time()
            return self._calculate_runtime(start_time, end_time)

        return output

    def start(self):
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
        runner_command = None
        while runner_command != "EXIT":
            print("-----------------------------------------------------------------")
            input_value = input("Please enter command: ")
            stripped_input = input_value.strip()
            runner_command = self._run_command(stripped_input)


if __name__ == "__main__":
    runner = Runner()
    runner.start()
