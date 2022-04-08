#importar librerias
import email
from glob import escape
from flask import Flask, render_template, request, session
import os
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#iniciamos el flask
app = Flask(__name__)
app.secret_key = '54SF4GHAFHGAS4' #llave secreta para la cookies


#rutas de servidor 
@app.route('/') #conecta con la inerfaz proncipal 
def index_interfaz(): #funcion 
    con_bd = sqlite3.connect('db.db') #conectar a la base de datos 
    cursor_db = con_bd.cursor() #recorrer el conjunto tablas y filas o insertar
    sql = "SELECT * FROM productos" # se hace la consulta en la base de datos 
    cursor_db.execute(sql) #se ejecuta la consulta a la base de datos 
    consulta=cursor_db.fetchall()#guarda el resultado de la consulta 
    print(consulta)
    return render_template('index.html', productos=consulta) #lo que me muestra la vista

@app.route('/cerrarsesion',  methods=['GET']) # conecta al servidor y el metodo [GET] se utliza para consultar.
def cerrar_sesion():
    if "user" in session: #desicion para saber si el ususario esta logeado 
        session.pop("user") # si se cumple la desicion borra la cookies y el usuario quedaria deslogeado
        global consulta
        con_bd = sqlite3.connect('db.db') #conectar a la base de datos 
        cursor_db = con_bd.cursor() #recorrer el conjunto tablas y filas o insertar
        sql = "SELECT * FROM productos" # se hace la consulta en la base de datos 
        cursor_db.execute(sql) #se ejecuta la consulta a la base de datos 
        consulta=cursor_db.fetchall()#guarda el resultado de la consulta 
        print(consulta)
        return render_template('index.html',productos=consulta)#me retorna a la pagina principal 
    return render_template('index.html',productos=consulta) #de lo contrario sigo en la pagina principal

@app.route('/comprar/<id_producto>',  methods=['GET'])  # conecta al servidor y el metodo [GET] se utliza para consultar.
def compra(id_producto):
    if "user" in session: # desicion si el usuario esta logeado puede realizar su compra
        correo = session["user"] #cookies
        con_bd = sqlite3.connect('db.db') #conectar a la base de datos 
        cursor_db = con_bd.cursor() #recorrer el conjunto tablas y filas o insertar
        sql = "SELECT precio FROM productos WHERE id_producto='"+id_producto+"'" # se hace la consulta en la base de datos 
        cursor_db.execute(sql) #se ejecuta la consulta a la base de datos 
        consulta=cursor_db.fetchone()#guarda el resultado de la consulta 
        consulta = int(consulta[0])#conviete el resultado de la base de datos en entero 
        sql = "SELECT nombre_producto FROM productos WHERE id_producto='"+id_producto+"'"# se realiza una consulta
        cursor_db.execute(sql)#ejecuta la consulta del nombre del producto
        productos=cursor_db.fetchone()#guarda la el resultado de la base de datos
        productos= productos[0].upper()#muestra el resultado en la varible producto
        sql = "SELECT nombre FROM usuarios WHERE correo ='"+correo+"'"#consultar el nombre de usuario en la base de datos 
        cursor_db.execute(sql)#ejecutar la consulta
        for i in cursor_db:# for anidado- iteramos por una lista 
            for nombre in i:#iteramos en el campo mas interno de la lista

                        sql = "SELECT href FROM productos WHERE id_producto='"+id_producto+"'"#consultar el nombre de usuario en la base de datos 
                        cursor_db.execute(sql)#ejecutar la consulta
                        href=cursor_db.fetchone()#guarda la el resultado de la base de datos
                        href= href[0] 

                        sql = "SELECT imgs FROM productos WHERE id_producto='"+id_producto+"'"#consultar el nombre de usuario en la base de datos 
                        cursor_db.execute(sql)#ejecutar la consulta
                        imgs=cursor_db.fetchone()#guarda la el resultado de la base de datos
                        imgs= imgs[0]                  
                        
                        proveedor_correo = 'smtp.gmail.com: 587'
                        remitente = 'losdeatras865@gmail.com'   #enviar los correos a los usuarios que se registran 
                        password = 'adsi86520'

                        servidor = smtplib.SMTP(proveedor_correo)
                        servidor.starttls()
                        servidor.ehlo()
                        servidor.login(remitente, password)

                        mensaje = """<table border="1">
                                    <tr>
                                    <th colspan="3">FACTURA</th>
                                    </tr>
                                    <tr>
                                    <th>PRODUCTO</th>
                                    <th>PRECIO</th>
                                    <th>IMAGEN</th>
                                    </tr>
                                    <tr>
                                    <td>{}</td>
                                    <td>${}</td>
                                    <td><a href="{}"><img src="{}" alt="" WIDTH="150" HEIGHT="150"  /></a></td>
                                    </tr>
                                    <td colspan="2">TOTAL</td>
                                    <td>${}</td>
                                    </tr>

                                    </table>""".format(productos,consulta,href,imgs,consulta) #mensaje que se envia 
                        msg = MIMEMultipart()
                        msg.attach(MIMEText(mensaje, 'html'))
                        msg['From'] = remitente
                        msg['To'] = correo
                        msg['Subject'] = 'papeleria los de atras'
                        servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
                        return render_template('carrito.html', usuario=nombre , email=correo, producto=productos, precio=consulta)#nos envia a la interfar de compra
    return render_template('login.html')# me envia al login para inicar la sesion y poder comprar 
    

