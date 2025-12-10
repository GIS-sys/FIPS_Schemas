 docker run -it -v "$(pwd):/app" -w /app python:3.11 sh -c "pip install psycopg2 tabulate && python analyze.py" > test_analyze.txt

