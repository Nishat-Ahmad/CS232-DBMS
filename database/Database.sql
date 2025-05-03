CREATE TABLE users (
    id SERIAL PRIMARY KEY, -- 1
    name VARCHAR(255) NOT NULL, -- 'Ali Khan'
    email VARCHAR(255) UNIQUE NOT NULL, -- 'ali.khan@example.com'
    password VARCHAR(255) NOT NULL, -- '$2b$12$...'
    role VARCHAR(10) CHECK (role IN ('admin', 'student')) NOT NULL,
    type VARCHAR(50) -- 'student'
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    roll_number VARCHAR(100) UNIQUE -- '2023045'
);

CREATE TABLE admins (
    id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    admin_level VARCHAR(50) -- 'super'
);

CREATE TABLE meals (
    id SERIAL PRIMARY KEY, -- 1
    name VARCHAR(255) NOT NULL, -- 'Chicken Biryani'
    time VARCHAR(10) CHECK (time IN ('breakfast', 'lunch', 'dinner')) NOT NULL,
    price NUMERIC(10, 2) NOT NULL, -- 120.00
    inventory INTEGER NOT NULL -- 50
);

CREATE TABLE attendance (
    id SERIAL PRIMARY KEY, -- 1
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    meal_id INTEGER REFERENCES meals(id) ON DELETE CASCADE,
    date DATE NOT NULL, -- '2025-05-03'
    status VARCHAR(10) CHECK (status IN ('present', 'absent'))
);

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY, -- 1
    item_name VARCHAR(255) NOT NULL, -- 'Rice'
    quantity INTEGER NOT NULL -- 100
);

CREATE TABLE complaints (
    id SERIAL PRIMARY KEY, -- 1
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    message TEXT NOT NULL, -- 'The food was cold and late.'
    status VARCHAR(10) CHECK (status IN ('pending', 'resolved')) DEFAULT 'pending'
);

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY, -- 1
    message TEXT NOT NULL, -- 'Dinner will be served at 7:30 PM today.'
    target_role VARCHAR(10) CHECK (target_role IN ('admin', 'student', 'all')) NOT NULL
);

CREATE TABLE meal_schedule_templates (
    id SERIAL PRIMARY KEY, -- 1
    weekday VARCHAR(10) CHECK (weekday IN ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')),
    meal_time VARCHAR(10) CHECK (meal_time IN ('breakfast', 'lunch', 'dinner')),
    meal_name VARCHAR(255) -- 'Paratha and Chana'
);

CREATE TABLE menu (
    id SERIAL PRIMARY KEY, -- 1
    date DATE NOT NULL, -- '2025-05-05'
    meal_time VARCHAR(10) CHECK (meal_time IN ('breakfast', 'lunch', 'dinner')),
    meal_id INTEGER REFERENCES meals(id)
);

CREATE TABLE billing (
    id SERIAL PRIMARY KEY, -- 1
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    month VARCHAR(20) NOT NULL, -- 'April'
    year INTEGER NOT NULL, -- 2025
    amount NUMERIC(10, 2) NOT NULL -- 4500.00
);
