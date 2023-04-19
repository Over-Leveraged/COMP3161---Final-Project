import mysql.connector
from faker import Faker
import random
import datetime
import string
from datetime import date, timedelta

# Connect to MySQL server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Student1.",
  database="course_system"
)

# Initialize Faker generator
faker = Faker()

cursor = mydb.cursor()

# Generate 50 admins and insert them into the Admin table
for i in range(50):
    ad_id = f'AD{i+1:03}'
    ad_name = faker.name()
    sql = f"INSERT INTO Admin (Ad_ID, Ad_Name) VALUES ('{ad_id}', '{ad_name}')"
    cursor.execute(sql)
    mydb.commit()

# Generate 100,000 students and insert them into the Student table
for k in range(100000):
    stu_id = f'STU{k+1:06}'
    stu_name = faker.name()
    courses_taken = random.randint(3, 6)
    sql = f"INSERT INTO Student (Stu_ID, Stu_Name, Courses_Taken) VALUES ('{stu_id}', '{stu_name}', {courses_taken})"
    cursor.execute(sql)
    mydb.commit()

# Generate 1000 lecturers and insert them into the Lecturer table
for j in range(1000):
    lec_id = f'LEC{j+1:06}'
    l_name = faker.name()
    courses_taught = random.randint(1, 5)
    sql = f"INSERT INTO Lecturer (Lec_ID, L_Name, Courses_Taught) VALUES ('{lec_id}', '{l_name}', {courses_taught})"
    cursor.execute(sql)
    mydb.commit()

# Select all lecturer IDs from the Lecturer table
cursor.execute("SELECT Lec_ID FROM Lecturer")
lecturer_ids = [row[0] for row in cursor.fetchall()]

# Generate 500 courses and insert them into the Course table
for x in range(500):
    c_id = x+1
    lec_id = random.choice(lecturer_ids)
    c_name = f'Course {x+1}'
    enrollment = random.randint(10, 500)
    sql = f"INSERT INTO Course (C_ID, Lec_ID, C_Name, Enrollment) VALUES ({c_id}, '{lec_id}', '{c_name}', {enrollment})"
    cursor.execute(sql)
    mydb.commit()


# Update the Courses_Taught column in the Lecturer table
cursor.execute(f"SELECT COUNT(*) FROM Course WHERE Lec_ID = '{lec_id}'")
num_courses = cursor.fetchone()[0]
cursor.execute(f"UPDATE Lecturer SET Courses_Taught = {num_courses} WHERE Lec_ID = '{lec_id}'")
mydb.commit()


# Generate passwords
def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for i in range(10))

# Create accounts for lecturers
cursor = mydb.cursor()
cursor.execute("SELECT Lec_ID, L_Name FROM Lecturer")
lecturers = cursor.fetchall()
for lec_id, l_name in lecturers:
    password = generate_password()
    name = f"{l_name}"
    type = "lecturer"
    sql = "INSERT INTO Account (U_ID, Password, Name, Type) VALUES (%s, %s, %s, %s)"
    values = (lec_id, password, name, type)
    cursor.execute(sql, values)
    mydb.commit()

# Create accounts for students
cursor.execute("SELECT Stu_ID, Stu_Name FROM Student")
students = cursor.fetchall()
for stu_id, stu_name in students:
    password = generate_password()
    name = f"{stu_name}"
    type = "student"
    sql = "INSERT INTO Account (U_ID, Password, Name, Type) VALUES (%s, %s, %s, %s)"
    values = (stu_id, password, name, type)
    cursor.execute(sql, values)
    mydb.commit()

# Create accounts for admins
cursor.execute("SELECT Ad_ID, Ad_Name FROM Admin")
admins = cursor.fetchall()
for ad_id, ad_name in admins:
    password = generate_password()
    name = f"{ad_name}"
    type = "admin"
    sql = "INSERT INTO Account (U_ID, Password, Name, Type) VALUES (%s, %s, %s, %s)"
    values = (ad_id, password, name, type)
    cursor.execute(sql, values)
    mydb.commit()

