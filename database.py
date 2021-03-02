import sqlite3
import pandas as pd
from sqlalchemy import create_engine


def create_database(theory,pracs,sem):
    cleandf=theory
    pracsdf=pracs
    Semester=sem
    #con = sqlite3.connect('Sem_Results.db')
    engine = create_engine('sqlite:///Sem_Results.db', echo=False)
    cleandf.to_sql(f'Sem_{Semester}_theory_results',engine,if_exists='replace',index=False)
    pracsdf.to_sql(f'Sem_{Semester}_pracs_results',engine,if_exists='replace',index=False)

def query_execute(query):
    con = sqlite3.connect('Sem_Results.db')
    c = con.cursor()
    result=c.execute(query)
    names = list(map(lambda x: x[0], c.description))
    df=pd.DataFrame(result)
    df.columns=names
    return df







