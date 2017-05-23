import sqlite3

# Connecting to the database file
conn = sqlite3.connect("database/" + "movies.db")
c = conn.cursor()


# Create table
c.execute('''CREATE TABLE IF NOT EXISTS Movies
            (Name VARCHAR (45) NOT NULL, Image VARCHAR (45) NOT NULL, Mood VARCHAR (45) NOT NULL)''')


# inserts the results which are stored in the list at that moment in time (Change when adding new city)
def insertinto(movie):
    c.execute("INSERT INTO Movies VALUES (?,?,?)", movie)
    print('commited')
    conn.commit()

list1 = ["The Intern", "/static/theintern.jpg", "calm"]

insertinto(list1)

# fetches whats in the database
#c.execute('select * from Motions')
#for fetch in c.fetchall():
    #print(fetch)
