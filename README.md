This project is a Python pipeline that loads, cleans, and saves data. `pipeline.py` connects all the functions together. `data_loaders.py` loads the files, and `data_validator.py` checks the data for invalid values. `data_processor.py` handles duplicates, missing values, and outliers. `data_output.py` saves the cleaned data, while `utils.py` handles logging and file validation. All modules are in the `src` folder, and `config.yaml` controls how the data is processed.

Example command:
```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output: The pipeline starts with 100 rows, validates 98 rows, and saves 92 cleaned rows to `output/clean.csv`.
