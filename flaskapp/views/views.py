from flaskapp.core.cooldownmanager import CoolDownManager

from flask import Blueprint, Flask, make_response, request
import threading

bp = Blueprint("core", __name__, url_prefix="/")

app = Flask(__name__)

cooldownmanager = CoolDownManager()
cooldownmanager.run_thread = threading.Thread(target=cooldownmanager._run, args=(), daemon=True)
cooldownmanager.run_thread.start()

@bp.route("/", methods=["GET"])
def get_token():
    if request.method == "GET":
        token = cooldownmanager.get_token()
        if token is True:
            status = 200
            data = {"message":"authorized"}
        else:
            status = 503
            data = {"message":"service not available"}
        response = make_response(data, status)
        return response
