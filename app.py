from flask import Flask
from flask import render_template, request, redirect, url_for,flash
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask import send_from_directory



app = Flask (__name__)
app.secret_key="FacKu"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='hiperlapso'
mysql.init_app(app)

CARPETA=os.path.join('uploads')
app.config['CARPETA']=CARPETA


@app.route('/')
def index():
    sql = "SELECT * FROM `hiperlapso`.`celular`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    celulares=cursor.fetchall()
    conn.commit()
    return render_template ('celulares/index.html', celulares=celulares)


#Mostrar imagen en web.

@app.route('/uploads/<nuevoNombreFoto>')
def uploads(nuevoNombreFoto):
    return send_from_directory(app.config['CARPETA'], nuevoNombreFoto)



@app.route('/create')
def create():
    return render_template('celulares/create.html')


#Eliminacion de datos.

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT foto FROM `hiperlapso`.`celular` WHERE id=%s", id)
    fila= cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM `hiperlapso`.`celular` WHERE id=%s", id)
    conn.commit()
    return redirect('/')



#Editar Datos.

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `hiperlapso`.`celular` WHERE id=%s", id)
    celulares= cursor.fetchall()
    conn.commit()
    return render_template('celulares/edit.html', celulares=celulares)


#Actualizacion de datos.

@app.route('/update', methods=['POST'])
def update():
    _marca=request.form['txtMarca']
    _modelo=request.form['txtModelo']
    _foto=request.files['txtFoto']
    _caracteristica1=request.form['txtCarac1']
    _caracteristica2=request.form['txtCarac2']
    _caracteristica3=request.form['txtCarac3']
    _precio=request.form['txtPrecio']
    id=request.form['txtID']

    sql="UPDATE `hiperlapso`.`celular` SET `marca` = %s, `modelo` = %s, `caracteristica1` = %s, `caracteristica2` = %s, `caracteristica3` = %s, `precio` = %s WHERE `id` = %s;"
    datos=(_marca,_modelo,_caracteristica1,_caracteristica2,_caracteristica3,_precio, id)
    conn = mysql.connect()
    cursor = conn.cursor()
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto )
        
        cursor.execute("SELECT foto FROM `hiperlapso`.`celular` WHERE id=%s;", (id))
        fila = cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

        cursor.execute("UPDATE `hiperlapso`.`celular` SET foto=%s WHERE id=%s",(nuevoNombreFoto, id))
        conn.commit()

    
    
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')



@app.route('/store', methods=['POST'])
def storage():
    _marca=request.form['txtMarca']
    _modelo=request.form['txtModelo']
    _foto=request.files['txtFoto']
    _caracteristica1=request.form['txtCarac1']
    _caracteristica2=request.form['txtCarac2']
    _caracteristica3=request.form['txtCarac3']
    _precio=request.form['txtPrecio']
    '''if _marca == '' or _modelo == '' or _foto.filename == '' or _caracteristica1 == '' or _caracteristica2 == '' or _caracteristica3 == '' or _precio == '':
        flash('Debe llenar todos los campos')
        return redirect(url_for('create'))'''

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)


    sql = "INSERT INTO `hiperlapso`.`celular` (`id`, `marca`, `modelo`, `foto`, `caracteristica1`, `caracteristica2`, `caracteristica3`, `precio`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);"
    datos=(_marca,_modelo,nuevoNombreFoto,_caracteristica1,_caracteristica2,_caracteristica3,_precio )
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)