# Select all course IDs from the Course table
cursor.execute("SELECT C_ID FROM Course")
course_ids = [row[0] for row in cursor.fetchall()]

# Generate assignments for each course and insert them into the Assignments table
for c_id in course_ids:
    # Select the maximum A_ID value for this course
    cursor.execute(f"SELECT MAX(A_ID) FROM Assignments WHERE C_ID = {c_id}")
    max_a_id = cursor.fetchone()[0] or 0

    for m in range(5):
        a_id = max_a_id + m + 1
        due_date = datetime.date.today() + datetime.timedelta(days=random.randint(1, 30))
        sql = f"INSERT INTO Assignments (A_ID, C_ID, Due_Date) VALUES ({a_id}, {c_id}, '{due_date}')"
        cursor.execute(sql)
        mydb.commit()

# Get all assignment IDs and course IDs from the Assignments table
cursor.execute("SELECT A_ID, C_ID FROM Assignments")
assignments = cursor.fetchall()

# Get all student IDs from the Student table
cursor.execute("SELECT Stu_ID FROM Student")
student_ids = [row[0] for row in cursor.fetchall()]

# Insert grades for each assignment and student
for assignment in assignments:
    a_id, c_id = assignment
    cursor.execute(f"SELECT Enrollment FROM Course WHERE C_ID = {c_id}")
    enrollment = cursor.fetchone()[0]
    for n in range(enrollment):
        stu_id = random.choice(student_ids)
        grade = round(random.uniform(50, 100), 2)
        # Check if record already exists
        cursor.execute(f"SELECT * FROM Assignment_Grades WHERE A_ID = {a_id} AND C_ID = {c_id} AND Stu_ID = '{stu_id}'")
        result = cursor.fetchone()
        if result:
            print(f"Record already exists for A_ID={a_id}, C_ID={c_id}, and Stu_ID='{stu_id}'. Skipping insertion.")
        else:
            # Insert new record
            sql = f"INSERT INTO Assignment_Grades (A_ID, C_ID, Stu_ID, Grade) VALUES ({a_id}, {c_id}, '{stu_id}', {grade})"
            cursor.execute(sql)
    mydb.commit()


# Get all course IDs from the Course table
cursor.execute("SELECT C_ID FROM Course")
course_ids = [row[0] for row in cursor.fetchall()]

# Generate event dates and insert them into the Events table for each course
for c_id in course_ids:
    num_events = random.randint(1, 10)
    for i in range(num_events):
        event_id = i+1
        event_date = date.today() + timedelta(days=random.randint(1, 90))
        sql = f"INSERT INTO Events (Event_ID, C_ID, Dates) VALUES ({event_id}, {c_id}, '{event_date}')"
        cursor.execute(sql)
        mydb.commit()

# Define list of discussion topics
discussion_topics = [
    "Guest Speakers",
    "Peer Feedback",
    "Case Studies",
    "Reflections on Course Materials"
]

# Define list of discussion topics
topics = ["Course material", "Assignments", "Lectures", "Group projects", "Exams", "Textbook readings", "Online resources"]


# Get all course IDs from the Course table
cursor.execute("SELECT C_ID FROM Course")
course_ids = [row[0] for row in cursor.fetchall()]

# Generate discussion topics and insert them into the Discussion_Forums table for each course
for c_id in course_ids:
    num_topics = random.randint(1, 10)
    for i in range(num_topics):
        d_id = i+1
        d_topic = f'{random.choice(topics)} Discussion for Course {c_id}'
        sql = f"INSERT INTO Discussion_Forums (D_ID, C_ID, D_Topic) VALUES ({d_id}, {c_id}, '{d_topic}')"
        try:
            cursor.execute(sql)
            mydb.commit()
        except mysql.connector.IntegrityError:
            # Ignore any duplicates (i.e. topics with the same D_ID and C_ID)
            pass

