CREATE TABLE IF NOT EXISTS guild_whitelist
(
    guildid BIGINT UNIQUE NOT NULL, 
    executor BIGINT NOT NULL,
    granted_on TIMESTAMP
);
