// MongoDB initialization script
db = db.getSiblingDB('job_recommender');

// Create collections
db.createCollection('users');
db.createCollection('jobs');
db.createCollection('applications');
db.createCollection('saved_jobs');
db.createCollection('resumes');
db.createCollection('job_recommendations');

// Create indexes for better performance
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "firebase_uid": 1 }, { unique: true });

db.jobs.createIndex({ "title": "text", "description": "text", "company": "text" });
db.jobs.createIndex({ "location": 1 });
db.jobs.createIndex({ "salary_range": 1 });
db.jobs.createIndex({ "created_at": -1 });

db.applications.createIndex({ "user_id": 1, "job_id": 1 }, { unique: true });
db.applications.createIndex({ "user_id": 1 });
db.applications.createIndex({ "job_id": 1 });
db.applications.createIndex({ "status": 1 });

db.saved_jobs.createIndex({ "user_id": 1, "job_id": 1 }, { unique: true });
db.saved_jobs.createIndex({ "user_id": 1 });

db.resumes.createIndex({ "user_id": 1 });
db.resumes.createIndex({ "created_at": -1 });

db.job_recommendations.createIndex({ "user_id": 1 });
db.job_recommendations.createIndex({ "job_id": 1 });
db.job_recommendations.createIndex({ "score": -1 });

print('MongoDB initialization completed successfully!');
