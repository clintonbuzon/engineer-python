# In-Memory Database Implementation

This repository contains the source code for a Python script that simulates database commands using an in-memory database.

## Prerequisites

- Python 3.9+
- venv (Python virtual environment)

## Getting Started

To get started, clone this repository and switch to the appropriate branch:

```bash
git clone https://github.com/clintonbuzon/engineer-python.git
cd engineer-python/
git checkout JCB-20240202
```

## Dependencies

For this project, it's recommended to use a Python virtual environment (venv). This isolates your project dependencies, preventing conflicts with packages in your global Python environment.

First add execute permission to shell scripts:

```bash
chmod +x *.sh
```

You can set up your environment and install the necessary dependencies using the provided build script:

```bash
./build.sh
```

Executing the build script performs the following actions:

- Installs the packages listed in `requirements.txt`
- Lints the code using `ruff` and `isort` to ensure code quality
- Runs unit tests to verify that the code behaves as expected

## Running the App

To run this code you need to run `build.sh` at least once to install dependencies on local machine. Once dependencies are installed, then you can execute the following shell file. 

```bash
./run.sh
```

## Performance Requirements

All performance requirements are tested within pytest. More details below.

### Aim for efficient operations

Operations GET, SET, DELETE, and COUNT should have a runtime of O(log n) or better, where n is the number of items in the database. This is tested by comparing command runtimes with a database of a million records.

The strategy used here is a Python dictionary to simulate the database:
- GET operations are fast as they directly access values using keys.
- SET operations update the database and maintain a separate dictionary for value counts, improving COUNT performance.
- DELETE operations are fast as they directly delete entries using keys.
- COUNT operations are nearly instantaneous as they retrieve stored count statistics instead of scanning the entire database.

### Memory usage should not double with each transaction

Initially, I considered duplicating the entire database for each transaction and reverting to this copy on a `ROLLBACK`. However, this doubles the database size for each transaction.

Instead, I implemented a transaction stack that stores the inverse of `SET` or `DELETE` operations. On a `ROLLBACK`, these inverse commands are executed in the correct order to restore the previous database state.

The current implementation supports multiple nested transactions.

### Pass the first three test cases outlined in the exam document

Passed all test cases as tested under `tests/unit_test.py`

You can run tests by executing the following shell file

```bash
./run_tests.sh
```

### They should accept the correct number of arguments and function correctly.

Added handling for:
- Invalid commands
- Valid commands but improper number of parameters