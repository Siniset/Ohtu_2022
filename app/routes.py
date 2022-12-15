from flask import render_template, request, redirect, abort, send_file, jsonify
from app.app import app
from app.controllers import reference_controller
from app.controllers import field_controller
from app.services import export_service


@app.route("/")
def index():
    references = reference_controller.get_titles()
    return render_template("index.html", references=references)


@app.route("/references/<reference_id>/fields", methods=["POST"])
def create_field(reference_id):
    name = request.form["name"]
    content = request.form["content"]

    field_controller.create(name, content, reference_id)

    return redirect("/")


@app.route("/references/<id>/fields")
def get_fields(id):
    return jsonify(field_controller.collect(id))


@app.route("/fields/<id>", methods=["PUT"])
def update_field(id):
    content = request.json["content"]
    field_controller.update(id, content)
    return jsonify({"content": content})


@app.route("/fields/<id>", methods=["DELETE"])
def delete_field(id):
    field_controller.delete_by_id(id)
    return jsonify({"id": id})


@app.route("/references", methods=["POST"])
def create_reference():
    name = request.form["name"]
    type = request.form["type"]

    fields = {
        "author": request.form["author"],
        "title": request.form["title"],
        "year": request.form["year"],
        "publisher": request.form["publisher"]
    }

    reference_controller.create(name, type, fields)
    return redirect("/")


@app.route("/references/<id>", methods=["DELETE"])
def delete_reference(id):
    reference_controller.delete_by_id(id)
    return jsonify({"id": id})


@app.route("/export")
def export():
    references = reference_controller.get_all()
    bibtex_file = export_service.export_as_bibtex(references)
    return send_file(bibtex_file, download_name="references.bib")

@app.errorhandler(404)
def handle_404(e):
    return render_template("error.html", code=404, message="Sivua ei löydy")

@app.errorhandler(ValueError)
def handler_bad_request(e):
    return render_template("error.html", code=400, message=e)
