from flask import Flask

from flask_smorest import Api

from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint


app = Flask(__name__)

# mandatory config for flask_smorest api
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"

# optional config
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(StoreBlueprint)
api.register_blueprint(ItemBlueprint)


@app.get("/")
def root():
    return {"message": "I am live!"}
