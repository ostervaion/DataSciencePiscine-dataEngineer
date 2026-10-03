CREATE SCHEMA IF NOT EXISTS "table";

CREATE TABLE IF NOT EXISTS "table".data_2022_oct (
    event_time TIMESTAMP WITH TIME ZONE,
    event_type VARCHAR(50),
    product_id BIGINT,
    price DECIMAL(10, 2),
    user_id INT,
    user_session UUID
);

\copy "table".data_2022_oct FROM '../customer/data_2022-oct.csv' WITH (FORMAT csv, HEADER true);
