# import pandas as pd

# dataframe=pd.read_csv("data/job_details.csv")

# def Job_matching():
#     print(dataframe["Job Description"])

# Job_matching()


import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import os
import warnings
import time

warnings.filterwarnings("ignore")

# ================= CONFIG =================
JOB_CSV_PATH = "./data/job_details.csv"
OUTPUT_CSV_PATH = "./data"
RESUME_TEXT_PATH = "C:\\Users\\Mayank kumar\\Downloads\\Resume.pdf"  # Add your resume as plain text
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Or use 'BAAI/bge-small-en', etc.
SIMILARITY_THRESHOLD = 0.7

# ============== LOAD MODEL ==============
print("📥 Loading model…")
model = SentenceTransformer(EMBEDDING_MODEL)
print("✅ Model loaded")

# ============== LOAD RESUME ==============
print("📄 Reading resume…")
if not os.path.exists(RESUME_TEXT_PATH):
    raise FileNotFoundError(f"Resume file not found at {RESUME_TEXT_PATH}")

# Robust encoding fallback
try:
    with open(RESUME_TEXT_PATH, "r", encoding="utf‑8") as f:
        resume_text = f.read()
except UnicodeDecodeError:
    with open(RESUME_TEXT_PATH, "r", encoding="latin1", errors="ignore") as f:
        resume_text = f.read()

resume_embedding = model.encode(resume_text, convert_to_tensor=True)

# ============== LOAD JOB DATA ==============
print("📂 Loading job data…")
try:
    df = pd.read_csv(JOB_CSV_PATH)
except Exception as e:
    raise RuntimeError(f"Error loading CSV: {e}")

print(f"🔍 Total jobs found: {len(df)}")

# ============== FILTER JOBS ==============
relevant_rows = []
for _, row in df.iterrows():
    job_desc = row.get("Job Description", "")
    if not isinstance(job_desc, str) or len(job_desc.strip()) == 0:
        continue  # Skip if description missing

    job_emb = model.encode(job_desc, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(resume_embedding, job_emb).item()

    if similarity >= SIMILARITY_THRESHOLD:
        relevant_rows.append(row)
        print(f"✅ [{similarity:.2f}] {row.get('Job Profile')} @ {row.get('Company Name')}")
    else:
        print(f"❌ [{similarity:.2f}] {row.get('Job Profile')} skipped")

# ============== SAVE RELEVANT JOBS ==============
if relevant_rows:
    filtered_df = pd.DataFrame(relevant_rows)
    filtered_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf‑8")
    print(f"💾 Saved {len(filtered_df)} relevant jobs → {OUTPUT_CSV_PATH}")
else:
    print("⚠️ No matching jobs found.")