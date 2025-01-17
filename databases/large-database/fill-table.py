import psycopg2
from faker import Faker
import random

# Database connection parameters
DB_NAME = "large_database"
DB_USER = "deps-postgres"
DB_PASSWORD = "deps-postgres-password"
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Initialize Faker
fake = Faker()

# Function to generate and insert users
def insert_users(num_users):
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        cur.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s)",
            (username, email)
        )
    conn.commit()

# Function to generate and insert user relations
def insert_user_relations(num_relations, num_users):
    relation_types = ['friend', 'follower', 'colleague', 'family']
    for _ in range(num_relations):
        user_id = random.randint(1, num_users)
        related_user_id = random.randint(1, num_users)
        while related_user_id == user_id:
            related_user_id = random.randint(1, num_users)
        relation_type = random.choice(relation_types)
        cur.execute(
            "INSERT INTO user_relations (user_id, related_user_id, relation_type) VALUES (%s, %s, %s)",
            (user_id, related_user_id, relation_type)
        )
    conn.commit()

# Insert data
num_users = 1_0_000
num_relations = 1_000

insert_users(num_users)
insert_user_relations(num_relations, num_users)

# Close the database connection
cur.close()
conn.close()
