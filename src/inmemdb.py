import logging

import psutil

logger = logging.getLogger()


class InMemDB:
    """In-memory database implementation."""

    def __init__(self):
        self.db = {}
        self.value_counts = {}
        self.transaction_stack = []
        self.valid_commands = {
            "SET": {"pattern": "SET name value", "parameter_count": 2},
            "GET": {"pattern": "GET name", "parameter_count": 1},
            "DELETE": {"pattern": "DELETE name", "parameter_count": 1},
            "COUNT": {"pattern": "COUNT value", "parameter_count": 1},
            "BEGIN": {"pattern": "BEGIN", "parameter_count": 0},
            "ROLLBACK": {"pattern": "ROLLBACK", "parameter_count": 0},
            "COMMIT": {"pattern": "COMMIT", "parameter_count": 0},
            "DEBUG": {"pattern": "DEBUG", "parameter_count": 0},
            "END": {"pattern": "END", "parameter_count": 0},
        }

    def _get_memory_usage(self):
        """Get the current memory usage of the process."""
        return psutil.Process().memory_info().rss / 1024**2

    def _debug(self):
        """Log the current state of the database and its related data structures."""
        logger.info(self.db)
        logger.info(self.value_counts)
        logger.info(self.transaction_stack)
        logger.info(f"RAM usage(MB): {self._get_memory_usage()}")

    def _parse_input(self, input):
        """
        Parse the input command and parameters.

        Args:
            input (str): The input command and parameters.

        Returns:
            tuple: The parsed command and the number of parameters.
        """
        parts = input.split(" ")
        command = parts[0].upper()
        parameter_count = len(parts) - 1
        return command, parameter_count

    def _check_if_valid_input(self, input):
        """
        Check if the input command and parameters are valid.

        Args:
            input (str): The input command and parameters.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        command, parameter_count = self._parse_input(input)

        if command not in self.valid_commands:
            logger.error(f"Invalid command: {command}")
            return False

        if parameter_count != self.valid_commands[command]["parameter_count"]:
            logger.error(
                f"Invalid parameter count. Expected pattern: {self.valid_commands[command]['pattern']}"
            )
            return False

        return True

    def run_command(self, input, is_rollback=False):
        """
        Run the given command.

        Args:
            input (str): The command to run.
            is_rollback (bool, optional): Whether the command is part of a rollback. Defaults to False.

        Returns:
            str: The result of the command.
        """
        if not self._check_if_valid_input(input):
            return "INVALID COMMAND"

        input_parts = input.split(" ")
        command = input_parts[0].upper()
        parameters = input_parts[1:]

        command_methods = {
            "END": self._end,
            "SET": self._set,
            "GET": self._get,
            "DELETE": self._delete,
            "COUNT": self._count,
            "BEGIN": self._begin,
            "ROLLBACK": self._rollback,
            "COMMIT": self._commit,
            "DEBUG": self._debug,
        }

        if command in command_methods:
            if command == "SET" or command == "DELETE":
                return command_methods[command](*parameters, is_rollback=is_rollback)
            else:
                return command_methods[command](*parameters)
        else:
            return "INVALID COMMAND"

    def _end(self):
        """End the current session and return an exit message."""
        return "EXIT"

    def _get(self, key):
        """
        Get the value of a given key from the database.

        Args:
            key (str): The key to get the value for.

        Returns:
            str: The value of the key, or "NULL" if the key does not exist.
        """
        return self.db.get(key, "NULL")

    def _update_value_counts(self, value, increment):
        """
        Update the count of a given value in the database.

        Args:
            value (str): The value to update the count for.
            increment (int): The amount to increment the count by.
        """
        self.value_counts[value] = self.value_counts.get(value, 0) + increment

    def _set(self, key, value, is_rollback=False):
        """
        Set the value of a given key in the database.

        If the key already exists and its value is different, the method updates the value, logs the change, and updates the value counts.
        If the key doesn't exist, the method adds the key-value pair, logs the deletion of the key, and updates the count of the new value.

        Args:
            key (str): The key to set the value for.
            value (str): The value to set.
            is_rollback (bool, optional): Whether the operation is part of a rollback. Defaults to False.
        """
        if key in self.db and self.db[key] != value:
            previous_value = self.db[key]
            self.db[key] = value
            self._append_trans_block(f"SET {key} {previous_value}", is_rollback)
            self._update_value_counts(previous_value, -1)
            self._update_value_counts(value, 1)
        elif key not in self.db:
            self._append_trans_block(f"DELETE {key}", is_rollback)
            self.db[key] = value
            self._update_value_counts(value, 1)

    def _count(self, value):
        """
        Count the number of occurrences of a given value in the database.

        Args:
            value (str): The value to count the occurrences of.

        Returns:
            int: The number of occurrences of the value.
        """
        return self.value_counts.get(value, 0)

    def _delete(self, key, is_rollback=False):
        """
        Delete a given key from the database.

        Args:
            key (str): The key to delete.
            is_rollback (bool, optional): Whether the operation is part of a rollback. Defaults to False.
        """
        if key in self.db:
            self._append_trans_block(f"SET {key} {self._get(key)}", is_rollback)
            self._update_value_counts(self._get(key), -1)
            del self.db[key]

    def _in_trans_block(self):
        """
        Check if there is an active transaction block.

        Returns:
            bool: True if there is an active transaction block, False otherwise.
        """
        return bool(self.transaction_stack)

    def _append_trans_block(self, command, is_rollback=False):
        """
        Append a command to the current transaction block.

        Args:
            command (str): The command to append.
            is_rollback (bool, optional): Whether the operation is part of a rollback. Defaults to False.
        """
        if self._in_trans_block() and not is_rollback:
            self.transaction_stack[-1].append(command)

    def _begin(self):
        """Begin a new transaction block."""
        self.transaction_stack.append([])

    def _rollback(self):
        """Rollback the commands in the current transaction block."""

        if not self.transaction_stack:
            return "TRANSACTION NOT FOUND"

        rollback_commands = self.transaction_stack.pop()
        rollback_commands.reverse()
        for command in rollback_commands:
            self.run_command(command, is_rollback=True)

    def _commit(self):
        """Commit the commands in the current transaction block."""
        if self.transaction_stack:
            self.transaction_stack.pop()
