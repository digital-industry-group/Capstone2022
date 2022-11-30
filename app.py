from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from resources.mail_chimp import blp as MailchimpBlueprint
from resources.google_analytics import blp as GoogleAnalyticsBlueprint

app = Flask(__name__)
app.config["API_TITLE"] = "REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["PROPAGATE_EXCEPTIONS"] = True
CORS(app)
api = Api(app)


api.register_blueprint(MailchimpBlueprint)
api.register_blueprint(GoogleAnalyticsBlueprint)
