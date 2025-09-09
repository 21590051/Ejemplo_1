import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la base de datos
class Bebida(db.Model):
    __tablename__ = 'bebidas'
    ID = db.Column(db.Integer, primary_key=True)  
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    unidades = db.Column(db.Integer, nullable=False)
     
    def to_dict(self):
        return {
            'ID': self.ID,
            'nombre': self.nombre,
            'descripcion': self.descripcion, 
            'precio': self.precio,
            'unidades': self.unidades,
        }

# Crear tablas automáticamente
with app.app_context():
    db.create_all()

# Ruta principal
@app.route("/")
def home():
    bebidas = Bebida.query.all()
    return render_template("index.html", bebidas=bebidas)

# Crear nueva bebida
@app.route('/bebidas/new', methods=['GET', 'POST'])
def create_bebida():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        unidades = int(request.form['unidades'])
        
        nva_bebida = Bebida(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            unidades=unidades
        )
        db.session.add(nva_bebida)
        db.session.commit()
        
        return redirect(url_for('home'))
    
    # Si es GET
    return render_template('create_bebida.html') 

if __name__ == "__main__":
    app.run(debug=True)
