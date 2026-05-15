from flask import Blueprint, request, jsonify

from ....container.web_container_team import WebContainerTeam
from .....application.dto.team_request_dto import (
    CreateTeamsFromWebRequestDTO,
    CreateTeamsFromListRequestDTO,
    GetTeamsRequestDTO,
    DeleteTeamRequestDTO
)
from .....commons.config.config_constants import ConfigConstants

team_bp = Blueprint('teams', __name__)


def init_routes(web_container_team: WebContainerTeam):

    @team_bp.route('/teams/web-scrapping/by-federation', methods=['POST'])
    def create_from_federation():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        competitions_by_federation = data.get(ConfigConstants.COMPETITIONS_BY_FEDERATION)
        if not competitions_by_federation:
            return jsonify({'error': f'{ConfigConstants.COMPETITIONS_BY_FEDERATION} is required'}), 400
        dto = CreateTeamsFromWebRequestDTO(
            competitions_by_federation=competitions_by_federation
        )
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400
        result = web_container_team.create_teams_from_web_use_case.execute(dto)
        status_code = 202 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message
        }), status_code

    @team_bp.route('/teams/web-scrapping/by-list', methods=['POST'])
    def create_from_list():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        teams_to_create = data.get('teams_to_create')
        if not teams_to_create:
            return jsonify({'error': 'teams_to_create is required'}), 400
        dto = CreateTeamsFromListRequestDTO(teams_to_create=teams_to_create)
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400
        result = web_container_team.create_teams_from_list_use_case.execute(dto)
        status_code = 202 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message
        }), status_code

    @team_bp.route('/teams/all', methods=['GET'])
    def get_all():
        result = web_container_team.get_all_teams_use_case.execute()
        return jsonify({
            'success': result.success,
            'count': result.count,
            'teams': result.teams
        }), 200

    @team_bp.route('/teams', methods=['GET'])
    def get_teams():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        teams_data = data.get('teams_data')
        if not teams_data:
            return jsonify({'error': 'teams_data is required'}), 400
        dto = GetTeamsRequestDTO(teams_data=teams_data)
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400
        result = web_container_team.get_teams_use_case.execute(dto)
        status_code = 200 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message,
            'data': result.data
        }), status_code

    @team_bp.route('/teams/<team_name>', methods=['DELETE'])
    def delete_team(team_name):
        dto = DeleteTeamRequestDTO(team_to_delete=team_name)
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400
        result = web_container_team.delete_team_use_case.execute(dto)
        status_code = 200 if result.success else 404
        return jsonify({
            'success': result.success,
            'message': result.message
        }), status_code

    return team_bp
