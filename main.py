from job_scraper import load_job_data

def main():
    # Collect user inputs
    query = input("Enter the job title: ").strip()
    location = input("Enter your preferred job location: ").strip()
    
    # Fetch job data
    job_df = load_job_data(query, location)
    if job_df.empty:
        print("No jobs found. Please try different parameters.")
        return
    
    # Display job data
    print("\nAvailable Jobs:\n")
    print(job_df[['Job Title', 'Company', 'Location', 'Skills', 'Salary']])

# Run the script
if __name__ == "__main__":
    main()
