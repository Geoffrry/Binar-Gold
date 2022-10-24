def Generate(filePath):

    from pathlib import Path
    import sqlite3
    import pandas as pd

    Path('data.db').touch()
    print('Database Created Succesfully')

    conn = sqlite3.connect('data.db', check_same_thread=False)

    try :
        conn.execute(''' DROP TABLE data''')
        conn.execute(''' DROP TABLE slangwords''')
        conn.execute(''' DROP TABLE stopwords''')
    # Create a Table with the appropriate Columns
    except :
         conn.execute(''' CREATE TABLE data (tweet varchar(280))''') # For the main data
         conn.execute(''' CREATE TABLE slangwords (alay varchar(255), normal varchar(255)) ''') 
         conn.execute(''' CREATE TABLE stopwords (kata varchar(255))''')
    # Same but this will be executed when the try function raise no exception
    else :
          conn.execute(''' CREATE TABLE data (tweet varchar(280))''') # For the main data
          conn.execute(''' CREATE TABLE slangwords (alay varchar(255), normal varchar(255)) ''') 
          conn.execute(''' CREATE TABLE stopwords (kata varchar(255))''')
    finally:
         print('Table Created Succesfully')

    df = pd.read_csv(filePath, encoding = 'latin-1')
    df = df.drop_duplicates()
    df.to_sql('data', conn, if_exists = 'replace', index = False)

    df1 = pd.read_csv('csv/kamusalay.csv', names = ['alay', 'normal'], encoding = 'latin-1', header = None)
    df1.to_sql('slangwords', conn, if_exists = 'replace', index = False)

    df2 = pd.read_csv('csv/stopwordbahasa.csv', names = ['kata'], encoding = 'latin-1', header = None)
    df2.to_sql('stopwords', conn, if_exists = 'replace', index = False)

    conn.commit()
    conn.close()