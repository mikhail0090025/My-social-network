CREATE TABLE IF NOT EXISTS UserProfile (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    name VARCHAR(15) NOT NULL,
    surname VARCHAR(22) NOT NULL,
    birth_date DATE NOT NULL,
    join_date DATE NOT NULL DEFAULT CURRENT_DATE,
    bio TEXT DEFAULT 'I am a user of this piece of shit'
);

CREATE TABLE IF NOT EXISTS Subscription (
    id SERIAL PRIMARY KEY,
    following_user_id INT NOT NULL,
    followed_user_id INT NOT NULL,
    FOREIGN KEY (following_user_id) REFERENCES UserProfile(id) ON DELETE CASCADE,
    FOREIGN KEY (followed_user_id) REFERENCES UserProfile(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Post (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INT NOT NULL,
    posted_time TIMESTAMPTZ DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES UserProfile(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "Like" (
    id SERIAL PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES UserProfile(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES Post(id) ON DELETE CASCADE,
    UNIQUE (post_id, user_id)
);

CREATE TABLE IF NOT EXISTS Chat (
    id SERIAL PRIMARY KEY,
    id_user1 INT NOT NULL,
    id_user2 INT NOT NULL,
    FOREIGN KEY (id_user1) REFERENCES UserProfile(id) ON DELETE CASCADE,
    FOREIGN KEY (id_user2) REFERENCES UserProfile(id) ON DELETE CASCADE,
    UNIQUE (id_user1, id_user2)
);

CREATE TABLE IF NOT EXISTS ChatMessage (
    id SERIAL PRIMARY KEY,
    chat_id INT NOT NULL,
    user_id INT NOT NULL,
    replied_message_id INT,
    content TEXT,
    send_time TIMESTAMPTZ DEFAULT NOW(),
    FOREIGN KEY (chat_id) REFERENCES Chat(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES UserProfile(id),
    FOREIGN KEY (replied_message_id) REFERENCES ChatMessage(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Blocked (
    id SERIAL PRIMARY KEY,
    blocker_user_id INT NOT NULL,
    blocked_user_id INT NOT NULL,
    FOREIGN KEY (blocker_user_id) REFERENCES UserProfile(id),
    FOREIGN KEY (blocked_user_id) REFERENCES UserProfile(id),
    UNIQUE (blocker_user_id, blocked_user_id)
);
