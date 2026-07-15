-- ============================================================================
-- Seed data: course catalog + per-goal learning paths + a default admin user
-- Run AFTER schema.sql:
--   mysql -u root -p learning_path_db < database/seed_data.sql
-- ============================================================================

USE learning_path_db;

-- ----------------------------------------------------------------------------
-- NOTE on the admin account: it is intentionally NOT seeded here.
-- utils/seed.py creates it automatically the first time app.py starts
-- (email: admin@learnpath.local / password: admin123), using Werkzeug to
-- generate a correct password hash at runtime. Inserting it manually via
-- SQL would require a pre-computed hash that could go stale between
-- Werkzeug versions — letting the app seed it avoids that entirely.
-- ----------------------------------------------------------------------------

-- ----------------------------------------------------------------------------
-- Courses
-- ----------------------------------------------------------------------------
INSERT INTO courses (name, domain, duration_hours, difficulty, description) VALUES
('Python Basics', 'Python', 12, 'Beginner', 'Core Python syntax, data types, and control flow.'),
('SQL Fundamentals', 'Data Analytics', 10, 'Beginner', 'Querying relational databases with SQL.'),
('Statistics for Data Analysis', 'Data Analytics', 14, 'Beginner', 'Descriptive and inferential statistics.'),
('Excel for Data Analysis', 'Data Analytics', 8, 'Beginner', 'Pivot tables, formulas, and dashboards in Excel.'),
('Data Visualization Principles', 'Data Analytics', 10, 'Intermediate', 'Designing clear, honest visual stories.'),
('Pandas for Data Analysis', 'Data Analytics', 12, 'Intermediate', 'Data wrangling with the pandas library.'),
('NumPy Essentials', 'Data Analytics', 8, 'Intermediate', 'Numerical computing with NumPy arrays.'),
('Machine Learning Basics', 'Machine Learning', 20, 'Intermediate', 'Supervised/unsupervised learning fundamentals.'),
('Power BI for Analysts', 'Data Analytics', 10, 'Intermediate', 'Building interactive BI reports and dashboards.'),
('Portfolio Projects: Data Analytics', 'Data Analytics', 15, 'Advanced', 'Capstone projects for your portfolio.'),

('Advanced Python', 'Python', 14, 'Intermediate', 'OOP, decorators, generators, and testing.'),
('Deep Learning Foundations', 'Machine Learning', 22, 'Advanced', 'Neural networks, CNNs, and RNNs.'),
('Feature Engineering', 'Machine Learning', 12, 'Intermediate', 'Preparing data for predictive models.'),
('MLOps Fundamentals', 'Machine Learning', 14, 'Advanced', 'Deploying and monitoring ML models.'),
('Portfolio Projects: Data Science', 'Machine Learning', 18, 'Advanced', 'End-to-end data science capstone.'),

('HTML, CSS & Bootstrap', 'Web Development', 10, 'Beginner', 'Building responsive page layouts.'),
('JavaScript Essentials', 'Web Development', 14, 'Beginner', 'Core JS, DOM manipulation, events.'),
('Flask Web Development', 'Web Development', 16, 'Intermediate', 'Building server-rendered apps with Flask.'),
('React Fundamentals', 'Web Development', 16, 'Intermediate', 'Component-based front-end development.'),
('REST API Design', 'Web Development', 10, 'Intermediate', 'Designing and consuming REST APIs.'),
('Databases for Web Apps', 'Web Development', 10, 'Intermediate', 'Relational modelling with MySQL.'),
('Portfolio Projects: Full Stack', 'Web Development', 20, 'Advanced', 'A complete full-stack capstone app.'),

('Cloud Computing Basics', 'Cloud Computing', 10, 'Beginner', 'Core cloud concepts: IaaS, PaaS, SaaS.'),
('AWS Fundamentals', 'Cloud Computing', 16, 'Intermediate', 'Core AWS services: EC2, S3, IAM.'),
('Docker & Containers', 'Cloud Computing', 12, 'Intermediate', 'Containerizing and shipping applications.'),
('Kubernetes Essentials', 'Cloud Computing', 16, 'Advanced', 'Orchestrating containers at scale.'),
('CI/CD Pipelines', 'Cloud Computing', 12, 'Advanced', 'Automating build, test, and deploy.'),

