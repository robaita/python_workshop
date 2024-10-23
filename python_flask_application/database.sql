CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name text NOT NULL,
    task_date date,
    estimated_time time,
    spent_time time,
    task_duration time,
    task_status varchar(15)
);