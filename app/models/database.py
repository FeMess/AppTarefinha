import sqlite3

class ManagementSystemDatabase:
    def __init__(self, db_name = 'tasks.db'):
        self.db_name = db_name

    def initialize_db(self):
        return sqlite3.connect(self.db_name) 
    
    def create_table_tasks(self): 
        with self.initialize_db() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    TaskName TEXT,
                    Status TEXT DEFAULT 'Pendente'
                )  
                """)
            
            connection.commit()

    def create_task(self, task_name):
        with self.initialize_db() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO tasks (TaskName, Status) VALUES (?, ?)
                """,
                (task_name, 'Pendente')
            )

            connection.commit()
        
    def remove_task(self, task_ID):
        with self.initialize_db() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM tasks WHERE ID = ?
                """,
                (task_ID,)
            )

            connection.commit()

    def get_task(self, task_ID = '*'):
        with self.initialize_db() as connection:
            cursor = connection.cursor()

            if task_ID == '*':
                cursor.execute(
                    """
                    SELECT * FROM tasks
                    """
                    )
            else:
                cursor.execute(
                    """
                    SELECT * FROM tasks WHERE ID = ?
                    """,
                    (task_ID,)
                    )
            
            list_result = cursor.fetchall()
            return list_result
            
    def update_task(self, task_ID, task_name, task_status):
        with self.initialize_db() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE tasks SET TaskName = ?, Status = ? WHERE ID = ?
                """,
                (task_name, task_status, task_ID)
                )
        
            connection.commit()