('UI/UX Design Principles', 'UI/UX', 10, 'Beginner', 'Usability heuristics and design thinking.'),
('Wireframing & Prototyping', 'UI/UX', 10, 'Beginner', 'Low- and high-fidelity prototypes.'),
('Figma Essentials', 'UI/UX', 8, 'Beginner', 'Designing interfaces in Figma.'),
('User Research Methods', 'UI/UX', 10, 'Intermediate', 'Interviews, surveys, and usability testing.'),
('Portfolio Projects: UI/UX', 'UI/UX', 14, 'Advanced', 'A polished case-study portfolio.'),

('Cyber Security Fundamentals', 'Cyber Security', 12, 'Beginner', 'CIA triad, threats, and vulnerabilities.'),
('Network Security', 'Cyber Security', 14, 'Intermediate', 'Firewalls, VPNs, and secure protocols.'),
('Ethical Hacking Basics', 'Cyber Security', 16, 'Intermediate', 'Penetration testing fundamentals.'),
('Security Operations (SOC)', 'Cyber Security', 14, 'Advanced', 'Incident detection and response.'),
('Portfolio Projects: Cyber Security', 'Cyber Security', 16, 'Advanced', 'Applied security capstone project.'),

('Linux & Shell Scripting', 'Cloud Computing', 10, 'Beginner', 'Command-line proficiency and automation.'),
('Git & Version Control', 'Web Development', 6, 'Beginner', 'Branching, merging, and collaboration.');

-- ----------------------------------------------------------------------------
-- Learning paths (ordered course sequence per career goal)
-- ----------------------------------------------------------------------------
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Analyst', course_id, 1 FROM courses WHERE name = 'Python Basics';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Analyst', course_id, 2 FROM courses WHERE name = 'SQL Fundamentals';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Analyst', course_id, 3 FROM courses WHERE name = 'Statistics for Data Analysis';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Analyst', course_id, 4 FROM courses WHERE name = 'Excel for Data Analysis';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Analyst', course_id, 5 FROM courses WHERE name = 'Data Visualization Principles';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Analyst', course_id, 6 FROM courses WHERE name = 'Pandas for Data Analysis';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Analyst', course_id, 7 FROM courses WHERE name = 'NumPy Essentials';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Analyst', course_id, 8 FROM courses WHERE name = 'Machine Learning Basics';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Analyst', course_id, 9 FROM courses WHERE name = 'Power BI for Analysts';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Analyst', course_id, 10 FROM courses WHERE name = 'Portfolio Projects: Data Analytics';

INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Scientist', course_id, 1 FROM courses WHERE name = 'Python Basics';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Scientist', course_id, 2 FROM courses WHERE name = 'Statistics for Data Analysis';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Scientist', course_id, 3 FROM courses WHERE name = 'Pandas for Data Analysis';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Scientist', course_id, 4 FROM courses WHERE name = 'NumPy Essentials';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Scientist', course_id, 5 FROM courses WHERE name = 'Machine Learning Basics';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Scientist', course_id, 6 FROM courses WHERE name = 'Feature Engineering';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Scientist', course_id, 7 FROM courses WHERE name = 'Deep Learning Foundations';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Scientist', course_id, 8 FROM courses WHERE name = 'MLOps Fundamentals';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Data Scientist', course_id, 9 FROM courses WHERE name = 'Portfolio Projects: Data Science';

INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Full Stack Developer', course_id, 1 FROM courses WHERE name = 'HTML, CSS & Bootstrap';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Full Stack Developer', course_id, 2 FROM courses WHERE name = 'JavaScript Essentials';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Full Stack Developer', course_id, 3 FROM courses WHERE name = 'Git & Version Control';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Full Stack Developer', course_id, 4 FROM courses WHERE name = 'Python Basics';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Full Stack Developer', course_id, 5 FROM courses WHERE name = 'Flask Web Development';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Full Stack Developer', course_id, 6 FROM courses WHERE name = 'Databases for Web Apps';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Full Stack Developer', course_id, 7 FROM courses WHERE name = 'REST API Design';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Full Stack Developer', course_id, 8 FROM courses WHERE name = 'React Fundamentals';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Full Stack Developer', course_id, 9 FROM courses WHERE name = 'Portfolio Projects: Full Stack';

INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Machine Learning Engineer', course_id, 1 FROM courses WHERE name = 'Python Basics';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Machine Learning Engineer', course_id, 2 FROM courses WHERE name = 'Advanced Python';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Machine Learning Engineer', course_id, 3 FROM courses WHERE name = 'Statistics for Data Analysis';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Machine Learning Engineer', course_id, 4 FROM courses WHERE name = 'NumPy Essentials';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Machine Learning Engineer', course_id, 5 FROM courses WHERE name = 'Machine Learning Basics';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Machine Learning Engineer', course_id, 6 FROM courses WHERE name = 'Feature Engineering';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Machine Learning Engineer', course_id, 7 FROM courses WHERE name = 'Deep Learning Foundations';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Machine Learning Engineer', course_id, 8 FROM courses WHERE name = 'MLOps Fundamentals';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Machine Learning Engineer', course_id, 9 FROM courses WHERE name = 'Portfolio Projects: Data Science';

INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cloud Engineer', course_id, 1 FROM courses WHERE name = 'Linux & Shell Scripting';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cloud Engineer', course_id, 2 FROM courses WHERE name = 'Cloud Computing Basics';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cloud Engineer', course_id, 3 FROM courses WHERE name = 'AWS Fundamentals';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cloud Engineer', course_id, 4 FROM courses WHERE name = 'Docker & Containers';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cloud Engineer', course_id, 5 FROM courses WHERE name = 'Kubernetes Essentials';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cloud Engineer', course_id, 6 FROM courses WHERE name = 'CI/CD Pipelines';

INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'UI/UX Designer', course_id, 1 FROM courses WHERE name = 'UI/UX Design Principles';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'UI/UX Designer', course_id, 2 FROM courses WHERE name = 'Wireframing & Prototyping';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'UI/UX Designer', course_id, 3 FROM courses WHERE name = 'Figma Essentials';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'UI/UX Designer', course_id, 4 FROM courses WHERE name = 'User Research Methods';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'UI/UX Designer', course_id, 5 FROM courses WHERE name = 'HTML, CSS & Bootstrap';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'UI/UX Designer', course_id, 6 FROM courses WHERE name = 'Portfolio Projects: UI/UX';

INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cyber Security Analyst', course_id, 1 FROM courses WHERE name = 'Cyber Security Fundamentals';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cyber Security Analyst', course_id, 2 FROM courses WHERE name = 'Linux & Shell Scripting';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cyber Security Analyst', course_id, 3 FROM courses WHERE name = 'Network Security';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cyber Security Analyst', course_id, 4 FROM courses WHERE name = 'Ethical Hacking Basics';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cyber Security Analyst', course_id, 5 FROM courses WHERE name = 'Security Operations (SOC)';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'Cyber Security Analyst', course_id, 6 FROM courses WHERE name = 'Portfolio Projects: Cyber Security';

INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'DevOps Engineer', course_id, 1 FROM courses WHERE name = 'Linux & Shell Scripting';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'DevOps Engineer', course_id, 2 FROM courses WHERE name = 'Git & Version Control';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'DevOps Engineer', course_id, 3 FROM courses WHERE name = 'Cloud Computing Basics';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'DevOps Engineer', course_id, 4 FROM courses WHERE name = 'Docker & Containers';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'DevOps Engineer', course_id, 5 FROM courses WHERE name = 'Kubernetes Essentials';
INSERT INTO learning_paths (career_goal, course_id, step_order)
SELECT 'DevOps Engineer', course_id, 6 FROM courses WHERE name = 'CI/CD Pipelines';
