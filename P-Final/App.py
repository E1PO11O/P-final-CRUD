import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'to_do_list'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"


usuarios = ["admin"]
contraseñas = ["admin"]

@app.route("/",methods=["GET","POST"])
def pagina_principal():
    return flask.render_template("login.html", datos={} )

@app.route("/autenticacion",methods=["GET","POST"])
def autenticar():
    global usuarios, contraseñas 

    autenticado = False

    if(flask.request.method == "POST"):
      usuario = flask.request.form["usuario1"]
      contraseña = flask.request.form["contraseña1"]

      indice = 0
      while(indice < len(usuarios)):
        if(usuario == usuarios[indice] and contraseña == contraseñas[indice]):
         autenticado = True
         break
        indice = indice + 1
    if (autenticado == True):  
     return redirect ("/d")
    else:
     flask.flash("Usuario Incorrecto")
     return flask.redirect(flask.url_for("pagina_principal"))
        

   
@app.route("/registro",methods=["GET","POST"])
def registrar():
    global usuarios, contraseñas

    if(flask.request.method == "POST"):
      usuario = flask.request.form["usuario2"]
      contraseña = flask.request.form["contraseña2"]

      usuarios.append(usuario)
      contraseñas.append(contraseña)

      flask.flash("Se ha registrado correctamente")

      return flask.redirect(flask.url_for("pagina_principal"))    

    

    

# routes
@app.route('/d')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
