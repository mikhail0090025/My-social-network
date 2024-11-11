import asyncpg
import asyncio
import os
from pathlib import Path

async def create_connection():
    try:
        connection = await asyncpg.connect(
            user='postgres',
            password='1111',
            database='my_social_network',
            host='localhost',
            port='5432'
        )
        print("Connection to the database established successfully.")
        return connection

    except Exception as e:
        print(f"Error: {e}")
        raise

def execute_query_sync(query, *args):
    async def execute_query():
        # Создаем соединение с базой данных
        conn = await create_connection()
        if conn is None:
            print("Failed to create a database connection.")
            return None

        try:
            # Выполняем SQL-запрос и получаем результат
            result = await conn.fetch(query, *args)
            return result

        except Exception as e:
            raise e

        finally:
            # Закрываем соединение
            await conn.close()
    
    return asyncio.run(execute_query())

def create_db_if_not_exists():
    sql_file_path = os.path.join(Path(__file__).resolve().parent.parent, 'sql', 'create_if_not_exists.sql')
    print(sql_file_path)
    with open(sql_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        commands = split_queries(content)
        for command in commands:
            execute_query_sync(command)

# For big SQL scripts
def split_queries(sql_code, each_line_new_command = False):
    splitter = '\n\n'
    if each_line_new_command:
        splitter = '\n'
    queries = [query.strip() for query in sql_code.strip().split(splitter)]
    return queries

create_db_if_not_exists()