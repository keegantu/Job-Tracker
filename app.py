import psycopg2


from flask import Flask



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




@app.route("/")

def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)