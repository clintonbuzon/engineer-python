import logging

import psutil

logger = logging.getLogger()


class InMemDB:
    def __init__(self):
        self.db = {}
        self.value_counts = {}
        self.transaction_stack = []
        self.valid_commands = [
            {"command": "SET", "pattern": "SET name value", "parameter_count": 2},
            {"command": "GET", "pattern": "GET name", "parameter_count": 1},
            {"command": "DELETE", "pattern": "DELETE name", "parameter_count": 1},
            {"command": "COUNT", "pattern": "COUNT value", "parameter_count": 1},
            {"command": "BEGIN", "pattern": "BEGIN", "parameter_count": 0},
            {"command": "ROLLBACK", "pattern": "ROLLBACK", "parameter_count": 0},
            {"command": "COMMIT", "pattern": "COMMIT", "parameter_count": 0},
            {"command": "DEBUG", "pattern": "DEBUG", "parameter_count": 0},
            {"command": "END", "pattern": "END", "parameter_count": 0},
        ]

    def _get_memory_usage(self):
        return psutil.Process().memory_info().rss / 1024**2

    def _debug(self):
        print(self.db)
        print(self.value_counts)
        print(self.transaction_stack)
        print(f"RAM usage(MB): {self._get_memory_usage()}")

    def _get_command_from_input(self, input):
        return input.split(" ")[0].upper()

    def _get_command_parameter_count_from_input(self, input):
        return len(input.split(" ")) - 1

    def _check_if_valid_input(self, input):
        command = self._get_command_from_input(input)
        parameter_count = self._get_command_parameter_count_from_input(input)
        for valid_command in self.valid_commands:
            if command == valid_command["command"]:
                if parameter_count == valid_command["parameter_count"]:
                    return True
                else:
                    logger.error(
                        f"Invalid parameter count. Expected pattern: {valid_command['pattern']}"
                    )
                    return False

        logger.error(f"Invalid command: {command}")
        return False

    def run_command(self, input, is_rollback=False):
        if self._check_if_valid_input(input):
            command = self._get_command_from_input(input)

            if command == "END":
                return "EXIT"
            elif command == "SET":
                key = input.split(" ")[1]
                value = input.split(" ")[2]
                self._set(key, value, is_rollback)
            elif command == "GET":
                key = input.split(" ")[1]
                output = self._get(key)
                return output
            elif command == "DELETE":
                key = input.split(" ")[1]
                self._delete(key, is_rollback)
            elif command == "COUNT":
                value = input.split(" ")[1]
                output = self._count(value)
                return output
            elif command == "BEGIN":
                self._begin()
            elif command == "ROLLBACK":
                self._rollback()
            elif command == "COMMIT":
                self._commit()
            elif command == "DEBUG":
                self._debug()
        else:
            return "INVALID COMMAND"

    def _get(self, key):
        if key in self.db:
            return self.db[key]["current_value"]
        else:
            return "NULL"

    def _update_value_counts(self, value, increment):
        if value in self.value_counts:
            self.value_counts[value] += increment
        else:
            self.value_counts[value] = increment

    def _set(self, key, value, is_rollback=False):
        # If the key already exists and the value is the same, do nothing
        if key in self.db and self.db[key]["current_value"] == value:
            return
        # If the key already exists and the value is different, update the value
        elif key in self.db and self.db[key]["current_value"] != value:
            previous_value = self.db[key]["current_value"]
            self.db[key] = {"current_value": value, "previous_value": previous_value}
            self._append_to_transaction_block(
                f"SET {key} {previous_value}", is_rollback
            )
            self._update_value_counts(previous_value, -1)
            self._update_value_counts(value, 1)
        # If the key does not exist, create a new key
        else:
            self._append_to_transaction_block(f"DELETE {key}", is_rollback)
            self.db[key] = {"current_value": value, "previous_value": None}
            self._update_value_counts(value, 1)

    def _count(self, value):
        count = 0

        # This is slow for large datasets
        # for item in self.db.items():
        #     if item[1]["current_value"] == value:
        #         count += 1
        # return count

        if value in self.value_counts:
            count = self.value_counts[value]
        return count

    def _delete(self, key, is_rollback=False):
        if key in self.db:
            self._append_to_transaction_block(
                f"SET {key} {self._get(key)}", is_rollback
            )
            self._update_value_counts(self.db[key]["current_value"], -1)
            del self.db[key]

    def _check_if_in_transaction_block(self):
        if self.transaction_stack == []:
            return False
        return True

    def _append_to_transaction_block(self, command, is_rollback=False):
        if self._check_if_in_transaction_block() and not is_rollback:
            self.transaction_stack[-1].append(command)

    def _begin(self):
        new_transaction_block = []
        self.transaction_stack.append(new_transaction_block)

    def _rollback(self):
        if self.transaction_stack:
            rollback_commands = self.transaction_stack.pop()
            rollback_commands.reverse()
            for command in rollback_commands:
                self.run_command(command, is_rollback=True)

    def _commit(self):
        if self.transaction_stack:
            self.transaction_stack.pop()
