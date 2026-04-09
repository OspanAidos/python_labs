-- Pattern search function
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT user_id, first_name, phone_number FROM phonebook
    WHERE first_name ILIKE '%' || p_pattern || '%'
       OR phone_number LIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- Pagination function
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT user_id, first_name, phone_number FROM phonebook
    ORDER BY user_id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;