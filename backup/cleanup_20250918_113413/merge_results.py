import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--scrape", required=True, help="Path to scrape.csv")
parser.add_argument("--audit", required=True, help="Path to audit_summary.csv")
parser.add_argument("--out", required=True, help="Output CSV path")
args = parser.parse_args()

scrape = pd.read_csv(args.scrape)
audit = pd.read_csv(args.audit)

merged = scrape.merge(audit, how="left", left_on=["State","Organization","URL"], right_on=["State","Organization","URL"])
merged.to_csv(args.out, index=False)
print("Wrote", args.out)
