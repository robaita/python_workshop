from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os


app = Flask(__name__)

# Set an environment variable
os.environ["DB"] = "localhost;root;avinash;test_database"
# # from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from .env file

db_details = os.getenv('DB').split(";")
db_host = db_details[0]
db_user = db_details[1]
db_password = db_details[2]
db_name = db_details[3]

connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name)

@app.route('/')
def home():
    return render_template('add_tasks.html')

@app.route('/add_record', methods=['GET', 'POST'])
def add_task():
    # print("I am in add task")
    if request.method == 'POST':
        
        task_name = request.form['task_info']
        print('Task name:', task_name)

        estimated_hr = request.form['estimated_time']
        print("Estimated Time:", estimated_hr)
        # spent_hr = request.form['spnt_time']

        # task_duration = 

        # task_status = request.form['tsk_status']

        # Insert the new task into the MySQL database
        # creating the cursor object
        cursor = connection.cursor()

        # make the query string
        insert_query = """
            INSERT INTO tasks (name, task_date, estimated_time, spent_time, task_duration, task_status)
            VALUES (%s, CURDATE(), %s, %s, %s, %s)
        """
        student_data = (task_name, estimated_hr, "-", "-", "Open")

        # excute the query
        cursor.execute(insert_query, student_data)

        connection.commit()
        cursor.close()

    return render_template('add_tasks.html')

@app.route('/show_records', methods=['GET', 'POST'])
def show_records():
    # creating the cursor object
    # print("I am in show records")
    cursor = connection.cursor()
    try:
        task_status = request.form['tsk_status'].lower().strip()
        # print("Task Status:", task_status)
        if task_status=="open":
            print("Open")
            select_query = "SELECT * FROM tasks WHERE task_status = 'Open'"
        elif  task_status=="close": 
            print("Close") 
            select_query = "SELECT * FROM tasks WHERE task_status = 'Close'"
        else:
            select_query = "SELECT * FROM tasks"

        cursor.execute(select_query)

        # Fetching all results
        tasks = cursor.fetchall()
        # print(tasks)
    except:
        tasks = []

    return render_template('show_tasks.html', tasks = tasks)


@app.route('/close_records', methods=['GET', 'POST'])
def close_records():
    # creating the cursor object
    # print("I am in close records")
    tasks = []
    cursor = connection.cursor()
    status = False
    try:
        task_name = request.form['task_name']
    except:
        status = True

    # print("Status:", status)
    try:
        if status == True:
            # query string
            select_query = "SELECT * FROM tasks"

            # execute query
            cursor.execute(select_query)

            # Fetching all results

            tasks = cursor.fetchall()
        else:
            # print("I am in update records")
            # print(task_name)
            tsk_id = task_name.split("|")[0]
            # print(tsk_id)
            # query string
            select_query = "SELECT * FROM tasks WHERE id =" + tsk_id
            # name_filter = (tsk_id.trim(),)

            # execute query
            cursor.execute(select_query)

            # Fetching all results

            records = cursor.fetchall()
            # print("Records:",records)

            # task_id = records[0][0]
            est_time = str(records[0][3]).split(":")
            spent_time = request.form['spnt_time']
            spnt_time= spent_time.split(":")
            # print(spnt_time, est_time)
            task_status = "Open"
            if (int(spnt_time[0])*60+int(spnt_time[1]))>(int(est_time[0])*60+int(est_time[1])):
                duration = (int(spnt_time[0])*60+int(spnt_time[1]))-(int(est_time[0])*60+int(est_time[1]))
                durtion_str = str(duration // 60)+":"+str(duration % 60)
                task_status = "Close"
            else:
                duration = (int(est_time[0])*60+int(est_time[1]))-(int(spnt_time[0])*60+int(spnt_time[1]))
                durtion_str = str(duration // 60)+":"+str(duration % 60)
                task_status = "Open"

            # insert into database
            update_query = "UPDATE tasks SET spent_time = %s, task_duration = %s, task_status=%s WHERE id = %s"
            updated_data = (spent_time, durtion_str, task_status, tsk_id)

            #Executing the query
            cursor.execute(update_query, updated_data)

            #Commit the transaction
            connection.commit()

            print(f'Task ID {tsk_id} updated successfully!')

    except:
        tasks = []

    print(tasks)
    return render_template('close_tasks.html', tasks = tasks)


@app.route('/delete_records', methods=['GET', 'POST'])
def delete_records():
    # creating the cursor object
    # print("I am in close records")
    tasks = []
    cursor = connection.cursor()
    status = False
    try:
        task_name = request.form['task_name']
    except:
        status = True

    # print("Status:", status)
    try:
        if status == True:
            # query string
            select_query = "SELECT * FROM tasks"

            # execute query
            cursor.execute(select_query)

            # Fetching all results

            tasks = cursor.fetchall()
        else:
            # print("I am in update records")
            # print(task_name)
            tsk_id = task_name.split("|")[0]

            delete_query = "DELETE FROM tasks WHERE id = " + tsk_id

            #Executing the query
            cursor.execute(delete_query)

            #Commit the transaction
            connection.commit()

            print(f'Task ID {tsk_id} deleted successfully!')


            # query string
            select_query = "SELECT * FROM tasks"

            # execute query
            cursor.execute(select_query)

            # Fetching all results

            tasks = cursor.fetchall()

    except:
        tasks = []

    print(tasks)
    return render_template('delete_tasks.html', tasks = tasks)

if __name__ == "__main__":
    app.run(debug=True, port=5001)