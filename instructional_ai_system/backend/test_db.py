from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:@localhost:3306/storyboard_db')
Session = sessionmaker(bind=engine)
session = Session()

# Import project Model
import sys
sys.path.append('d:/Downloads/StoryBoardAI/instructional_ai_system/backend')
from app import models

result = session.query(models.Project).order_by(models.Project.updated_at.desc()).first()
if result:
    print(f'Project ID: {result.id} - Title: {result.title}')
    doc = result.design_doc
    if doc:
        print('--- DESIGN DOC START ---')
        lines = doc.splitlines()
        for i, line in enumerate(lines[:30]):
            print(f'{i}: {line}')
        print('--- DESIGN DOC END ---')
    else:
        print('No design doc')
