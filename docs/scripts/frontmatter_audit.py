#!/usr/bin/env python3
"""DCLT Frontmatter Audit - finds files missing frontmatter and optionally adds starter YAML.

Usage:
    python scripts/frontmatter_audit.py              # audit only
    python scripts/frontmatter_audit.py --fix        # add frontmatter
    python scripts/frontmatter_audit.py --fix --dir 02_EXECUTION
"""
import os, sys
from pathlib import Path
from datetime import date

SKIP = {"legacy_site_content","node_modules",".git","__pycache__","attachment",
        "wordpress-posts","current-site-screenshots","export","overrides",
        "_archive","migrated-stories"}
SKIP_F = {"index.md","README.md","DASHBOARD.md","SCHEMA.md"}

def has_fm(fp):
    try:
        with open(fp,"r",encoding="utf-8",errors="replace") as f:
            return f.readline().strip()=="---"
    except: return False

def heading(fp):
    try:
        with open(fp,"r",encoding="utf-8",errors="replace") as f:
            for l in f:
                l=l.strip()
                if l.startswith("# "): return l.lstrip("# ").strip()
                if l.startswith("## "): return l.lstrip("# ").strip()
    except: pass
    return None

def infer_type(rp):
    s=str(rp)
    if s.startswith("01"): return "strategy"
    if s.startswith("02"): return "execution"
    if s.startswith("03"): return "reference"
    if s.startswith("04"): return "daily"
    return "reference"

def gen_fm(fp,rp):
    t=heading(fp) or fp.stem.replace("-"," ").replace("_"," ").title()
    t=t.replace(chr(34),chr(92)+chr(34))
    ty=infer_type(rp)
    d=date.today().isoformat()
    return f"---\ntitle: \"{t}\"\ntype: {ty}\nstatus: active\nupdated: {d}\ntags: []\n---\n\n"

def main():
    fix = "--fix" in sys.argv
    td = None
    for i,a in enumerate(sys.argv):
        if a=="--dir" and i+1<len(sys.argv): td=sys.argv[i+1]
    ws=Path(".").resolve()
    for a in sys.argv[1:]:
        if not a.startswith("-"): ws=Path(a).resolve(); break
    print(f"Scanning: {ws}")
    print(f"Mode: {'FIX' if fix else 'AUDIT'}\n")
    missing,hf,tot=[],0,0
    for dp,dns,fns in os.walk(ws):
        dns[:]=[d for d in dns if d not in SKIP]
        rd=Path(dp).relative_to(ws)
        if td and not str(rd).startswith(td): continue
        for fn in sorted(fns):
            if not fn.endswith(".md") or fn in SKIP_F: continue
            fp=Path(dp)/fn; rp=rd/fn; tot+=1
            if has_fm(fp): hf+=1
            else: missing.append((fp,rp))
    print(f"Total: {tot} | With FM: {hf} | Missing: {len(missing)}\n")
    if not missing: print("All files have frontmatter!"); return
    if fix:
        fx=0
        for fp,rp in missing:
            fm=gen_fm(fp,rp)
            try:
                c=open(fp,"r",encoding="utf-8",errors="replace").read()
                open(fp,"w",encoding="utf-8").write(fm+c); fx+=1
                print(f"  + {rp}")
            except Exception as e: print(f"  ERR: {rp} - {e}")
        print(f"\nFixed {fx} files.")
    else:
        for fp,rp in missing[:30]: print(f"  {rp}")
        if len(missing)>30: print(f"  ...and {len(missing)-30} more")
        print("\nRun with --fix to add starter frontmatter.")

if __name__=="__main__": main()