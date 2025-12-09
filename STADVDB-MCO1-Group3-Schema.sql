DROP SCHEMA IF EXISTS GamesData;

CREATE SCHEMA GamesData;

USE GamesData;

-- Create the Games table
CREATE TABLE Games (
    game_id INT PRIMARY KEY,
    name VARCHAR(255),
    release_date DATE,
    required_age INT,
    price DECIMAL(10, 2),
    dlc_count INT,
    detailed_description LONGTEXT,
    short_description TEXT,
    header_image VARCHAR(255),
    website VARCHAR(255),
    support_url TEXT,
    support_email VARCHAR(255),
    windows_support BOOLEAN,
    mac_support BOOLEAN,
    linux_support BOOLEAN,
    metacritic_score DECIMAL(3, 1),
    metacritic_url TEXT,
    achievements INT,
    recommendations INT,
    notes TEXT,
    user_score INT,
    score_rank INT,
    positive INT,
    negative INT,
    min_estimated_owners INT,
    max_estimated_owners INT,
    average_playtime_forever INT,
    average_playtime_2weeks INT,
    median_playtime_forever INT,
    median_playtime_2weeks INT,
    peak_ccu INT
);

-- Create the Customers table
CREATE TABLE Customers (
    customer_id VARCHAR(255) PRIMARY KEY,
    display_name VARCHAR(500)
);

-- Create the Reviews table
CREATE TABLE Reviews (
    review_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255),
    game_id INT,
    review_text TEXT,
    rating VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

-- Create the Languages table
CREATE TABLE Languages (
    lang_id VARCHAR(255) PRIMARY KEY,
    lang_name VARCHAR(255)
);

-- Create the Supported_Languages junction table
CREATE TABLE Supported_Languages (
    game_lang_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    lang_id VARCHAR(255),
    FOREIGN KEY (game_id) REFERENCES Games(game_id),
    FOREIGN KEY (lang_id) REFERENCES Languages(lang_id)
);

-- Create the Full_Audio_Languages junction table
CREATE TABLE Full_Audio_Languages (
    full_aud_lang_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    lang_id VARCHAR(255),
    FOREIGN KEY (game_id) REFERENCES Games(game_id),
    FOREIGN KEY (lang_id) REFERENCES Languages(lang_id)
);

-- Create the Packages table
CREATE TABLE Packages (
    pack_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    title VARCHAR(255),
    description TEXT,
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

-- Create the Subs table
CREATE TABLE Subs (
    sub_id VARCHAR(255) PRIMARY KEY,
    pack_id VARCHAR(255),
    text TEXT,
    description TEXT,
    price DECIMAL(10, 2),
    FOREIGN KEY (pack_id) REFERENCES Packages(pack_id)
);

-- Create the Developers table
CREATE TABLE Developers (
    dev_id VARCHAR(255) PRIMARY KEY,
    dev_name VARCHAR(255)
);

-- Create the Publishers table
CREATE TABLE Publishers (
    pub_id VARCHAR(255) PRIMARY KEY,
    pub_name VARCHAR(255)
);

-- Create the Game_Developers junction table
CREATE TABLE Game_Developers (
    game_dev_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    dev_id VARCHAR(255),
    FOREIGN KEY (game_id) REFERENCES Games(game_id),
    FOREIGN KEY (dev_id) REFERENCES Developers(dev_id)
);

-- Create the Game_Publishers junction table
CREATE TABLE Game_Publishers (
    game_pub_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    pub_id VARCHAR(255),
    FOREIGN KEY (game_id) REFERENCES Games(game_id),
    FOREIGN KEY (pub_id) REFERENCES Publishers(pub_id)
);

-- Create the Categories table
CREATE TABLE Categories (
    cat_id VARCHAR(255) PRIMARY KEY,
    category VARCHAR(255)
);

-- Create the Genres table
CREATE TABLE Genres (
    gen_id VARCHAR(255) PRIMARY KEY,
    genre VARCHAR(255)
);

-- Create the Game_Categories junction table
CREATE TABLE Game_Categories (
    game_cat_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    cat_id VARCHAR(255),
    FOREIGN KEY (game_id) REFERENCES Games(game_id),
    FOREIGN KEY (cat_id) REFERENCES Categories(cat_id)
);

-- Create the Game_Genres junction table
CREATE TABLE Game_Genres (
    game_gen_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    gen_id VARCHAR(255),
    FOREIGN KEY (game_id) REFERENCES Games(game_id),
    FOREIGN KEY (gen_id) REFERENCES Genres(gen_id)
);

-- Create the Screenshots table
CREATE TABLE Screenshots (
    screenshot_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    ss_url TEXT,
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

-- Create the Movies table
CREATE TABLE Movies (
    movie_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    mov_url TEXT,
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

-- Create the Tags table
CREATE TABLE Tags (
    tag_id VARCHAR(255) PRIMARY KEY,
    tag_name VARCHAR(255)
);

-- Create the Game_Tags junction table
CREATE TABLE Game_Tags (
    game_tag_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    tag_id VARCHAR(255),
    tag_value VARCHAR(255),
    FOREIGN KEY (game_id) REFERENCES Games(game_id),
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
);
