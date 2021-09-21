from flask import Flask, render_template, request
import  sqlite3 as sql
import bcrypt
import json
import json2html

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload_folder'
app.config['MAX_CONTENT-PATH'] = 16 * 1024 * 1024

def get_db():
    con = sql.connect('db/users.db')
    con.row_factory = sql.Row
    return con

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        usr = request.form['username']
        pssd = request.form['password']
        db = get_db()
        try:
            r = db.execute('select * from users where username=?',[usr]).fetchall()[0]
        except:
            return "User does not exist"
        if bcrypt.hashpw(pssd.encode('ascii'), r['password']) != r['password']:
            return "<h1> Login Failed please redo </h1>"
        return "Something"


@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        user = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        db.execute("insert into users(username,password,email) values(?,?,?)"    ,[user,bcrypt.hashpw(password.encode('ascii'),bcrypt.gensalt()),email])
        db.commit()
        return "done"

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
        f = request.files["file"]
        try:
            print(f)
            print(json.load(f))
        except:
            return "The file type is not JSON"
        f.save(f.filename)
        return "File successfully uploaded"



if __name__ == "__main__":
    app.run(debug=True)
