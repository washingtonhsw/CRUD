from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    con = sql.connect("form_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users")
    data = cur.fetchall()
    return render_template("index.html", datas=data)


@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        nome = request.form["nome"]
        nascimento = request.form["nascimento"]
        matricula = request.form["matricula"]
        av1 = request.form["av1"]
        av2 = request.form["av2"]
        sexo = request.form["sexo"]
        con = sql.connect("form_db.db")
        cur = con.cursor()
        cur.execute("insert into users(NOME,NASCIMENTO,MATRICULA,AV1,AV2,SEXO) values (?,?,?,?,?,?)",
                    (nome, nascimento, matricula, av1, av2, sexo))
        con.commit()
        flash("Dados cadastrados", "success")
        return redirect(url_for("index"))
    return render_template("add_user.html")


@app.route("/edit_user/<string:id>", methods=["POST", "GET"])
def edit_user(id):
    if request.method == "POST":
        nome = request.form["nome"]
        nascimento = request.form["nascimento"]
        matricula = request.form["matricula"]
        av1 = request.form["av1"]
        av2 = request.form["av2"]
        sexo = request.form["sexo"]
        con = sql.connect("form_db.db")
        cur = con.cursor()
        cur.execute("update users set NOME=?,NASCIMENTO=?,MATRICULA=?,AV1=?,AV2=?,SEXO=? where ID=?",
                    (nome, nascimento, matricula, av1, av2, sexo, id))
        con.commit()
        flash("Dados atualizados", "success")
        return redirect(url_for("index"))
    con = sql.connect("form_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from users where ID =?", (id,))
    data = cur.fetchone()
    return render_template("edit_user.html", datas=data)


@app.route("/delete_user/<string:id>", methods=["GET"])
def delete_user(id):
    con = sql.connect("form_db.db")
    cur = con.cursor()
    cur.execute("delete from users where ID=?", (id,))
    con.commit()
    flash("Dados deletados", "warning")
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.secret_key = "admin123"
    app.run(debug=True)
