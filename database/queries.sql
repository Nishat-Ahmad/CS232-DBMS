CREATE TABLE IF NOT EXISTS deleted_meals AS TABLE meals WITH NO DATA;
ALTER TABLE deleted_meals ADD COLUMN deleted_at TIMESTAMP DEFAULT now();

CREATE OR REPLACE FUNCTION archive_meal_before_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO deleted_meals SELECT OLD.*, now();
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_archive_meal ON meals;
CREATE TRIGGER trigger_archive_meal
BEFORE DELETE ON meals
FOR EACH ROW
EXECUTE FUNCTION archive_meal_before_delete();

CREATE TABLE IF NOT EXISTS deleted_menus AS TABLE menus WITH NO DATA;
ALTER TABLE deleted_menus ADD COLUMN deleted_at TIMESTAMP DEFAULT now();

CREATE OR REPLACE FUNCTION archive_menu_before_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO deleted_menus SELECT OLD.*, now();
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_archive_menu ON menus;
CREATE TRIGGER trigger_archive_menu
BEFORE DELETE ON menus
FOR EACH ROW
EXECUTE FUNCTION archive_menu_before_delete();

CREATE TABLE IF NOT EXISTS deleted_users AS TABLE users WITH NO DATA;
ALTER TABLE deleted_users ADD COLUMN deleted_at TIMESTAMP DEFAULT now();

CREATE OR REPLACE PROCEDURE archive_user_proc()
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO deleted_users SELECT *, now() FROM users WHERE id = (SELECT id FROM users ORDER BY id DESC LIMIT 1);
END;
$$;

CREATE OR REPLACE FUNCTION archive_user_before_delete()
RETURNS TRIGGER AS $$
BEGIN
    CALL archive_user_proc();
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_archive_user ON users;
CREATE TRIGGER trigger_archive_user
BEFORE DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION archive_user_before_delete();

CREATE TABLE IF NOT EXISTS deleted_attendance AS TABLE attendance WITH NO DATA;
ALTER TABLE deleted_attendance ADD COLUMN deleted_at TIMESTAMP DEFAULT now();

CREATE OR REPLACE FUNCTION archive_attendance_before_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO deleted_attendance SELECT OLD.*, now();
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_archive_attendance ON attendance;
CREATE TRIGGER trigger_archive_attendance
BEFORE DELETE ON attendance
FOR EACH ROW
EXECUTE FUNCTION archive_attendance_before_delete();