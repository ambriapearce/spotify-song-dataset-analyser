# Function for top 5 artist analysis

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def top5():
    """
    The Database is connected to.
    This function will take 2 user inputs both being integers, which will 
    then show statistics based on the years the user inputed.
    Visual statistics are shown.
    Finnally, the connection to Database is closed.
    """
    
    conn = sqlite3.connect('CWDatabase.db')
    
    start = input("Please choose a year between 1998 and 2020: ")
    end = input("Please choose an end year between 1998 and 2020: ")
    
    
    try:
        start, end = int(start), int(end)
        if start < 1998 or end > 2020 or start > end:
            print("Sorry must be between 1998 and 2020.")
            return
    except ValueError:
        print("Error. Please enter a valid year.")
        return

    query = """
    SELECT Artist.Artist_Name AS "Artist", Song.Year As "Year",
    (COUNT(Song.ID) * 0.3 + AVG(Song.Popularity) * 0.7) AS "Rank",
    AVG(Song.Popularity) AS "Average",
    COUNT(Song.ID) AS "Total Songs"
    FROM Song
    JOIN Artist ON Song.Artist_ID = Artist.ID
    WHERE Song.Year BETWEEN :start AND :end
    GROUP BY Artist.Artist_Name
    ORDER BY "Rank" DESC
    LIMIT 5;
    """
   
    topdf = pd.read_sql_query(query, conn, params = {"start": start, "end": end})
   
    
    print(f"Top Artists ({start}–{end}): ")
    print("\n")
# View DataFrame
    print(topdf.to_string(index = False))
    print("\n")

# Visualisation: stats
    topdf.plot(x = "Artist", y = ['Average', 'Rank'], kind = 'line', marker = 'x', color = ["blue", "red"])
    plt.gcf().set_facecolor("white")
    plt.title("Top Artists")
    plt.xlabel('Artist')
    plt.xticks(rotation = 45)
    plt.legend()
    plt.show()
    
    conn.close()

if __name__ == "__main__":
    top5()

""" Reference:
Description: Pandas DataFrame.to_string
Author: Geeks for Geeks
Date: 12/01/2024
URL: https://www.geeksforgeeks.org/python-pandas-dataframe-to_string/
"""