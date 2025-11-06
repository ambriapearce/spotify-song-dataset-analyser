import pandas as pd
import sqlite3
import matplotlib.pyplot as plt



# Function for artist analysis

class Artist:
    def __init__(self,database):
        self.database = database
        self.conn = sqlite3.connect(self.database)


    def close_db(self):
         if self.conn:
             self.conn.close()

    def artist(self, name):
       
        queries = """
        SELECT Genre.Genre, ROUND(AVG(Song.Popularity), 1) AS Popularity,
        (SELECT ROUND(AVG(Popularity), 1) FROM Song WHERE Genre.ID = Song.Genre_ID) AS Overall
        FROM Song
        JOIN Genre ON Song.Genre_ID = Genre.ID
        JOIN Artist ON Song.Artist_ID = Artist.ID
        WHERE Artist.Artist_Name = :name
        GROUP BY Genre.Genre;
        """
        artistdf = pd.read_sql_query(queries, self.conn, params = {"name":name})
       
        if artistdf.empty:
            print(f"Sorry no data found for {name}.")
            return
           
        print(f"Popularity for {name}: ")
        print("\n")
        print(artistdf.to_string(index = False))
        print("\n")

        # Visualisation 
        artistdf.plot(x = "Genre", y = ['Popularity', 'Overall'], kind ='bar', color =["orange", "purple"], width = 0.3)
        plt.gcf().set_facecolor("white")
        plt.title(f"Popularity of {name} by Genres")
        plt.ylabel('Popularity')
        plt.xlabel(' ')
        plt.xticks(rotation = 45)
        plt.legend()
        plt.tight_layout()
        plt.show()
    


""" Reference:
Description: Pandas DataFrame.to_string
Author: Geeks for Geeks
Date: 12/01/2024
URL: https://www.geeksforgeeks.org/python-pandas-dataframe-to_string/
"""