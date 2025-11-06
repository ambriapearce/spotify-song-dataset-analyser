# Load the libraries
import pandas as pd
import sqlite3

class Preprocessing:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.dfOriginal = None
        self.dfSongs = None 

    
    def load(self):
        """ 
        The data from the CSV file is loaded into a pandas 
        DataFrame named dfSongs.
        """
        self.dfOriginal = pd.read_csv(self.csv_file)
        # A copy of the data is saved to dfSongs
        self.dfSongs = self.dfOriginal.copy() 

    

    def clean(self):
        """ 
        The original data is cleaned by the following process:
        - Missing values are checked and handled.
        - Duplicates are checked and removed.
        - Columns are renamed.
        - Values are converted.
    
        Returns: The cleaned DataFrame
        """
        # Dropping missing values
        if self.dfSongs.isna().sum().sum()> 0:
            self.dfSongs = self.dfSongs.dropna()

        # Dropping duplicate rows
        if self.dfSongs.duplicated().sum().sum() > 0:
            self.dfSongs = self.dfSongs.drop_duplicates()

        # Rename column duration_ms to duration & convert duration
        self.dfSongs = self.dfSongs.rename(columns={'duration_ms': 'duration'})
        self.dfSongs['duration'] = (self.dfSongs['duration'] / 1000).round()

    
    def filter(self):
        """
        Filters are applied to the cleaned DataFrame:
        - Songs popularity value >= 50
        - Songs Danceability values > 2.0 
        - Speechiness values
        > 0.33 & < 0.66

        Returns: The filtered DataFrame
        """
          
        self.dfSongs = self.dfSongs[
        (self.dfSongs['popularity'] > 50) & 
        (self.dfSongs['danceability'] > 0.2) &
        (self.dfSongs['speechiness'] >= 0.33) &
        (self.dfSongs['speechiness'] <= 0.66)
        ]

    
    def sqlite_table(self):
        """ 
        Creates an sqlite database.
        """
        # Creating sqlite Database
        conn = sqlite3.connect("CWDatabase.db")
        try:
            c = conn.cursor()

            c.execute("DROP TABLE IF EXISTS Song")
            
            c.execute("""
            CREATE TABLE IF NOT EXISTS Artist(
            ID INTEGER PRIMARY KEY,
            Artist_Name TEXT UNIQUE
            )""")
            
            c.execute("""
            CREATE TABLE IF NOT EXISTS Genre (
            ID INTEGER PRIMARY KEY,
            Genre TEXT UNIQUE
            )
            """)
            
            c.execute("""
            CREATE TABLE IF NOT EXISTS Song (
            ID INTEGER PRIMARY KEY,
            Song TEXT,
            Duration INTEGER,
            Explicit BOOLEAN, 
            Year INTEGER,
            Popularity INTEGER, 
            Danceability REAL,
            Speechiness REAL,
            Artist_ID INTEGER,
            Genre_ID INTEGER,
            FOREIGN KEY (Genre_ID) REFERENCES Genre(ID)
            FOREIGN KEY (Artist_ID) REFERENCES Artist(ID),
            UNIQUE (Song, Artist_ID)
            )
            """)

            conn.commit()
        finally:
            conn.close()



    
    def data_input(self):
        """ 
        Cleaned & filtered data in the sql DataBase inseted into the
        tables.
        """
        conn = sqlite3.connect("CWDatabase.db")
        try:
            c = conn.cursor()   

            for _, row in self.dfSongs.iterrows():
                c.execute("INSERT OR IGNORE INTO Artist (Artist_Name) VALUES (?)", (row['artist'],))
                c.execute("SELECT ID FROM Artist WHERE Artist_Name = ?", (row['artist'],))
                artist_id = c.fetchone()[0]

                genres = row['genre'].split(',')
                genre_ids = []
            
                for genre in genres:
                    c.execute("INSERT OR IGNORE INTO Genre (Genre) VALUES(?)", (genre.strip(),))
                    c.execute("SELECT ID FROM Genre WHERE Genre = ?", (genre.strip(),))
                    genre_ids.append(c.fetchone()[0])

                for genre_id in genre_ids:
                    c.execute("""
                    INSERT OR IGNORE INTO Song (Song, Duration, Explicit, Year,
                    Popularity, Danceability, Speechiness, Artist_ID,Genre_ID)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row['song'], row['duration'], row['explicit'],
                        row['year'], row['popularity'], row['danceability'],
                        row['speechiness'], artist_id, genre_id
                        ))
                   
                        
            conn.commit()
        finally:
            conn.close()
   


# to check programm  
p = Preprocessing('songs.csv')
p.load()
p.clean()
p.filter()
p.sqlite_table()
p.data_input()
            