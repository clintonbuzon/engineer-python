echo "------------------------------------------"
echo "Installing required python dependencies..."
echo "------------------------------------------"
pip install -r requirements.txt

echo "------------------------------------------"
echo "Linting the code..."
echo "------------------------------------------"
isort .
ruff clean
ruff format
ruff check

echo "------------------------------------------"
echo "Running tests..."
echo "------------------------------------------"
python3 -m pytest -v