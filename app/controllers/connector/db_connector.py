import psycopg2

conn_params = {
    "host": "ep-aged-recipe-a2f1iyj1.eu-central-1.aws.neon.tech",
    "database": "DB_Zlagoda",
    "user": "DB_Zlagoda_owner",
    "password": "85rkPbEFmuDM"
}


def get_connection():
    return psycopg2.connect(
        dbname="DB_Zlagoda",
        user="DB_Zlagoda_owner",
        password="85rkPbEFmuDM",
        host="ep-aged-recipe-a2f1iyj1.eu-central-1.aws.neon.tech"
    )
