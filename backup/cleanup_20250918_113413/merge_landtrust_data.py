import os
import pandas as pd

# Base directory (relative to this script)
BASE_DIR = os.path.dirname(__file__)

# Paths to datasets
base_path = os.path.join(BASE_DIR, "../data/landtrusts/datasets")
socials_path = os.path.join(base_path, "landtrust_master_with_socials.tsv")
phase2_path = os.path.join(base_path, "phase2_scrape.tsv")  # updated here

# Logo and screenshot directories
logos_dir = os.path.join(base_path, "screens/logos")
screens_dir = os.path.join(base_path, "screens/screenshots")

# Output file
output_path = os.path.join(base_path, "landtrust_master_final.tsv")

# Load datasets
socials = pd.read_csv(socials_path, sep="\t")
phase2 = pd.read_csv(phase2_path, sep="\t")

# Normalize org names for merging (basic lowercasing + stripping)
socials["Organization_norm"] = socials["Organization"].str.lower().str.strip()
phase2["Organization_norm"] = phase2["Organization"].str.lower().str.strip()

# Merge datasets
merged = pd.merge(
    socials,
    phase2.drop(columns=["URL"]),  # avoid duplicate URL columns
    on="Organization_norm",
    how="left",
    suffixes=("", "_phase2")
)

# Add logo and screenshot paths
def find_file(org_name, folder):
    safe_name = org_name.replace(" ", "_").replace("/", "_")
    for ext in [".png", ".jpg", ".jpeg", ".svg", ".webp"]:
        candidate = os.path.join(folder, f"{safe_name}_logo{ext}")
        if os.path.exists(candidate):
            return candidate
        candidate2 = os.path.join(folder, f"{safe_name}_homepage{ext}")
        if os.path.exists(candidate2):
            return candidate2
    return ""

merged["LogoPath"] = merged["Organization"].apply(lambda x: find_file(x, logos_dir))
merged["ScreenshotPath"] = merged["Organization"].apply(lambda x: find_file(x, screens_dir))

# Save final master file
merged.to_csv(output_path, sep="\t", index=False)

print(f"✅ Master file written to {output_path}")