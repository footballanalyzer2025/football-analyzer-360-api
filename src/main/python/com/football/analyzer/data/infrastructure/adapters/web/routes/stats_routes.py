from flask import Blueprint, request, jsonify

from ....container.web_container_stats import WebContainerStats
from .....application.dto.stats_request_dto import StatsRequestDTO
from .....commons.config.config_constants import ConfigConstants

stats_bp = Blueprint('stats', __name__)


def init_routes(web_container_stats: WebContainerStats):

    @stats_bp.route('/stats/upcoming-limited-schedule-matches', methods=['GET'])
    def get_upcoming_limited_schedule_matches():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        stats_by_federation_and_competitions = data.get(ConfigConstants.STATS_BY_FEDERATION_AND_COMPETITIONS)
        if not stats_by_federation_and_competitions:
            return jsonify({'error': f'{ConfigConstants.STATS_BY_FEDERATION_AND_COMPETITIONS} is required'}), 400
        dto = StatsRequestDTO(
            stats_by_federation_and_competitions=stats_by_federation_and_competitions
        )
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400
        result = web_container_stats.get_stats_use_case.execute(dto)
        status_code = 200 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message,
            'data': result.data
        }), status_code

    return stats_bp