thread_names = ["Introductions", "Guest Speakers", "Feedback and Suggestions", "Group Projects", "Case Studies", "Exam Preparation", "Course Material Questions", "Textbook Readings Discussion", "Online Resources Discussion", "Reflections on the Course"]


cursor.execute("SELECT D_ID FROM Discussion_Forums")
forum_ids = [row[0] for row in cursor.fetchall()]

# Generate discussion threads and insert them into the Discussion_Thread table for each forum
for f_id in forum_ids:
    num_threads = random.randint(1, len(thread_names))
    for g in range(num_threads):
        t_id = g+1
        t_name = thread_names[g]
        sql = f"INSERT INTO Discussion_Thread (Thread_ID, D_ID, T_Name) VALUES ({t_id}, {f_id}, '{t_name}') ON DUPLICATE KEY UPDATE T_Name = '{t_name}'"
        cursor.execute(sql)
        mydb.commit()


# Get all course IDs from the Course table
cursor.execute("SELECT C_ID FROM Course")
course_ids = [row[0] for row in cursor.fetchall()]

# Define a list of item names and types
item_names = ["Quiz", "Essay", "Presentation", "Midterm", "Final Exam"]
item_types = ["Assessment", "Assignment", "Exam"]

# Generate course items and insert them into the Course_Items table for each course
for c_id in course_ids:
    num_items = random.randint(2, 5)
    for c in range(num_items):
        item_id = c+1
        item_name = random.choice(item_names)
        item_type = random.choice(item_types)
        sql = f"INSERT INTO Course_Items (Item_ID, C_ID, Item_Name, Item_Type) VALUES ({item_id}, {c_id}, '{item_name}', '{item_type}')"
        cursor.execute(sql)
        mydb.commit()

# Create a list of section names
section_names = ["Introduction", "Background", "Theory", "Applications", "Case Studies", "Exercises", "Summary"]

# Get all course IDs from the Course table
cursor.execute("SELECT C_ID FROM Course")
course_ids = [row[0] for row in cursor.fetchall()]

# Generate section names and insert them into the Sections table for each course
for c_id in course_ids:
    num_sections = random.randint(1, len(section_names))
    for r in range(num_sections):
        sec_id = r+1
        sec_name = f'{section_names[r]} for Course {c_id}'
        sql = f"INSERT INTO Sections (Sec_ID, C_ID, Sec_Name) VALUES ({sec_id}, {c_id}, '{sec_name}')"
        cursor.execute(sql)
        mydb.commit()

# get existing thread and user IDs
cursor.execute("SELECT Thread_ID FROM Discussion_Thread")
threads = cursor.fetchall()
cursor.execute("SELECT U_ID FROM Account")
accounts = cursor.fetchall()

# generate random data for each reply
for f in range(100):  # generate 100 replies
    reply_id = f + 1
    thread_id = random.choice(threads)[0]
    u_id = random.choice(accounts)[0]
    reply_content = faker.paragraph()
    reply_date = faker.date_time_between(start_date='-1y', end_date='now')
    
    # check if reply ID, thread ID, and student ID combination already exists
    sql = "SELECT * FROM Discussion_Thread_Reply WHERE Reply_ID = %s AND Thread_ID = %s AND U_ID = %s"
    val = (reply_id, thread_id, u_id)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result is not None:
        continue  # skip this iteration if the combination already exists
    
    # insert data into database
    sql = "INSERT INTO Discussion_Thread_Reply (Reply_ID, Thread_ID, U_ID, Reply_Content, Reply_Date) VALUES (%s, %s, %s, %s, %s)"
    val = (reply_id, thread_id, u_id, reply_content, reply_date)
    cursor.execute(sql, val)

# commit changes to database and close connection
mydb.commit()
cursor.close()
mydb.close()
