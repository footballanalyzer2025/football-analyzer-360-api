import logging

from flask import Blueprint, request, jsonify

from ....container.web_container_federation import WebContainerFederation
from .....application.dto.federation_request_dto import (
    CreateOrUpdateFederationFromWebRequestDTO,
    GetFederationsRequestDTO,
    DeleteFederationRequestDTO, GetCalendarsRequestDTO
)
from .....commons.config.config_constants import ConfigConstants

federation_bp = Blueprint('federations', __name__)
logger = logging.getLogger(__name__)


def init_routes(web_container_federation: WebContainerFederation):

    @federation_bp.route('/federations/web-scrapping', methods=['POST'])
    def create_or_update_from_web():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        competitions_by_federation = data.get(ConfigConstants.COMPETITIONS_BY_FEDERATION)
        if not competitions_by_federation:
            return jsonify({'error': f'{ConfigConstants.COMPETITIONS_BY_FEDERATION} is required'}), 400

        dto = CreateOrUpdateFederationFromWebRequestDTO(
            competitions_by_federation=competitions_by_federation
        )
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400

        result = web_container_federation.create_or_update_from_web_use_case.execute(dto)
        status_code = 202 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message
        }), status_code

    @federation_bp.route('/federations', methods=['GET'])
    def get_federations():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        competitions_by_federation = data.get(ConfigConstants.COMPETITIONS_BY_FEDERATION)
        if not competitions_by_federation:
            return jsonify({'error': f'{ConfigConstants.COMPETITIONS_BY_FEDERATION} is required'}), 400
        dto = GetFederationsRequestDTO(
            competitions_by_federation=competitions_by_federation
        )
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400
        result = web_container_federation.get_federations_use_case.execute(dto)
        status_code = 200 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message,
            'count': result.count,
            'federations': result.federations
        }), status_code

    @federation_bp.route('/federations/all', methods=['GET'])
    def get_all():
        result = web_container_federation.get_all_federations_use_case.execute()
        return jsonify({
            'success': result.success,
            'count': result.count,
            'federations': result.federations
        }), 200

    @federation_bp.route('/federations/calendars', methods=['GET'])
    def get_calendars():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        calendars_by_federation_and_competitions = data.get(ConfigConstants.CALENDARS_BY_FEDERATION_AND_COMPETITIONS)
        if not calendars_by_federation_and_competitions:
            return jsonify({'error': f'{ConfigConstants.CALENDARS_BY_FEDERATION_AND_COMPETITIONS} is required'}), 400
        dto = GetCalendarsRequestDTO(
            calendars_by_federation_and_competitions=calendars_by_federation_and_competitions
        )
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400
        result = web_container_federation.get_calendars_use_case.execute(dto)
        status_code = 200 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message,
            ConfigConstants.CALENDARS_BY_FEDERATION_AND_COMPETITIONS: result.calendars_by_federation_and_competitions
        }), status_code

    @federation_bp.route('/federations/upcoming-limited-schedule-matches', methods=['GET'])
    def get_upcoming_matches():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        calendars_by_federation_and_competitions = data.get(ConfigConstants.CALENDARS_BY_FEDERATION_AND_COMPETITIONS)
        if not calendars_by_federation_and_competitions:
            return jsonify({'error': f'{ConfigConstants.CALENDARS_BY_FEDERATION_AND_COMPETITIONS} is required'}), 400
        dto = GetCalendarsRequestDTO(
            calendars_by_federation_and_competitions=calendars_by_federation_and_competitions
        )
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400
        result = web_container_federation.get_upcoming_matches_use_case.execute(dto)
        status_code = 200 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message,
            'upcoming_matches_by_federation_and_competition': result.upcoming_matches_by_federation_and_competition
        }), status_code

    @federation_bp.route('/federations/<federation_name>', methods=['DELETE'])
    def delete_by_name(federation_name):
        dto = DeleteFederationRequestDTO(federation_name=federation_name)
        result = web_container_federation.delete_federation_use_case.execute(dto)
        status_code = 200 if result.success else 404
        return jsonify({
            'success': result.success,
            'message': result.message
        }), status_code

    @federation_bp.route('/federations/web-scrapping/status', methods=['GET'])
    def get_scraping_status():
        return jsonify({
            'status': 'processing',
            'message': 'Last scraping status'
        }), 200

    return federation_bp
