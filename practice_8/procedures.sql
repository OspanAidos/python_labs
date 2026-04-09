-- Upsert procedure
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone_number = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone_number) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- Delete procedure
CREATE OR REPLACE PROCEDURE delete_contact_proc(p_target VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook 
    WHERE first_name = p_target OR phone_number = p_target;
END;
$$;