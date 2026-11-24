# SmartEdu Institute

A small Python project for analyzing student marks, fee records, batches, and feedback. It uses a built-in sample class by default, or can process a compatible CSV file supplied on the command line.

## Features

- Calculates each student's average and grade.
- Reports top performers, students at risk, grade counts, and city-level summaries.
- Derives performance, scholarship eligibility, normalized feedback, and fee status.
- Displays a city and batch pivot table.
- Writes processed data as CSV, a summary as text, and class statistics as JSON.
- Includes reusable `Person`, `Student`, `ScholarshipStudent`, `Batch`, and `ClassReport` models.

## Requirements

- Python 3.9 or newer
- pandas 2.x

Install the dependency:

```bash
python -m pip install -r requirements.txt
```

## Run with the included sample data

```bash
python main.py
```

Generated files are written to the current directory:

- `smartedu_data.csv` — processed student records
- `report.json` — class totals, average score, at-risk count, and grade distribution
- `summary.txt` — names included in the processed report

## Use your own CSV

```bash
python main.py --input students.csv --output-dir output
```

The CSV must contain these columns (column names are case-sensitive):

`Roll`, `Name`, `City`, `Batch`, `Maths`, `Science`, `English`, `CS`, `Fees`, `Feedback`

The four subject columns and `Fees` should contain numeric values. By default, records with fee values outside the interquartile range (1.5 × IQR) are excluded before reports are saved. Keep every row with:

```bash
python main.py --input students.csv --keep-outliers
```

## Project files

```text
main.py                Command-line application and pipeline
smartedu_analytics.py  Data loading, analysis, and report generation
smartedu_classes.py    Object-oriented student and class models
smartedu_data.csv      Example/generated processed data
report.json            Example/generated report
summary.txt            Example/generated student-name summary
```

## Notes

Fee status is demonstrated with a small in-code lookup for rolls 101–103; unmatched students have a blank status. Scholarship eligibility is calculated from the average and fee amount in `smartedu_analytics.py` and can be adjusted for your institution's policy.
# SmartEdu-Institute
