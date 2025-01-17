-- Create the users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the user_relations table to relate users
CREATE TABLE user_relations (
    relation_id SERIAL PRIMARY KEY,
    user_id INT,
    related_user_id INT,
    relation_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (related_user_id) REFERENCES users(user_id)
);

DROP TABLE user_relations;
DROP TABLE users;
