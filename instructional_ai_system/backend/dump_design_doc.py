from sqlalchemy import create_engine, text

engine = create_engine('mysql+pymysql://root:@localhost:3306/storyboard_db')

with engine.connect() as conn:
    # Get the latest project with a design doc
    result = conn.execute(text("SELECT design_doc FROM projects WHERE design_doc IS NOT NULL ORDER BY id DESC LIMIT 1"))
    row = result.fetchone()
    if row:
        with open('sample_design_doc.md', 'w', encoding='utf-8') as f:
            f.write(row[0])
        print("Done: sample_design_doc.md created")
    else:
        print("No design doc found")
