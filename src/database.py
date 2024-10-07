import sqlite3
import instaloader


# Create sqlite table
def create_table() -> None:
    """
    Creates SQLite tables for user profiles and posts in the 'instagram_data.db' database.

    This function establishes a connection to the database, creates the necessary tables,
    and commits the changes.
    """
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()

    # create table for user profile
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profile (
        id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        biography TEXT,
        followers INTEGER,
        followees INTEGER,
        is_private BOOLEAN,
        is_verified BOOLEAN
    )
    ''')

    # create table for posts 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        profile_id INTEGER,
        shortcode TEXT,
        caption TEXT,
        likes INTEGER,
        comments INTEGER,
        date_utc TIMESTAMP,
        FOREIGN KEY(profile_id) REFERENCES Profile(id) ON DELETE CASCADE ON UPDATE CASCADE
    )
    ''')

    conn.commit()
    conn.close()


# inser data into user profile table
def insert_user_profile_table(profile: instaloader.Profile) -> None:
    """
    Inserts user profile data into the 'user_profile' table in the 'instagram_data.db' database.

    Args:
        profile (instaloader.Profile): profile (instaloader.Profile): The Instagram user profile object.
    """
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO user_profile (username, full_name, biography, followers, followees, is_private, is_verified)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (profile.username, profile.full_name, profile.biography, profile.followers, profile.followees, profile.is_private, profile.is_verified))
    
    conn.commit()
    conn.close()

    print("Successfully insert user profile into database!")


# insert data into post table
def insert_post_table(profile: instaloader.Profile) -> None:
    """
    Inserts user's Instagram posts into the 'posts' table in the SQLite database.

    Args:
        profile (instaloader.Profile): The Instagram user profile object.
    """
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()
    
    # query the corresponding user profile id to store the posts
    cursor.execute(f'SELECT id FROM user_profile WHERE username = ?', (profile.username,))
    rows = cursor.fetchone()
    profile_id = rows[0]

    # query the last id of previous stored user profile id to determine the starting and ending id of new added 10 posts
    if profile_id > 1:
        cursor.execute(f'SELECT id FROM posts WHERE id = (SELECT MAX(id) FROM posts WHERE profile_id = ?)', (profile_id-1, ))
        rows = cursor.fetchone()
        last_post_id = rows[0]
    else:
        last_post_id = 0

    for post in profile.get_posts():
        cursor.execute('''
        INSERT INTO Posts (profile_id, shortcode, caption, likes, comments, date_utc)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (profile_id, post.shortcode, post.caption, post.likes, post.comments, post.date_utc))

        if cursor.lastrowid >= last_post_id + 10:
            break

    conn.commit()
    conn.close()

    print("Successfully insert uesr's posts into database!\n")


def retrieve_data(profile: instaloader.Profile) -> tuple[list[str], list[str]]:
    """
    Retrieves user biography and post captions for personality trait prediction.

    Args:
        profile (instaloader.Profile): The Instagram user profile object.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing two lists:
            - The first list contains user biographies (strings).
            - The second list contains post captions (strings).
    """
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()
    
    # retrive biography from user_profile table
    cursor.execute(f'SELECT biography FROM user_profile WHERE username = ?',  (profile.username,))
    bio_rows = cursor.fetchall()

    # retrive caption from posts table
    cursor.execute(f'SELECT caption FROM posts WHERE profile_id = (SELECT id FROM user_profile WHERE username = ?)', (profile.username,))
    caption_rows = cursor.fetchall()

    conn.commit()
    conn.close()

    return bio_rows, caption_rows


def print_all_username() -> None:
    """
    Prints all Instagram usernames stored in the 'user_profile' table of the SQLite database.
    """
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT username from user_profile')
    rows = cursor.fetchall()

    conn.commit()
    conn.close()

    if rows:
        for row in rows:
            print(row[0])    
        print()
    else:
        print("No user found in the database! \n")


# check if the input Instagarm user is stored in the database
def is_in_the_database(username: str) -> bool:
    """
    Checks if the input Instagram username is stored in the 'user_profile' table of the SQLite database.

    Args:
        username (str): The Instagram username to check.

    Returns:
        bool: True if the username is found in the database, False otherwise.
    """
    conn = sqlite3.connect('instagram_data.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT username from user_profile WHERE username = ?', (username,))
    rows = cursor.fetchone()

    conn.commit()
    conn.close()

    for row in rows:
        if row == username:
            return True
        else:
            return False

