from flask import Flask

from .routes.federation_routes import init_routes as init_federation_routes
from .routes.manager_date_routes import init_routes as init_manager_routes
from .routes.team_routes import init_routes as init_team_routes
from ..database.mongodb_connection_adapter import MongoDBConnectionAdapter
from ...container.notification_container import NotificationContainer
from ...container.web_container_federation import WebContainerFederation
from ...container.web_container_manager_dates import WebContainerManagerDates
from ...container.web_container_team import WebContainerTeam

FOOTBALL_ANALYZER_API_PATH_MAIN = '/football-analyzer-360/api/v1'


def create_app():
    app = Flask(__name__)
    db_connection = MongoDBConnectionAdapter()
    if not db_connection.connect():
        raise Exception("Failed to connect to MongoDB")
    notification_container = NotificationContainer()
    web_container_manager_dates = WebContainerManagerDates(db_connection)
    web_container_federation = WebContainerFederation(
        db_connection,
        notification_container,
        app
    )
    web_container_team = WebContainerTeam(
        db_connection,
        web_container_manager_dates,
        web_container_federation,
        notification_container,
        app
    )
    manager_date_bp = init_manager_routes(web_container_manager_dates)
    federation_bp = init_federation_routes(web_container_federation)
    team_bp = init_team_routes(web_container_team)
    app.register_blueprint(manager_date_bp, url_prefix=FOOTBALL_ANALYZER_API_PATH_MAIN)
    app.register_blueprint(federation_bp, url_prefix=FOOTBALL_ANALYZER_API_PATH_MAIN)
    app.register_blueprint(team_bp, url_prefix=FOOTBALL_ANALYZER_API_PATH_MAIN)
    return app
