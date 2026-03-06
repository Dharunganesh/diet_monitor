CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    height FLOAT,
    weight FLOAT,
    calorie_goal INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE food_classes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    calories_per_100g FLOAT,
    protein_per_100g FLOAT,
    carbs_per_100g FLOAT,
    fats_per_100g FLOAT
);

CREATE TABLE food_entries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    food_class_id INTEGER REFERENCES food_classes(id),
    quantity FLOAT,
    total_calories FLOAT,
    total_protein FLOAT,
    total_carbs FLOAT,
    total_fats FLOAT,
    image_path TEXT,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Week 5: Social Features
CREATE TABLE feed_posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    entry_id INTEGER REFERENCES food_entries(id),
    caption TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES feed_posts(id),
    user_id INTEGER REFERENCES users(id),
    comment_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES feed_posts(id),
    user_id INTEGER REFERENCES users(id)
);