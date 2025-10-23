-- PostgreSQL initialization script
-- Create database if it doesn't exist (this is handled by POSTGRES_DB env var)

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    firebase_uid VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    phone VARCHAR(20),
    location VARCHAR(255),
    bio TEXT,
    skills TEXT[],
    experience_level VARCHAR(50),
    preferred_job_types TEXT[],
    salary_expectation INTEGER,
    availability VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create companies table
CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    industry VARCHAR(100),
    size VARCHAR(50),
    location VARCHAR(255),
    logo_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create jobs table
CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT[],
    responsibilities TEXT[],
    benefits TEXT[],
    location VARCHAR(255),
    remote_option BOOLEAN DEFAULT FALSE,
    job_type VARCHAR(50), -- full-time, part-time, contract, internship
    experience_level VARCHAR(50), -- entry, mid, senior, executive
    salary_min INTEGER,
    salary_max INTEGER,
    currency VARCHAR(3) DEFAULT 'USD',
    application_deadline DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create applications table
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'applied', -- applied, reviewed, interviewed, rejected, accepted
    cover_letter TEXT,
    resume_url VARCHAR(500),
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, job_id)
);

-- Create saved_jobs table
CREATE TABLE IF NOT EXISTS saved_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, job_id)
);

-- Create resumes table
CREATE TABLE IF NOT EXISTS resumes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255),
    file_url VARCHAR(500),
    file_size INTEGER,
    analysis_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create job_recommendations table
CREATE TABLE IF NOT EXISTS job_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    score DECIMAL(5,2),
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, job_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_firebase_uid ON users(firebase_uid);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_skills ON users USING GIN(skills);

CREATE INDEX IF NOT EXISTS idx_jobs_company_id ON jobs(company_id);
CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs USING GIN(to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_jobs_description ON jobs USING GIN(to_tsvector('english', description));
CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location);
CREATE INDEX IF NOT EXISTS idx_jobs_job_type ON jobs(job_type);
CREATE INDEX IF NOT EXISTS idx_jobs_experience_level ON jobs(experience_level);
CREATE INDEX IF NOT EXISTS idx_jobs_salary_range ON jobs(salary_min, salary_max);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at);
CREATE INDEX IF NOT EXISTS idx_jobs_active ON jobs(is_active);

CREATE INDEX IF NOT EXISTS idx_applications_user_id ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_job_id ON applications(job_id);
CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_applications_applied_at ON applications(applied_at);

CREATE INDEX IF NOT EXISTS idx_saved_jobs_user_id ON saved_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_saved_jobs_job_id ON saved_jobs(job_id);

CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_resumes_created_at ON resumes(created_at);

CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON job_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_job_id ON job_recommendations(job_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_score ON job_recommendations(score DESC);

-- Create functions for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_applications_updated_at BEFORE UPDATE ON applications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_resumes_updated_at BEFORE UPDATE ON resumes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO companies (name, description, website, industry, size, location) VALUES
('TechCorp Inc.', 'Leading technology company specializing in AI and machine learning solutions.', 'https://techcorp.com', 'Technology', 'Large', 'San Francisco, CA'),
('StartupXYZ', 'Innovative startup focused on sustainable technology solutions.', 'https://startupxyz.com', 'Technology', 'Small', 'Austin, TX'),
('DataCorp Solutions', 'Data analytics and business intelligence company.', 'https://datacorp.com', 'Data Analytics', 'Medium', 'New York, NY')
ON CONFLICT DO NOTHING;

-- Insert sample jobs
INSERT INTO jobs (company_id, title, description, requirements, responsibilities, location, job_type, experience_level, salary_min, salary_max) 
SELECT 
    c.id,
    'Software Engineer',
    'We are looking for a talented software engineer to join our development team.',
    ARRAY['Bachelor degree in Computer Science', '3+ years of experience', 'Proficiency in JavaScript, React, Node.js'],
    ARRAY['Develop web applications', 'Collaborate with team members', 'Write clean, maintainable code'],
    'San Francisco, CA',
    'full-time',
    'mid',
    80000,
    120000
FROM companies c WHERE c.name = 'TechCorp Inc.'
ON CONFLICT DO NOTHING;

INSERT INTO jobs (company_id, title, description, requirements, responsibilities, location, job_type, experience_level, salary_min, salary_max) 
SELECT 
    c.id,
    'Data Analyst',
    'Join our data team to analyze business metrics and provide insights.',
    ARRAY['Bachelor degree in Statistics or related field', '2+ years of experience', 'Proficiency in SQL, Python, R'],
    ARRAY['Analyze business data', 'Create reports and dashboards', 'Work with stakeholders'],
    'New York, NY',
    'full-time',
    'entry',
    60000,
    90000
FROM companies c WHERE c.name = 'DataCorp Solutions'
ON CONFLICT DO NOTHING;
