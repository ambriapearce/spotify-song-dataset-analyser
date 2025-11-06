# Function for genre analysis

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def genre():
    """
    Connection to Database is made, then closed once carring out the rest of the function.
    Libaries are local variables to make it simple for analysis. 
    This function will take the users input (integer) and will produce a DataFrame as well as visual statistics.
    """


    conn = sqlite3.connect('CWDatabase.db')
    year = input("\nEnter a year between 1998 & 2020 for your analyis of genres: ")
    
    try:
        year = int(year)
        if year < 1998 or year > 2020:
            print("You must enter a year between 1998 & 2020.")
            return
    except ValueError:
        print("Error. Please enter a number.")
        return
 
    
    query = """
    SELECT Genre.Genre, ROUND(AVG(Song.Danceability), 2) AS "Average Danceability", 
    ROUND(AVG(Song.Popularity), 2) AS "Average Popularity", ROUND(AVG(Song.Duration), 2) AS "Average Duration",
    COUNT(Song.ID) AS "Total Songs"
    FROM Song
    JOIN Genre ON Song.Genre_ID = Genre.ID
    WHERE Song.Year = :year
    GROUP BY Genre.Genre;
    """
    genre = pd.read_sql_query(query, conn, params= {"year": year})
    
    if genre.empty:
        print(f"No data found for {year}.")
        return

    print(f"Songs in {year}: ")
    print("\n") 
#View DataFrame
    print(genre.to_string(index = False))
    print("\n")
    print("\n")

# Visualisation: stats

    plt.figsize = (8,4)
    plt.style.use("classic")
    plt.figure(facecolor = "white")
    plt.pie(genre['Total Songs'], autopct ='%1.1f%%',
            wedgeprops = {"linewidth":2,"edgecolor":"white"})
    plt.title("Total Songs")
    plt.legend(genre['Genre'], loc = "upper right")
    plt.show()
   
    conn.close()


if __name__ == "__main__":
    genre()


""" Reference:
Description: Pandas DataFrame.to_string
Author: Geeks for Geeks
Date: 12/01/2024
URL: https://www.geeksforgeeks.org/python-pandas-dataframe-to_string/
"""
