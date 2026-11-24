import pandas as pd
import json
from pathlib import Path

def load_data(path=None):
    """Load a CSV file, or return the bundled demonstration class."""
    if path is not None:
        df = pd.read_csv(path)
        required = {'Roll', 'Name', 'City', 'Batch', 'Maths', 'Science', 'English', 'CS', 'Fees', 'Feedback'}
        missing = required.difference(df.columns)
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
        df['Average'] = df[['Maths', 'Science', 'English', 'CS']].mean(axis=1).round(2)
        return df

    data = {
        'Roll': [101,102,103,104,105,106,107,108,109,110,111,112],
        'Name': ['Aarav','Priya','Rohan','Sneha','Kiran','Divya',
                 'Eshan','Farida','Gaurav','Hema','Isha','Jai'],
        'City': ['Mumbai','Delhi','Mumbai','Chennai','Delhi','Mumbai',
                 'Chennai','Delhi','Mumbai','Chennai','Delhi','Mumbai'],
        'Batch': ['Morning','Evening','Morning','Evening','Morning','Evening',
                  'Morning','Evening','Morning','Evening','Morning','Evening'],
        'Maths': [88,45,72,91,60,55,83,38,77,95,62,80],
        'Science': [79,50,68,88,55,49,85,42,73,90,58,76],
        'English': [92,60,74,85,70,65,78,55,80,88,70,84],
        'CS': [95,40,80,92,65,58,90,35,82,96,66,88],
        'Fees': [15000,12000,18000,9000,11000,14000,
                 95000,10000,16000,13000,12500,17000],
        'Feedback': ['Great class!','needs improvement','Very Good',
                     'Excellent!','Average','Best faculty',
                     'GOOD quality','Not satisfied!!!','Worth it!',
                     'Brilliant','Okay','Superb']
    }

    df = pd.DataFrame(data)
    df['Average'] = df[['Maths','Science','English','CS']].mean(axis=1).round(2)
    return df


def analyze(df):
    df = df.copy()

    print("\n===== DATA HEAD =====")
    print(df.head())

    print("\n===== DATA INFO =====")
    df.info()

    print("\n===== DATA DESCRIPTION =====")
    print(df.describe())

    print("\n===== MISSING VALUES =====")
    print(df.isnull().sum())

    print("\n===== TOP STUDENTS =====")
    print(df[df['Average'] >= 85][['Name','Average']])

    print("\n===== AT RISK STUDENTS =====")
    print(df[df['Average'] < 55][['Name','Average']])

    # Grade
    df['Grade'] = pd.cut(df['Average'],
                         bins=[0,54,69,84,100],
                         labels=['F','C','B','A'])

    print("\nGrade Count:\n", df['Grade'].value_counts())
    print("\nGrade %:\n", df['Grade'].value_counts(normalize=True))

    # Crosstab
    print("\nCrosstab (City vs Grade):\n")
    print(pd.crosstab(df['City'], df['Grade']))

    # Groupby
    city_summary = df.groupby('City').agg(
        avg_marks=('Average','mean'),
        top_score=('Average','max'),
        student_count=('Roll','count')
    )
    print("\nCity Summary:\n", city_summary)

    # Transform
    df['City_Avg'] = df.groupby('City')['Average'].transform('mean')

    # Map
    df['City_Type'] = df['City'].map({
        'Mumbai':'Metro',
        'Delhi':'Metro',
        'Chennai':'Tier-2'
    })

    # Apply
    df['Performance'] = df['Average'].apply(
        lambda x: 'Star' if x>=85 else 'Good' if x>=70 else 'Average' if x>=55 else 'At-Risk'
    )

    # Scholarship
    df['Scholarship'] = df.apply(
        lambda row: 'Eligible' if row['Average']>=80 and row['Fees']>12000 else 'No',
        axis=1
    )

    # Text cleaning
    df['Feedback'] = (
        df['Feedback']
        .str.lower()
        .str.strip()
        .str.replace(r'[^\w\s]', '', regex=True)
    )

    df['Positive'] = df['Feedback'].str.contains(
        'good|great|excellent|best|superb|brilliant'
    )

    return df


def remove_outliers(df):
    """Remove rows whose fees are outside the IQR range."""
    if df.empty or 'Fees' not in df:
        return df.copy()
    Q1 = df['Fees'].quantile(0.25)
    Q3 = df['Fees'].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    return df[(df['Fees'] >= lower) & (df['Fees'] <= upper)]


def merge_data(df):
    fee_status = pd.DataFrame({
        'Roll':[101,102,103],
        'Status':['Paid','Pending','Paid']
    })
    return pd.merge(df, fee_status, on='Roll', how='left')


def pivot_table(df):
    print("\n===== PIVOT TABLE =====\n")
    print(pd.pivot_table(
        df,
        values='Average',
        index='City',
        columns='Batch',
        aggfunc='mean',
        fill_value=0,
        margins=True
    ))

    print("\nCrosstab (City vs Grade):\n")
    print(pd.crosstab(df['City'], df['Grade']))


def save_all(df, output_dir="."):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "smartedu_data.csv", index=False)

    report = {
        "total_students": int(len(df)),
        "top_student": None if df.empty else str(df.loc[df['Average'].idxmax(), 'Name']),
        "average_score": None if df.empty else round(float(df['Average'].mean()), 2),
        "at_risk_students": int((df['Average'] < 55).sum()) if not df.empty else 0,
        "grade_distribution": {
            str(grade): int(count)
            for grade, count in df['Grade'].value_counts().sort_index().items()
        } if not df.empty else {}
    }

    with (output_dir / "report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    with (output_dir / "summary.txt").open("w", encoding="utf-8") as f:
        for i in df['Name']:
            f.write(i + "\n")

    print(" Files Saved!")


def read_json_safe(path="report.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            print("\nJSON Data:", json.load(f))
    except FileNotFoundError:
        print(f"Report not found: {path}")
