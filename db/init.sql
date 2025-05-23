-- Учителя
CREATE TABLE teacher (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    experience INTEGER NOT NULL,
    specialty VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL
);

    CREATE TABLE course (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        teacher_id INTEGER NOT NULL,
        student_limit INTEGER NOT NULL,
        CONSTRAINT fk_course_teacher FOREIGN KEY (teacher_id)
            REFERENCES teacher (id)
            ON DELETE CASCADE
    );

CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

CREATE TABLE request (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id  INTEGER NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending' NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_request_student FOREIGN KEY (student_id)
        REFERENCES student (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_request_course FOREIGN KEY (course_id)
        REFERENCES course  (id)
        ON DELETE CASCADE
);

CREATE UNIQUE INDEX uq_student_pending_request 
    ON request (student_id) 
    WHERE (status = 'pending');

CREATE OR REPLACE FUNCTION check_course_limit()
RETURNS TRIGGER AS $$
DECLARE 
    current_count INTEGER;
    max_limit INTEGER;
BEGIN
    IF NEW.status = 'approved' THEN
        SELECT student_limit INTO max_limit 
        FROM course 
        WHERE id = NEW.course_id;

        SELECT COUNT(*) INTO current_count 
        FROM request 
        WHERE 
            course_id = NEW.course_id AND 
            status = 'approved' AND 
            id != COALESCE(NEW.id, 0);

        IF current_count >= max_limit THEN
            RAISE EXCEPTION 'Course student limit exceeded';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_course_limit
BEFORE INSERT OR UPDATE ON request
FOR EACH ROW EXECUTE FUNCTION check_course_limit();