"""Command-line entry point for SmartEdu Institute analytics."""

import argparse
from pathlib import Path

from smartedu_analytics import analyze, load_data, merge_data, pivot_table, read_json_safe, remove_outliers, save_all


def run(input_path=None, output_dir=".", keep_outliers=False):
    """Run the complete analytics and reporting pipeline."""
    df = load_data(input_path)
    df = analyze(df)
    df = merge_data(df)
    if not keep_outliers:
        df = remove_outliers(df)
    pivot_table(df)
    save_all(df, output_dir)
    read_json_safe(Path(output_dir) / "report.json")
    return df


def main():
    parser = argparse.ArgumentParser(description="Analyze SmartEdu student performance and fees.")
    parser.add_argument("--input", help="Input CSV; omit to use the built-in sample class.")
    parser.add_argument("--output-dir", default=".", help="Directory for generated reports (default: current directory).")
    parser.add_argument("--keep-outliers", action="store_true", help="Keep rows with unusually high or low fees.")
    args = parser.parse_args()
    run(args.input, args.output_dir, args.keep_outliers)


if __name__ == "__main__":
    main()
