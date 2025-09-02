CREATE DATABASE recipe_recommender;

USE recipe_recommender;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

-- Recipes table
CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ingredients TEXT,
    recipe_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Linking table (users ↔ recipes)
CREATE TABLE user_recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    recipe_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);
