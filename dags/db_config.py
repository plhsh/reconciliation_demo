from sqlalchemy import create_engine


def get_engine():
    return create_engine('postgresql://my_custom_user:my_secure_password@my_custom_postgres:5432/my_custom_db')


