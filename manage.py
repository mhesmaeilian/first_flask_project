from firstproject import myapp , db
from flask_script import Manager

manager=Manager(myapp)

@manager.command
def init():
    db.create_all()
    print('database created successfuly')

if __name__=="__main__":
    manager.run()
