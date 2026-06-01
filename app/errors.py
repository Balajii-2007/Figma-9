"""
errors.py — Custom error handlers.
"""
from flask import render_template, jsonify, request


def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(e):
        if request.accept_mimetypes.accept_json:
            return jsonify(error="Not found"), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        if request.accept_mimetypes.accept_json:
            return jsonify(error="Internal server error"), 500
        return render_template("errors/500.html"), 500
