-- Create table

CREATE TABLE IF NOT EXISTS course_copy (
    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id TEXT,
    copied_from TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
