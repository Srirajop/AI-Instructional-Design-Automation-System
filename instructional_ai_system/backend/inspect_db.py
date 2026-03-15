from sqlalchemy import create_engine, inspect

engine = create_engine('mysql+pymysql://root:@localhost:3306/storyboard_db')
inspector = inspect(engine)

with open('schema_out.txt', 'w', encoding='utf-8') as f:
    f.write(f"Tables: {inspector.get_table_names()}\n")

    if 'projects' in inspector.get_table_names():
        f.write("\nProjects columns:\n")
        for col in inspector.get_columns('projects'):
            f.write(f"  {col['name']}: {col['type']}\n")

    if 'users' in inspector.get_table_names():
        f.write("\nUsers columns:\n")
        for col in inspector.get_columns('users'):
            f.write(f"  {col['name']}: {col['type']}\n")

    if 'chat_messages' in inspector.get_table_names():
        f.write("\nChatMessages columns:\n")
        for col in inspector.get_columns('chat_messages'):
            f.write(f"  {col['name']}: {col['type']}\n")
