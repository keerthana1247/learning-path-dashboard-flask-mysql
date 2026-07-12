-- ============================================================================
-- Learning Path Dashboard — MySQL Schema
-- Run this file to create the database and all tables:
--   mysql -u root -p < database/schema.sql
-- ============================================================================

CREATE DATABASE IF NOT EXISTS learning_path_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE learning_path_db;

-- ----------------------------------------------------------------------------
-- USERS
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  user_id         INT AUTO_INCREMENT PRIMARY KEY,
  name            VARCHAR(120)  NOT NULL,
  email           VARCHAR(150)  NOT NULL UNIQUE,
  password_hash   VARCHAR(255)  NOT NULL,
  is_admin        BOOLEAN       DEFAULT FALSE,
  college         VARCHAR(150),
  department      VARCHAR(100),
  year            VARCHAR(20),
  career_goal     VARCHAR(100),
  interests       VARCHAR(255),
  created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- SKILLS  (a user's self-rated proficiency, 0-100, per skill)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS skills (
  skill_id     INT AUTO_INCREMENT PRIMARY KEY,
  user_id      INT NOT NULL,
  skill_name   VARCHAR(100) NOT NULL,
  rating       INT DEFAULT 0,
  updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_skills_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  CONSTRAINT uq_user_skill UNIQUE (user_id, skill_name)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- COURSES  (master course catalog)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS courses (
  course_id       INT AUTO_INCREMENT PRIMARY KEY,
  name            VARCHAR(150) NOT NULL,
  domain          VARCHAR(100),
  duration_hours  INT DEFAULT 10,
  difficulty      VARCHAR(20) DEFAULT 'Beginner',
  description     TEXT
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- LEARNING_PATHS  (ordered course sequence per career goal)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS learning_paths (
  path_id       INT AUTO_INCREMENT PRIMARY KEY,
  career_goal   VARCHAR(100) NOT NULL,
  course_id     INT NOT NULL,
  step_order    INT NOT NULL,
  CONSTRAINT fk_path_course FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- PROGRESS  (a user's enrollment + progress in a course)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS progress (
  progress_id       INT AUTO_INCREMENT PRIMARY KEY,
  user_id           INT NOT NULL,
  course_id         INT NOT NULL,
  progress_percent  INT DEFAULT 0,
  status            VARCHAR(20) DEFAULT 'Not Started',   -- Not Started / In Progress / Completed
  started_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at      TIMESTAMP NULL,
  CONSTRAINT fk_progress_user   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_progress_course FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
  CONSTRAINT uq_user_course UNIQUE (user_id, course_id)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- ACTIVITY_LOGS  (daily study-time entries; powers weekly/monthly analytics
-- and the Learning Health Score / streak calculations)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS activity_logs (
  log_id          INT AUTO_INCREMENT PRIMARY KEY,
  user_id         INT NOT NULL,
  course_id       INT NULL,
  activity_date   DATE NOT NULL,
  hours_spent     DECIMAL(4,1) DEFAULT 0.5,
  CONSTRAINT fk_activity_user   FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_activity_course FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- GOALS  (weekly / monthly targets)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS goals (
  goal_id        INT AUTO_INCREMENT PRIMARY KEY,
  user_id        INT NOT NULL,
  title          VARCHAR(200) NOT NULL,
  goal_type      VARCHAR(20) DEFAULT 'weekly',   -- weekly / monthly
  target_value   INT DEFAULT 1,
  current_value  INT DEFAULT 0,
  start_date     DATE,
  end_date       DATE,
  completed      BOOLEAN DEFAULT FALSE,
  CONSTRAINT fk_goals_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- CERTIFICATES  (uploaded certificate portfolio)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS certificates (
  certificate_id  INT AUTO_INCREMENT PRIMARY KEY,
  user_id         INT NOT NULL,
  platform        VARCHAR(100),
  title           VARCHAR(200),
  filename        VARCHAR(255),
  uploaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_certificates_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Helpful indexes
-- ----------------------------------------------------------------------------
CREATE INDEX idx_activity_user_date ON activity_logs(user_id, activity_date);
CREATE INDEX idx_progress_user      ON progress(user_id);
CREATE INDEX idx_learning_paths_goal ON learning_paths(career_goal, step_order);
CREATE INDEX idx_skills_user        ON skills(user_id);
