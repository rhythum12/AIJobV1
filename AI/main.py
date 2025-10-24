from job_scraper import load_job_data
from recommender.job_recommender import JobRecommender
import pandas as pd
import re
import time

def fetch_jobs_safely(query, location):
    """Try shorter queries automatically until we get results."""
    print(f"\n🔍 Fetching jobs related to '{query}' in {location}...")
    job_df = load_job_data(query, location)
    if not job_df.empty:
        return job_df

    # If nothing found, trim query gradually
    terms = query.split()
    while len(terms) > 1:
        terms.pop()  # remove last word
        shorter = " ".join(terms)
        print(f"⚠️ Retrying with shorter query: '{shorter}'...")
        time.sleep(1)
        job_df = load_job_data(shorter, location)
        if not job_df.empty:
            return job_df
    return pd.DataFrame()

def main():
    print("\n=== 🤖 AI Job Recommendation System ===\n")

    query = input("Enter the job title (press Enter to skip): ").strip()
    location = input("Enter your preferred job location (e.g., Perth): ").strip()
    skills_input = input("Enter your skills (comma separated, press Enter to skip): ").strip()

    skills_input = re.sub(r"[,;]+", " ", skills_input)
    skills = [s.strip() for s in skills_input.split() if s.strip()]

    if not query and not skills:
        print("\n⚠️ You must enter at least a job title or one skill.")
        return

    # auto domain context
    base_keywords = ""
    combined = (query + " " + " ".join(skills)).lower()
    if any(k in combined for k in ["nurse", "first aid", "cpr", "care", "health", "medical"]):
        base_keywords = "healthcare nursing hospital"
    elif any(k in combined for k in ["python", "data", "machine", "ai", "software", "developer", "engineer"]):
        base_keywords = "software data technology IT"
    elif any(k in combined for k in ["teacher", "childcare", "education", "trainer", "school"]):
        base_keywords = "education teaching childcare"
    elif any(k in combined for k in ["electrician", "construction", "mechanic", "technician"]):
        base_keywords = "trade construction engineering"
    else:
        base_keywords = "job work employment"

    search_query = " ".join(filter(None, [query, " ".join(skills), base_keywords]))

    # Limit to 5 words for Adzuna stability
    search_terms = search_query.split()
    if len(search_terms) > 5:
        search_query = " ".join(search_terms[:5])

    job_df = fetch_jobs_safely(search_query, location)
    if job_df.empty:
        print("❌ Still no jobs found after retrying.")
        return

    print(f"✅ Fetched {len(job_df)} jobs from Adzuna.")
    job_df.to_csv("jobs.csv", index=False)
    print("💾 Saved jobs to jobs.csv")

    df = pd.DataFrame({
        "job_id": range(len(job_df)),
        "title": job_df["Job Title"],
        "company": job_df["Company"],
        "description": job_df["Description"],
        "skills": job_df["Skills"],
        "location": job_df["Location"],
        "posted_at": pd.Timestamp.now(),
        "employment_type": "Full-time",
        "remote": False,
        "salary_min": job_df["Salary"],
        "salary_max": job_df["Salary"],
        "currency": "AUD",
        "url": ""
    })

    print("\n🔧 Training recommender model...")
    rec = JobRecommender().fit(df)

    user_vec = rec.build_user_profile(
        target_title=query if query else "",
        skills=skills,
        resume_text=f"Candidate skilled in {', '.join(skills)}"
    )

    print("\n🎯 Generating AI-based job recommendations...\n")
    recs = rec.recommend(
        user_vector=user_vec,
        k=10,
        user_location=location,
        desired_salary_min=60000,
        desired_salary_max=200000
    )

    if recs.empty:
        print("⚠️ No relevant recommendations found.")
    else:
        pd.set_option("display.max_colwidth", 100)
        print("=== Top Job Recommendations ===\n")
        print(recs[["title", "company", "location", "salary_min", "salary_max", "score"]]
              .to_string(index=False))

if __name__ == "__main__":
    main()
