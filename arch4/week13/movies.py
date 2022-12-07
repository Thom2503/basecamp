'''
Columns of table 'movies': id,title,director,genre,year
'''
import sqlite3

# create connection to existing database ('movies_example.db')
con = sqlite3.connect("movies_example.db")
cur = con.cursor()

# # Print all movies
# cur.execute("SELECT * FROM `movies`")
# print(cur.fetchall())

# # Print all movies that were released in '2019'
# cur.execute("SELECT * FROM `movies` WHERE `year` = 2019")
# print(cur.fetchall())

# # Print all movies from which the title starts with 'Spider-Man'
# cur.execute("SELECT * FROM `movies` WHERE `title` LIKE '%Spider-Man%'")
# print(cur.fetchall())

# # Print all movies that belong to the genre 'Action' or 'Drama'
# cur.execute("SELECT * FROM `movies` WHERE `genre` = 'Action' OR `genre` = 'Drama'")
# print(cur.fetchall())

# # Print (with one query) all movies directed by 'Jon Watts' and released after '2019'
# cur.execute("SELECT * FROM `movies` WHERE `director` = 'Jon Watts' and `year` > 2019")
# print(cur.fetchall())

# Add the following movie:
# title: 'Black Adam', director: 'Jaume Collet-Serra', genre: 'Action', year: '2022'
cur.execute("INSERT INTO `movies` VALUES (NULL, ?, ?, ?, ?)", ('Black Adam', 'James Collet-Serra', 'Action', 2022))

# Change all movies directed by the 'Russo brothers' to 'Anthony and Joseph Russo'
cur.execute("UPDATE `movies` SET `director` = 'Antony and Joseph Russo' WHERE `director` = 'Russo Brothers'")

# Remove all movies that were release in '2017'
cur.execute("DELETE FROM `movies` WHERE `year` = 2017")

# Print again all movies
result = cur.execute("SELECT * FROM `movies`").fetchall()
for row in result:
    print(row)

# commit the changes to db
con.commit()

# close the connection
con.close()
