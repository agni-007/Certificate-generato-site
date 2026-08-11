# Certificate Generator

A Python script to bulk generate customized PDF certificates from an Excel or CSV file containing names.

## Requirements

Install the required Python libraries using `pip`:

```bash
pip install pandas PyMuPDF openpyxl
```

## Usage

1. Place your PDF template (`template.pdf`) and Excel/CSV file (`v.xlsx` or your data file) in the project directory.
2. Run the script:

```bash
python script.py
```

3. Generated certificates will be saved in the `certificates_output/` folder.
