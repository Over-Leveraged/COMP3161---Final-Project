from app import app
from flask import Flask, request, make_response
import json
import mysql.connector
from dbcon import databaseConnection
import json


@app.route('/RegisterUser', methods = ['GET', 'POST'])
def RegisterUser():
    conn = databaseConnection()
    cursor = conn.cursor()
    U_ID = request.form['U_ID']
    Password = request.form['Password']
    Name = request.form['Name']
    Type = request.form['Type']
    cursor.execute('INSERT INTO account (U_ID, Password, Name, Type) VALUES (%s, %s, %s, %s)', (U_ID, Password, Name, Type))
    if Type == 'lecturer':
        cursor.execute('INSERT INTO lecturer (Lec_ID, L_Name) VALUES (%s, %s)', (U_ID,Name))
    elif Type == 'student':
        cursor.execute('INSERT INTO student (Stu_ID, Stu_Name) VALUES (%s, %s)', (U_ID,Name))
    elif Type == 'admin':
        cursor.execute('INSERT INTO admin (Ad_ID, Ad_Name) VALUES (%s, %s)', (U_ID,Name))
    conn.commit()
    cursor.close()
    conn.close()
    return make_response('User Registered', 200)

@app.route('/get_user/<user_id>', methods = ['GET'])
def get_user(user_id):
    conn = databaseConnection() ##CHANGE THIS TO YOUR USERNAME AND PASSWORD IN THE dbcon.py FILE also ensure the database is named the same as in the dbcon.py file
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM account WHERE U_ID = %s', (user_id,))
    user = cursor.fetchone()

    if user is not None:
        U_ID, Password, Name, Type = user
        #U_ID, Password, Name = user
        userj = {}
        userj['U_ID'] = U_ID
        userj['Password'] = Password
        userj['Name'] = Name
        userj['Type'] = Type
        cursor.close()
        conn.close()
        return make_response(userj, 200)
    return make_response('User not found', 404)

@app.route('/get_admins', methods = ['GET'])
def get_admins():
    conn = databaseConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin')
    admin_lst = []
    for (Ad_ID, Ad_Name) in cursor:
        admin = {}
        admin['admin_id'] = Ad_ID
        admin['admin_name'] = Ad_Name
        admin_lst.append(admin)
    cursor.close()
    conn.close()
    return admin_lst

@app.route('/UserLogin', methods = ['GET', 'POST'])
def UserLogin():
    conn = databaseConnection()
    cursor = conn.cursor()
    U_ID = request.form['U_ID']
    Password = request.form['Password']
    cursor.execute('SELECT * FROM account WHERE U_ID = %s AND Password = %s', (U_ID, Password))
    row = cursor.fetchone()
    if row is not None: 
        U_ID, Password, Name, Type = row
        user = {}
        user['U_ID'] = U_ID
        user['Password'] = Password
        user['Name'] = Name
        user['Type'] = Type
        cursor.close()
        conn.close()
        message = "Successfully logged in as: {}".format(user['Name'])
        return make_response(message, 200)
    else:
        error_msg = 'User not found with those credentials'
        return make_response(error_msg, 404)
    

@app.route('/createCourse', methods = ['GET', 'POST'])
def createCourse():
    conn = databaseConnection()
    cursor = conn.cursor()
    U_ID = request.form['U_ID']
    Password = request.form['Password']
    C_ID = request.form['CourseID']
    Lec_ID = request.form['LecturerID']
    C_Name = request.form['CourseName']

    cursor.execute('SELECT * FROM account WHERE U_ID = %s AND Password = %s', (U_ID, Password))
    row = cursor.fetchone()
    if row is not None: 
        U_ID, Password, Name, Type = row
        cursor.execute('SELECT * FROM lecturer WHERE Lec_ID = %s', (Lec_ID,))
        lecRow = cursor.fetchone()
        if lecRow is not None:
            Lec_ID, Lec_Name, CoursesTaught = lecRow
            #dump the details into a dictionary
            if CoursesTaught < 5:
                cursor.execute('INSERT INTO course (C_ID, Lec_ID, C_Name) VALUES (%s, %s, %s)', (C_ID, Lec_ID, C_Name))
                cursor.execute('UPDATE lecturer SET Courses_Taught = Courses_Taught + 1 WHERE Lec_ID = %s', (Lec_ID,))
                conn.commit()
                cursor.close()
                conn.close()
                sucess_msg = 'Course Created and assigned to: {} ' .format(Lec_Name)
                return make_response(sucess_msg  , 200)

            else:
                error_msg = 'Lecturer not found'
                return make_response(error_msg, 404)
        else:
            error_msg = 'Lecturer not found with those credentials, cannot assign course'
            return make_response(error_msg, 404)

        #cursor.close()
        #conn.close()
        #message = "Successfully logged in as: {}".format(Name)
        #return make_response(message, 200)
    else:
        error_msg = 'Admin not found with those credentials cannot create course'
        cursor.close()
        conn.close()
        return make_response(error_msg, 404)

