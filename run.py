from flask_prometheus_metrics import register_metrics
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from flaskr import create_app


if __name__ == '__main__':
    app = create_app()
    register_metrics(app, app_version="v0.1.2", app_config="staging")
    dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})
    app.run(debug=True, application=dispatcher)