@app.route('/reginterfaz')#conecta con la inerfaz de registro
def registro_interfaz():
    return render_template('registro.html')#la ruta nos devuelve la vista de registro


@app.route('/registro', methods = ["POST"])#conecta al servidor y el metodo [POST] se utliza para que los datos sean seguros.
def registro():  #vamos a recoger los datos que infresan los usuarios o clientes 
    nombre= request.form.get("usuario")
    correo = request.form.get("correo")
    contrasena = request.form.get("contrasena")
    edad = request.form.get("edad")
    ciudad = request.form.get("ciudad")
    telefono = request.form.get("telefono")
    con_bd = sqlite3.connect('db.db')#conexion a base de datos
    cursor_db = con_bd.cursor()
    sql = "INSERT INTO usuarios(nombre,correo,contrasena,edad,ciudad,telefono)VALUES(?,?,?,?,?,?)"#los datos ingresados se guardan en la base de datos 
    try:
        cursor_db.execute(sql, (nombre,correo,contrasena,edad,ciudad,telefono))#ejecuta lo ingresado a guardar 
        con_bd.commit()
        cursor_db.close() #cierra la conexion 
        
        #envia correo a la persona que se registro
        proveedor_correo = 'smtp.gmail.com: 587'
        remitente = 'losdeatras865@gmail.com'   #enviar los correos a los usuarios que se registran 
        password = 'adsi86520'

        servidor = smtplib.SMTP(proveedor_correo)
        servidor.starttls()
        servidor.ehlo()
        servidor.login(remitente, password)

        mensaje = """<a href="https://ibb.co/PFRrFPm"><img src="https://i.ibb.co/ydDNdZf/registro.png" alt="registro" border="0"></a>""" #mensaje que se envia 
        msg = MIMEMultipart()
        msg.attach(MIMEText(mensaje, 'html'))
        msg['From'] = remitente
        msg['To'] = correo
        msg['Subject'] = 'papeleria los de atras'
        servidor.sendmail(msg['From'] , msg['To'], msg.as_string())
        return render_template('login.html') #retorna al login para iniciar sesion
    
    except:
        return render_template('login.html')# si ya me encuentro registrado me enviara a iniciar la sesion


@app.route('/logininterfaz')#conecta con la inerfaz de login
def ingreso_interfaz():
    return render_template('login.html')#muestra la vista de login.html


@app.route('/login', methods = ["POST"])#conecta al servidor y el metodo [POST] se utliza para que los datos sean seguros.
def login():
    global nombre # me conviete la variable nombre en global
    correo = request.form.get("correo") # el usuario debe ingresar el correo 
    contrasena = request.form.get("contrasena") # el usuario debe ingresar el contraseña 
    con_bd = sqlite3.connect('db.db') #conecto a la base de datos 
    cursor_db = con_bd.cursor()
    sql = "SELECT contrasena FROM usuarios WHERE correo ='"+correo+"'and contrasena='"+contrasena+"'"#consta base de datos verificar correo y contraseña
    cursor_db.execute(sql)#se ejecuta la consulta anterior 
    if cursor_db.fetchall():#desicion si este resultado es verdardero ejecuta lo siguiente
        session["user"] = correo # crear una cookies 
        sql = "SELECT nombre FROM usuarios WHERE correo ='"+correo+"'"#consultamos el nombre del correo ingresado 
        cursor_db.execute(sql)#ejecutamos la consulta 
        for i in cursor_db: # recorremos el resultado de la base de datos con un for anidado 
            for nombre in i:
                nombre = nombre.upper() # guarda el nombre del usuaro en la varible nombre
            con_bd = sqlite3.connect('db.db') #conectar a la base de datos 
            cursor_db = con_bd.cursor() #recorrer el conjunto tablas y filas o insertar
            sql = "SELECT * FROM productos" # se hace la consulta en la base de datos 
            cursor_db.execute(sql) #se ejecuta la consulta a la base de datos 
            consulta=cursor_db.fetchall()#guarda el resultado de la consulta 
            print(consulta)
            return render_template('index1.html', usuario=nombre, productos=consulta) #me retorna a la vista index1
    else:
        return render_template('login.html')#de lo contrario el usuario es incorrecto y vulvo al login

@app.route('/index1') #conecta con la inerfaz de index1
def index1_interfaz():
    con_bd = sqlite3.connect('db.db') #conectar a la base de datos 
    cursor_db = con_bd.cursor() #recorrer el conjunto tablas y filas o insertar
    sql = "SELECT * FROM productos" # se hace la consulta en la base de datos 
    cursor_db.execute(sql) #se ejecuta la consulta a la base de datos 
    consulta=cursor_db.fetchall()#guarda el resultado de la consulta 
    print(consulta)
    return render_template('index1.html' , usuario=nombre, productos=consulta)#muestra la vista de index1.html

app.run(debug = True, port=5000) # configuracion de servidor de flask