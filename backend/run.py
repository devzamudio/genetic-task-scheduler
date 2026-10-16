"""run.py: Punto de entrada para ejecutar el servidor Flask."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # host="0.0.0.0" es CRÍTICO en Docker para permitir conexiones externas al contenedor
    app.run(host="0.0.0.0", debug=True, port=5000)