@app.route('/get_Discussion_threads/<D_ID>', methods = ['GET'])
def get_Discussion_threads(D_ID):
    conn = databaseConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM discussion_thread WHERE D_ID = %s', (D_ID,))
    thread_lst = []
    for (Thread_ID, D_ID, T_Name) in cursor:
        #U_ID, Password, Name = user
        dthreadj = {}
        dthreadj['Thread_ID'] = Thread_ID
        dthreadj['D_ID'] = D_ID
        dthreadj['T_Name'] = T_Name
        thread_lst.append(dthreadj)
    cursor.close()
    conn.close()
    return make_response(thread_lst, 200)

@app.route('/add_Discussion_thread', methods = ['POST'])
def add_Discussion_thread():
    conn = databaseConnection()
    cursor = conn.cursor()
    D_ID = request.form['D_ID']
    T_Name = request.form['T_Name']
    Thread_ID = request.form['Thread_ID']
    cursor.execute('INSERT INTO discussion_thread (Thread_ID, D_ID, T_Name) VALUES (%s, %s, %s)', (Thread_ID, D_ID, T_Name))
    conn.commit()
    cursor.close()
    conn.close()
    return make_response('Discussion Thread Added', 200)

@app.route('/add_reply', methods = ['POST'])
def add_reply():
    conn = databaseConnection()
    cursor = conn.cursor()
    Thread_ID = request.form['Thread_ID']
    Reply_ID = request.form['Reply_ID']
    Reply = request.form['Reply']
    U_ID = request.form['U_ID']
    cursor.execute('INSERT INTO discussion_thread_reply (Reply_ID, Thread_ID, Reply_Content, U_ID) VALUES (%s, %s, %s, %s)', (Reply_ID, Thread_ID, Reply, U_ID))
    conn.commit()
    cursor.close()
    conn.close()
    return make_response('Reply Added', 200)

@app.route('/add_course_items', methods = ['POST'])
def add_course_items():
    conn = databaseConnection()
    cursor = conn.cursor()
    C_ID = request.form['C_ID']
    Item_ID = request.form['Item_ID']
    Item_Name = request.form['Item_Name']
    Item_Type = request.form['Item_Type']
    #U_ID = request.form['U_ID']
    cursor.execute('INSERT INTO course_items (Item_ID, C_ID, Item_Name, Item_Type) VALUES (%s, %s, %s, %s)', (Item_ID, C_ID, Item_Name, Item_Type))
    conn.commit()
    cursor.close()
    conn.close()
    return make_response('Course Item Added', 200)


#Get all course items for a specific course
@app.route('/get_course_items/<C_ID>', methods = ['GET'])
def get_course_items(C_ID):
    conn = databaseConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM course_items WHERE C_ID = %s', (C_ID,))
    course_items_lst = []
    for (Item_ID, C_ID, Item_Name, Item_Type) in cursor:
        #U_ID, Password, Name = user
        course_itemsj = {}
        course_itemsj['Item_ID'] = Item_ID
        course_itemsj['C_ID'] = C_ID
        course_itemsj['Item_Name'] = Item_Name
        course_itemsj['Item_Type'] = Item_Type
        course_items_lst.append(course_itemsj)
    cursor.close()
    conn.close()
    return make_response(course_items_lst, 200)

@app.route('/submit_assignment', methods = ['POST'])
def submit_assignment():
    conn = databaseConnection()
    cursor = conn.cursor()
    A_ID = request.form['A_ID']
    C_ID = request.form['C_ID']
    STU_ID = request.form['STU_ID']
    cursor.execute('INSERT INTO assignment_grades (A_ID, C_ID, STU_ID) VALUES (%s, %s, %s)', (A_ID, C_ID, STU_ID))
    conn.commit()
    cursor.close()
    conn.close()
    return make_response('Assignment Submitted', 200)

@app.route('/assignGrades', methods = ['POST'])
def assignGrades():
    conn = databaseConnection()
    cursor = conn.cursor()
    A_ID = request.form['A_ID']
    C_ID = request.form['C_ID']
    STU_ID = request.form['STU_ID']
    Grade = request.form['Grade']
    cursor.execute('UPDATE assignment_grades SET Grade = %s WHERE A_ID = %s AND C_ID = %s AND STU_ID = %s', (Grade, A_ID, C_ID, STU_ID))
    conn.commit()
    cursor.close()
    conn.close()
    return make_response('Assignment Grade Assigned', 200)

   

    

























    



     
     



                                                            






    


        


    #except mysql.connector.Error as err:
        #print(err)











# if __name__ == '__main__':
#     app.run(debug=True)

