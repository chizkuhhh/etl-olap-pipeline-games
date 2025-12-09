CREATE INDEX idx_games_game_id ON games(game_id);
CREATE INDEX idx_games_average_playtime_forever ON games(average_playtime_forever);
CREATE INDEX idx_game_genres_game_id_gen_id ON game_genres(game_id, gen_id);
CREATE INDEX idx_genres_gen_id ON genres(gen_id);
CREATE INDEX idx_genres_genre ON genres(genre);
CREATE INDEX idx_games_release_date ON games(release_date);
CREATE INDEX idx_reviews_game_id ON reviews(game_id);
CREATE INDEX idx_games_release_date_linux ON games(release_date, linux_support);
CREATE INDEX idx_games_release_date_windows ON games(release_date, windows_support);
CREATE INDEX idx_games_release_date_mac ON games(release_date, mac_support);
CREATE INDEX idx_games_playtime ON games(game_id, average_playtime_forever);

-- roll-up
EXPLAIN SELECT
    gnr.genre AS Genre,
    COUNT(g.game_id) AS Total_Games,
    AVG(g.average_playtime_forever) AS Avg_Playtime_Forever
FROM games g
JOIN game_genres gg ON g.game_id = gg.game_id
JOIN genres gnr ON gg.gen_id = gnr.gen_id
GROUP BY gnr.genre
ORDER BY Avg_Playtime_Forever DESC;

-- optimized roll-up
EXPLAIN WITH GenreCounts AS (
    SELECT
        gg.gen_id,
        COUNT(g.game_id) AS Total_Games,
        AVG(g.average_playtime_forever) AS Avg_Playtime_Forever
    FROM Games g
    JOIN Game_Genres gg ON g.game_id = gg.game_id
    GROUP BY gg.gen_id
)
SELECT gnr.genre AS Genre, gc.Total_Games, gc.Avg_Playtime_Forever
FROM GenreCounts gc
JOIN Genres gnr ON gc.gen_id = gnr.gen_id
ORDER BY gc.Avg_Playtime_Forever DESC;


-- drill-down
SELECT
    MONTH(release_date) AS release_month,
    COUNT(reviews.review_id) AS total_reviews,
    SUM(recommendations) AS total_recommendations,
    AVG(average_playtime_forever) AS avg_playtime
FROM reviews
JOIN games ON reviews.game_id = games.game_id
WHERE YEAR(release_date) = 2023
GROUP BY MONTH(release_date);

-- optimized drill-down
EXPLAIN WITH FilteredGames AS (
    SELECT game_id, release_date, recommendations, average_playtime_forever
    FROM games
    WHERE YEAR(release_date) = 2023
)
SELECT
    MONTH(release_date) AS release_month,
    COUNT(reviews.review_id) AS total_reviews,
    SUM(recommendations) AS total_recommendations,
    AVG(average_playtime_forever) AS avg_playtime
FROM reviews
JOIN FilteredGames fg ON reviews.game_id = fg.game_id
GROUP BY MONTH(release_date);

-- slice
explain SELECT games.name, price
FROM games
JOIN game_genres ON games.game_id = game_genres.game_id
JOIN genres ON game_genres.gen_id = genres.gen_id
WHERE genres.genre = 'Action' AND YEAR(games.release_date) = 2023;

-- slice optimization
EXPLAIN WITH FilteredGames AS (
    SELECT game_id, name, price
    FROM games
    WHERE YEAR(release_date) = 2023
)
SELECT fg.name, fg.price
FROM FilteredGames fg
JOIN game_genres gg ON fg.game_id = gg.game_id
JOIN genres gnr ON gg.gen_id = gnr.gen_id
WHERE gnr.genre = 'Action';


-- dice
explain SELECT games.name, achievements
FROM games
JOIN game_genres ON games.game_id = game_genres.game_id
JOIN genres ON game_genres.gen_id = genres.gen_id
WHERE genres.genre = 'RPG'
AND YEAR(games.release_date) = 2023
AND games.linux_support = 1;

-- dice optimization
EXPLAIN WITH FilteredGames AS (
    SELECT game_id, name, achievements
    FROM games
    WHERE YEAR(release_date) = 2023 AND linux_support = 1
)
SELECT fg.name, fg.achievements
FROM FilteredGames fg
JOIN game_genres gg ON fg.game_id = gg.game_id
JOIN genres gnr ON gg.gen_id = gnr.gen_id
WHERE gnr.genre = 'RPG';

SHOW TABLE STATUS LIKE 'games';