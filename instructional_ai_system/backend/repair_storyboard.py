import sys
sys.path.append('d:/Downloads/StoryBoardAI/instructional_ai_system/backend')
from app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:@localhost:3306/storyboard_db')
Session = sessionmaker(bind=engine)
session = Session()

project = session.query(models.Project).order_by(models.Project.updated_at.desc()).first()
if project:
    sb = project.storyboard
    lines = sb.splitlines()
    new_lines = []
    fixed_count = 0
    for line in lines:
        sline = line.strip()
        if sline.startswith('|') and sline.endswith('|'):
            pipe_count = sline.count('|')
            if pipe_count > 4:
                # Potential corrupted row
                cells = [c.strip() for c in sline.split('|')]
                # cells[0] and cells[-1] are empty strings from split
                content = [c for c in cells if c]
                if len(content) == 3:
                    new_lines.append('| ' + ' | '.join(content) + ' |')
                    fixed_count += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    project.storyboard = '\n'.join(new_lines)
    session.commit()
    print(f'Storyboard repaired. Fixed {fixed_count} rows.')
else:
    print('No project found.')

session.close()
