import pymysql
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class SQLAgent:

    def __init__(self):
        pass

    def get_connection(self):
        return pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=3306
        )

# Execute SQL query, Return DataFrame
    def fetch_dataframe(self, query):
        try:
            conn = self.get_connection()
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            print("SQL Error:", e)
            return pd.DataFrame()

# Database Access Layer
    def get_city_summary(self):
        accidents = self.fetch_dataframe(
            "SELECT city, COUNT(*) total FROM accident_events GROUP BY city"
        )
        complaints = self.fetch_dataframe(
            "SELECT city, COUNT(*) total FROM nlp_complaints GROUP BY city"
        )
        crowd = self.fetch_dataframe(
            "SELECT city, COUNT(*) total FROM crowd_events WHERE severity='Overcrowded' GROUP BY city"
        )
        return {
            "accidents": accidents,
            "complaints": complaints,
            "crowd": crowd
        }

