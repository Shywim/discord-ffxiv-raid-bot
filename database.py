import sqlite3
from sqlite3 import Error
from datetime import datetime
from tqdm import tqdm

COLUMNS = ["discord_id", "character_name", "jobs", "num_raids"]
TANKS = ["WAR", "PLD", "DRK", "GNB"]
HEALERS = ["WHM", "SCH", "AST"]
MELEES = ["MNK", "DRG", "NIN", "SAM"]
RANGED = ["BRD", "MCH", "DNC"]
CASTERS = ["BLM", "SMN", "RDM"]
LIMITED = ["BLU"]
DPS = [*MELEES, *RANGED, *CASTERS]
JOBS = [*TANKS, *HEALERS, *DPS]


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    # finally:
    #     if conn:
        #         conn.close()
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_player(conn, player):
    """
    Create a new player into the player table
    :param conn:
    :param player:
    :return: player id
    """
    sql = ''' INSERT INTO player(discord_id,character_name,jobs,signup_date,num_raids)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, player)
    conn.commit()
    return cur.lastrowid


def update_player(conn, field, value, discord_id: int, character_name: str):
    """
    update character_name, jobs, num_raids of a character
    :param conn:
    :param field:
    :return: discord id
    """
    if field in COLUMNS:
        sql = f''' UPDATE player
                   SET {field} = ?
                   WHERE discord_id = ?
                   AND character_name = ?'''
        cur = conn.cursor()
        cur.execute(sql, (value, discord_id, character_name))
        conn.commit()
    else:
        print(f"{field} not in database columns")


def update_jobs(conn, job_list, discord_id, character_name):
    update_player(conn, "jobs", job_list, discord_id, character_name)


if __name__ == '__main__':

    sql_create_player_table = """ CREATE TABLE IF NOT EXISTS player (
                                        id integer PRIMARY KEY,
                                        discord_id integer NOT NULL,
                                        character_name text NOT NULL,
                                        jobs text,
                                        signup_date text,
                                        num_raids integer
                                    ); """

    conn = create_connection(r"database/test.db")

    # create tables
    with conn:
        # create Player table
        create_table(conn, sql_create_player_table)

        # create a new Player
        for i in tqdm(range(100)):
            player = (1234567890 + i, "Nama Zu", "PLD,DNC,SAM,MCH", datetime.today().strftime('%Y-%m-%d'), 0)
            create_player(conn, player)

        # update player
        update_player(conn, "character_name", "Na Mazu", 1234567904, "Nama Zu")
        update_player(conn, "jobs", "SAM", 1234567904, "Na Mazu")
        update_player(conn, "num_raids", 10, 1234567904, "Na Mazu")
