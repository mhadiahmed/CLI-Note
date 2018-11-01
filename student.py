from peewee import *

db = SqliteDatabase('student.db')

class Student(Model):
	name = CharField(max_length=255,unique=True)
	points = IntegerField(default=0)
	
	class Meta:
		database = db

### create() save() delete_instance() get() select()

students = [
	{'name':'mahdi','points':853},
	{'name':'ali','points':258},
	{'name':'ahmed','points':852},
	{'name':'jon','points':159},
	{'name':'snow','points':357},
]

def add_data():
	for student in students:
		try:
			Student.create(name=student['name'],
					   points=student['points'])
		except IntegrityError:
			record = Student.get(name=student['name'])
			record.points = student['points']
			record.save()

def get_data():
	student = Student.select().order_by(Student.points.desc()).get()
	
	#for std in student:
	#	print(std.name , std.points)
	return student	
		

if __name__ == "__main__":
	db.connect()
	db.create_tables([Student],safe=True)
	add_data()
	print("Our top student degree {0.name}".format(get_data()))
