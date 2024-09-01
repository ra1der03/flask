import flask_bcrypt
import pydantic
from flask import Flask, Response, jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from models import Session, Advertisement
from schema import CreateAdvertisement, Schema, UpdateAdvertisement

app = Flask("app")
bcrypt = flask_bcrypt.Bcrypt(app)


class HttpError(Exception):

    def __init__(self, status_code: int, error_message: str | dict):
        self.status_code = status_code
        self.error_message = error_message


def validate(schema_cls: Schema, json_data: dict):
    return json_data


@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    json_response = jsonify({"error": err.error_message})
    json_response.status_code = err.status_code
    return json_response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: Response):
    request.session.close()
    return response


def get_advertisement(advertisement_id):
    advertisement = request.session.get(Advertisement, advertisement_id)
    if advertisement is None:
        raise HttpError(404, "advertisement not found")
    return advertisement


def add_advertisement(advertisement: Advertisement):
    request.session.add(advertisement)
    try:
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, "advertisement already exists")
    return advertisement


class AdvertisementView(MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, advertisement_id):
        advertisement = add_advertisement(advertisement_id)
        return jsonify(advertisement.json)

    def post(self):
        json_data = validate(CreateAdvertisement, request.json)
        advertisement = add_advertisement(Advertisement(**json_data))
        return jsonify(advertisement.json)

    def patch(self, advertisement_id):
        json_data = validate(UpdateAdvertisement, request.json)
        advertisement = get_advertisement(advertisement_id)
        for field, value in json_data.items():
            setattr(advertisement, field, value)
        advertisement = add_advertisement(advertisement)
        return jsonify(advertisement.json)

    def delete(self, advertisement_id):
        advertisement = get_advertisement(advertisement_id)
        self.session.delete(advertisement)
        self.session.commit()
        return jsonify({"status": "deleted"})


advertisement_view = AdvertisementView.as_view("advertisement")

app.add_url_rule("/advertisement/", view_func=advertisement_view, methods=["POST"])
app.add_url_rule(
    "/advertisement/<int:advertisement_id>/", view_func=advertisement_view, methods=["GET", "PATCH", "DELETE"]
)

app.run()
