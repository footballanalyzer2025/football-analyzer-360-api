from flask import Blueprint, request, jsonify

from ....container.web_container_standings import WebContainerStandings
from .....application.dto.standings_request_dto import StandingsRequestDTO
from .....commons.config.config_constants import ConfigConstants

standings_bp = Blueprint('standings', __name__)


def init_routes(web_container_standings: WebContainerStandings):

    @standings_bp.route('/standings', methods=['GET'])
    def get_standings():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        standings_by_federation_and_competitions = data.get(ConfigConstants.STANDINGS_BY_FEDERATION_AND_COMPETITIONS)
        if not standings_by_federation_and_competitions:
            return jsonify({'error': f'{ConfigConstants.STANDINGS_BY_FEDERATION_AND_COMPETITIONS} is required'}), 400
        dto = StandingsRequestDTO(
            standings_by_federation_and_competitions=standings_by_federation_and_competitions
        )
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400
        result = web_container_standings.get_standings_from_web_use_case.execute(dto)
        status_code = 200 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message,
            'data': result.data
        }), status_code

    return standings_bp
