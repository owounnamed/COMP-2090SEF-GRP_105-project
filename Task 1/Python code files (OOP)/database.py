import os
import sqlite3
from utils import DB_NAME, IMAGE_FOLDER
from models import Restaurant


class DatabaseManager:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

        if not os.path.exists(IMAGE_FOLDER):
            os.makedirs(IMAGE_FOLDER)

        self.initialize_database()

    def connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize_database(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                area TEXT NOT NULL,
                cuisine TEXT NOT NULL,
                price_level INTEGER NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                restaurant_id INTEGER,
                username TEXT,
                rating REAL,
                comment TEXT,
                image_path TEXT,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS deleted_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_review_id INTEGER,
                restaurant_name TEXT,
                username TEXT,
                rating REAL,
                comment TEXT,
                image_path TEXT,
                delete_reason TEXT
            )
            """
        )

        # Add image_path column if old database does not have it.
        cursor.execute("PRAGMA table_info(reviews)")
        columns = cursor.fetchall()
        column_names = []
        for row in columns:
            column_names.append(row[1])

        if "image_path" not in column_names:
            cursor.execute("ALTER TABLE reviews ADD COLUMN image_path TEXT")

        conn.commit()
        conn.close()

        self.seed_data()

    def seed_data(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM restaurants")
        count = cursor.fetchone()[0]

        if count == 0:
            sample_restaurants = [
                ("Mong Kok Noodle House", "Mong Kok", "Chinese", 60, 22.3193, 114.1700),
                ("Ho Man Tin Cafe", "Ho Man Tin", "Cafe", 80, 22.3171, 114.1808),
                ("Kowloon Sushi", "Mong Kok", "Japanese", 150, 22.3185, 114.1688),
                ("Budget Thai Corner", "Ho Man Tin", "Thai", 70, 22.3162, 114.1819),
                ("BBQ Express", "Mong Kok", "Korean", 120, 22.3210, 114.1721),
                ("Campus Western Bites", "Ho Man Tin", "Western", 95, 22.3178, 114.1799)
            ]

            cursor.executemany(
                "INSERT INTO restaurants (name, area, cuisine, price_level, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
                sample_restaurants
            )
            conn.commit()

        conn.close()

    def add_restaurant(self, name, area, cuisine, price_level, latitude, longitude):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO restaurants (name, area, cuisine, price_level, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
            (name, area, cuisine, price_level, latitude, longitude)
        )
        conn.commit()
        conn.close()

    def update_restaurant(self, restaurant_id, name, area, cuisine, price_level, latitude, longitude):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE restaurants
            SET name=?, area=?, cuisine=?, price_level=?, latitude=?, longitude=?
            WHERE id=?
            """,
            (name, area, cuisine, price_level, latitude, longitude, restaurant_id)
        )
        conn.commit()
        conn.close()

    def delete_restaurant(self, restaurant_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM restaurants WHERE id=?", (restaurant_id,))
        conn.commit()
        conn.close()

    def add_review(self, review):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (restaurant_id, username, rating, comment, image_path) VALUES (?, ?, ?, ?, ?)",
            (review.restaurant_id, review.username, review.rating, review.comment, review.image_path)
        )
        conn.commit()
        conn.close()

    def delete_review(self, review_id, delete_reason=""):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT rv.id, r.name, rv.username, rv.rating, rv.comment, rv.image_path
            FROM reviews rv
            JOIN restaurants r ON rv.restaurant_id = r.id
            WHERE rv.id=?
            """,
            (review_id,)
        )
        row = cursor.fetchone()

        if row is not None:
            cursor.execute(
                """
                INSERT INTO deleted_reviews
                (original_review_id, restaurant_name, username, rating, comment, image_path, delete_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (row[0], row[1], row[2], row[3], row[4], row[5], delete_reason)
            )

        cursor.execute("DELETE FROM reviews WHERE id=?", (review_id,))
        conn.commit()
        conn.close()

    def get_restaurants(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT r.id, r.name, r.area, r.cuisine, r.price_level, r.latitude, r.longitude,
                   IFNULL(AVG(rv.rating), 0) AS avg_rating
            FROM restaurants r
            LEFT JOIN reviews rv ON r.id = rv.restaurant_id
            GROUP BY r.id, r.name, r.area, r.cuisine, r.price_level, r.latitude, r.longitude
            """
        )
        rows = cursor.fetchall()
        conn.close()

        restaurant_list = []
        for row in rows:
            restaurant_list.append(Restaurant(*row))
        return restaurant_list

    def get_reviews_by_restaurant(self, restaurant_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, restaurant_id, username, rating, comment, image_path FROM reviews WHERE restaurant_id=? ORDER BY id DESC",
            (restaurant_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_all_reviews(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT rv.id, r.name, rv.username, rv.rating, rv.comment, rv.image_path
            FROM reviews rv
            JOIN restaurants r ON rv.restaurant_id = r.id
            ORDER BY rv.id DESC
            """
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_deleted_reviews(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, original_review_id, restaurant_name, username, rating, comment, image_path, delete_reason
            FROM deleted_reviews
            ORDER BY id DESC
            """
        )
        rows = cursor.fetchall()
        conn.close()
        return rows
