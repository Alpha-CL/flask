from flask import jsonify


def init_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(err):
        error_response = {
            'message': str(err),
            'status': 404
        }
        return jsonify(error_response), 404

    @app.errorhandler(Exception)
    def handle_error(err):
        error_response = {
            'message': str(err),
            'status': 500
        }
        return jsonify(error_response), 500
