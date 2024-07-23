from flask import Flask
from flask_cors import CORS
from infrastructure.routers.task_router import task_router
from infrastructure.controllers.notifications_controller import notifications_blueprint
from infrastructure.services.scheduler import scheduler  # Importar el scheduler

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(task_router)
app.register_blueprint(notifications_blueprint)

@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    if scheduler.running:
        scheduler.shutdown()

if __name__ == '__main__':
    if not scheduler.running:
        scheduler.start()  # Iniciar el scheduler solo si no está corriendo
    try:
        app.run(debug=True, host='0.0.0.0', port=5003)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Apagar el scheduler en caso de interrupción
