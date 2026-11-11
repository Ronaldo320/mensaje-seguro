from flask import Flask, request, jsonify, render_template
import uuid
import os

app = Flask(__name__)
# Base de datos en memoria (para producción real se usaría SQLite o MongoDB)
mensajes_secretos = {} 

@app.route('/')
def index():
    # Muestra la página principal para crear el mensaje
    return render_template('index.html')

@app.route('/api/guardar', methods=['POST'])
def guardar():
    data = request.json
    mensaje = data.get('mensaje')
    if not mensaje:
        return jsonify({'error': 'No hay mensaje'}), 400
    
    # Genera un ID único para el enlace
    link_id = str(uuid.uuid4())
    mensajes_secretos[link_id] = mensaje
    
    # Devuelve el link completo
    enlace = f"{request.url_root}leer/{link_id}"
    return jsonify({'enlace': enlace})

@app.route('/leer/<link_id>')
def leer(link_id):
    # Aquí está la magia: pop() extrae el mensaje y lo ELIMINA inmediatamente
    mensaje = mensajes_secretos.pop(link_id, None)
    
    if mensaje:
        return render_template('leer.html', mensaje=mensaje)
    else:
        return "Este mensaje ha sido destruido o no existe.", 404

if __name__ == '__main__':
    app.run(debug=True)