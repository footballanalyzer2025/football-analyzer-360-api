from flask import Blueprint, request, jsonify

from ....container.web_container_manager_dates import WebContainerManagerDates
from .....application.dto.manager_date_request_dto import (
    CreateOrUpdateManagerDateRequestDTO,
    GetManagersDateRequestDTO,
    DeleteManagerDateRequestDTO
)

manager_date_bp = Blueprint('manager_dates', __name__)


def init_routes(web_container_manager_dates: WebContainerManagerDates):

    @manager_date_bp.route('/manager-dates', methods=['POST'])
    def create_or_update():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        dto = CreateOrUpdateManagerDateRequestDTO(managers_data=data)
        result = web_container_manager_dates.create_or_update_use_case.execute(dto)
        status_code = 200 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message,
            'managers': result.data
        }), status_code

    @manager_date_bp.route('/manager-dates', methods=['GET'])
    def get_by_teams():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        team_managers = data.get('team_managers')
        if not team_managers:
            return jsonify({'error': 'team_managers is required'}), 400
        dto = GetManagersDateRequestDTO(team_managers=team_managers)
        validation_error = dto.validate()
        if validation_error:
            return jsonify({'error': validation_error}), 400
        result = web_container_manager_dates.get_managers_use_case.execute(dto)
        status_code = 200 if result.success else 400
        return jsonify({
            'success': result.success,
            'message': result.message,
            'managers': result.data
        }), status_code

    @manager_date_bp.route('/manager-dates/all', methods=['GET'])
    def get_all():
        result = web_container_manager_dates.get_all_managers_use_case.execute()
        return jsonify({
            'success': result.success,
            'count': result.count,
            'managers': result.managers
        }), 200

    @manager_date_bp.route('/manager-dates/<team_name>', methods=['DELETE'])
    def delete_by_team(team_name):
        dto = DeleteManagerDateRequestDTO(team_name=team_name)
        result = web_container_manager_dates.delete_manager_use_case.execute(dto)
        status_code = 200 if result.success else 404
        return jsonify({
            'success': result.success,
            'message': result.message
        }), status_code

    return manager_date_bp
