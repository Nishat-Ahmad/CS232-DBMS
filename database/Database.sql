-- Users
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50),
    password VARCHAR(255)
);

-- Weekly Menu
CREATE TABLE WeeklyMenu (
    menu_id SERIAL PRIMARY KEY,
    weekday VARCHAR(10) NOT NULL,     -- e.g. 'Monday'
    meal_type VARCHAR(50) NOT NULL,   -- e.g. 'Lunch', 'Dinner'
    items TEXT                        -- e.g. 'Rice, Dal, Paneer'
);

-- Meal Instance (Actual meal on a real date)
CREATE TABLE MealInstance (
    meal_id SERIAL PRIMARY KEY,
    menu_id INT REFERENCES WeeklyMenu(menu_id) ON DELETE CASCADE,
    date DATE NOT NULL                -- e.g. '2025-04-21'
);

-- Attendance (who showed up for which meal)
CREATE TABLE Attendance (
    attendance_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    meal_id INT REFERENCES MealInstance(meal_id) ON DELETE CASCADE,
    status VARCHAR(50),              -- 'present', 'absent', 'cancelled'
    UNIQUE(user_id, meal_id)         -- prevent duplicates
);

-- Billing (how much each user owes)
CREATE TABLE Billing (
    bill_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    month VARCHAR(20),               -- e.g. 'April'
    total_meals INT,
    total_breakfasts INT,
    amount NUMERIC(10,2),
    generated_on DATE,
    is_paid BOOLEAN DEFAULT FALSE
);

-- Inventory (optional but useful)
CREATE TABLE Inventory (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    unit VARCHAR(50),                -- e.g. 'kg', 'litre'
    quantity INT,
    updated_on DATE
);

