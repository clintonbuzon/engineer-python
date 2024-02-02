# In-Memory Database Implementation

This repo consists of a source code of a Python script which simulates database commands using inmemory database

## Prerequisites
- python 3.9+
- venv

## Getting Started

To get started with the code on this repo, you need to either *clone* or *download* this repo and branch into your machine as shown below;

```bash
git clone https://github.com/affinaquest/engineer-python.git
git checkout JCB-20240202
```

## Dependencies

Before you begin playing with the source code, it is highly recommeneded you do this within a venv.

First add execute permission to shell scripts

```bash
chmod +x *.sh
```

You can install dependencies as shown below;

```bash
./build.sh
```

Running the build shell command would do the following:
- Install requirements.txt
- Run linting via ruff and isort
- Run tests to ensure that code is working as expected

## Running the App

To run this code you need to run `build.sh` at least once to install dependencies on local machine. Once dependencies are installed, then you can execute the following shell file. 

```bash
./run.sh
```

## Performance Requirements

All performance requirements are tested within pytest. More details below.

### Aim for efficient operations

Ensure that GET, SET, DELETE, and COUNT have a runtime of less than O(log n), if not better (where n is the number of items in the database).

Tests done is to capture runtime of each command and compare the same command when the db has a million (1,000,000) records.

The strategy implemented here is I used python dictionary to simulate the db. 
- GET operations are relatively quick since there is no need to scan through the entire dictionary. Just specify the key and you can get the values quickly
- SET operations do multiple things, but mainly does the SET as expected, and keeping track the count of values in a different python dictionary. This way there will be a minimal performance hit on each `SET` but there would be a significant performance boost on `COUNT`
- DELETE operations are relatively quick since we used python dictionary and we just need to specify key to be deleted
- COUNT operations are almost instantanious since each command that modified the db (e.g. `SET` and `DELETE`), count statistics are stored thus we just need to pull this instead of traversing through the entire db

### Memory usage should not double with each transaction

Initial thought on this was to create a copy of the entire DB when creating a transaction and just pointing to that copy when doing a `ROLLBACK` but this does double db size for each transaction.

Strategy implemented here is that we create a transaction stack that holds opposing commands whenever `SET` or `DELETE` operations are done. Whenever we do a `ROLLBACK`, we execute the opposing commands in proper order in order to get back the db from its previous state. 

Implemented code works with multiple nested transactions.

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