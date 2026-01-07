import psycopg2


from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/db_test")
def db_test():
    try:
        conn = psycopg2.connect(
            dbname="job_tracker",
            user="keegantu",
            host="localhost",
            port="5432"
        )
        conn.close()
        return "success"
    except Exception as e:
        return f"failed: {str(e)}"

@app.route("/applications")
def apps():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname="job_tracker",
            user="keegantu",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM application")
        rows = cursor.fetchall()
        
        return render_template("applications.html", applications=rows)
    except Exception as error:
        return f"Error: {error}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route("/add-application")
def add_application():
        return render_template("add_application.html")


@app.route("/submit-applications", methods=["POST"])
def submit():
    conn = None
    cursor = None
    

    try:
        conn = psycopg2.connect(
            dbname="job_tracker",
            user="keegantu",
            host="localhost",
            port="5432"
        )
        position = request.form['position']
        company = request.form['company']
        contact = request.form['contact']
        salary = request.form['salary']
        date_applied = request.form['date_applied']
        location = request.form['location']
        last_updated = request.form['last_updated']
        status = request.form['status']
        interview_datetime = request.form['interview_datetime']
        interview_location = request.form['interview_location']
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO application (position, company, contact, salary, date_applied, location, last_updated, status, interview_datetime, interview_location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (position, company, contact, salary, date_applied, location, last_updated, status, interview_datetime, interview_location))
        conn.commit()
        return redirect(url_for('apps'))
    except Exception as error:
        return f"Error: {error}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@app.route("/delete-application/<int:id>")
def delete_application(id):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname="job_tracker",
            user="keegantu",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        
        delete_query = """
        DELETE FROM application WHERE id = %s;
        """
        cursor.execute(delete_query, (id,))
        conn.commit()
        return redirect(url_for('apps'))
    except Exception as error:
        return f"Error: {error}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route("/edit-application/<int:id>")
def edit_app(id):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname="job_tracker",
            user="keegantu",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM application WHERE id = %s", (id,))
        app = cursor.fetchone()
        
        return render_template("edit_application.html", application=app)
    except Exception as error:
        return f"Error: {error}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route("/update-application/<int:id>", methods=["POST"])
def update(id):
    conn = None
    cursor = None
    

    try:
        conn = psycopg2.connect(
            dbname="job_tracker",
            user="keegantu",
            host="localhost",
            port="5432"
        )
        position = request.form['position']
        company = request.form['company']
        contact = request.form['contact']
        salary = request.form['salary']
        date_applied = request.form['date_applied']
        location = request.form['location']
        last_updated = request.form['last_updated']
        status = request.form['status']
        interview_datetime = request.form['interview_datetime']
        interview_location = request.form['interview_location']

        cursor = conn.cursor()
        update_query = """
            UPDATE application 
            SET position=%s, company=%s, contact=%s, salary=%s, date_applied=%s, location=%s, last_updated=%s, status=%s, interview_datetime=%s, interview_location=%s 
            WHERE id=%s
        """
        cursor.execute(update_query, (position, company, contact, salary, date_applied, location, last_updated, status, interview_datetime, interview_location, id))
        conn.commit()
        return redirect(url_for('apps'))
    except Exception as error:
        return f"Error: {error}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True, port=5001)