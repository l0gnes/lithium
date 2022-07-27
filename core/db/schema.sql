CREATE TABLE IF NOT EXISTS guild_whitelist
(
    guildid BIGINT UNIQUE NOT NULL, 
    executor BIGINT NOT NULL,
    granted_on TIMESTAMP
);

CREATE TABLE IF NOT EXISTS repositories
(
    identifier VARCHAR(60) UNIQUE NOT NULL,
    link TEXT NOT NULL
);