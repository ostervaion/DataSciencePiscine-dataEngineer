import glob
import os
import sys
import psycopg2

# Database Connection Settings
DB_CONFIG = {
    "host": "localhost",
    "database": "piscineds",
    "user": "juetxeba",
    "password": "mysecretpassword",
    "port": 5432,
}

# Path to directory containing the CSV files
CUSTOMER_DIR = os.path.abspath("../../subject/customer/")


def import_csv_files():
    conn = None
    try:
        # 1. Establish Database Connection
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("Connected to PostgreSQL successfully.")

        # 2. Create Schema
        cursor.execute('CREATE SCHEMA IF NOT EXISTS "automatic_table";')

        # 4. Find all CSV files in the directory
        csv_files = sorted(glob.glob(os.path.join(CUSTOMER_DIR, "*.csv")))

        if not csv_files:
            print(f"No CSV files found in {CUSTOMER_DIR}")
            return

        # 5. Loop through and import each CSV file
        copy_sql = """
        COPY "automatic_table".data_2022_oct 
        FROM STDIN 
        WITH (FORMAT csv, HEADER true);
        """

        for csv_file in csv_files:
            print(f"Importing {os.path.basename(csv_file)}...")
            with open(csv_file, "r", encoding="utf-8") as f:
                cursor.copy_expert(sql=copy_sql, file=f)

        # Commit all changes at once
        conn.commit()
        print("All CSV files imported successfully!")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        if conn:
            conn.rollback()  # Rollback changes if any file fails
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    import_csv_files()
