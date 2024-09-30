import sqlite3

def get_db():
    db = sqlite3.connect('task_manager.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

if __name__ == '__main__':
    init_db()