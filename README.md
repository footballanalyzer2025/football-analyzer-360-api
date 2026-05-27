# Football Analyzer 360

Football match analysis system using Web Scraping and Hexagonal Architecture.

## 🏗️ Project Structure

```
src/
└── main/
    └── python/
        └── com/
            └── football/
                └── analyzer/
                    └── data/
                        ├── application/
                        │   ├── dto/
                        │   │   ├── federation_request_dto.py
                        │   │   ├── manager_date_request_dto.py
                        │   │   ├── manager_date_response_dto.py
                        │   │   ├── standings_request_dto.py
                        │   │   ├── stats_request_dto.py
                        │   │   └── team_request_dto.py
                        │   ├── services/
                        │   │   ├── notifications/
                        │   │   │   └── notification_service.py
                        │   │   ├── parsers/
                        │   │   └── web_scrapping/
                        │   │       ├── web_scrapping_competitions_by_federations_orchestrator_service.py
                        │   │       ├── web_scrapping_standings_orchestrator_service.py
                        │   │       ├── web_scrapping_team_matches_orchestrator_service.py
                        │   │       └── web_scrapping_team_orchestrator_service.py
                        │   └── use_cases/
                        │       ├── calendar/
                        │       │   ├── get_calendars_use_case.py
                        │       │   └── get_upcoming_matches_of_calendars_use_case.py
                        │       ├── federation/
                        │       │   ├── create_or_update_federation_from_web_use_case.py
                        │       │   ├── delete_federation_use_case.py
                        │       │   ├── get_all_federations_use_case.py
                        │       │   └── get_federations_use_case.py
                        │       ├── manager_date/
                        │       │   ├── create_or_update_manager_date_use_case.py
                        │       │   ├── delete_manager_date_use_case.py
                        │       │   ├── get_all_manager_dates_use_case.py
                        │       │   └── get_managers_date_use_case.py
                        │       ├── standings/
                        │       │   └── get_standings_from_web_use_case.py
                        │       ├── stats/
                        │       │   └── get_stats_use_case.py
                        │       └── team/
                        │           ├── create_teams_from_list_use_case.py
                        │           ├── create_teams_from_web_use_case.py
                        │           ├── delete_team_use_case.py
                        │           ├── get_all_teams_use_case.py
                        │           ├── get_team_matches_use_case.py
                        │           └── get_teams_use_case.py
                        ├── commons/
                        │   └── config/
                        │       ├── config_constants.py
                        │       ├── config_ini.py
                        │       ├── config_loader.py
                        │       └── singleton_meta.py
                        ├── domain/
                        │   ├── entities/
                        │   │   ├── competition.py
                        │   │   ├── federation.py
                        │   │   ├── match.py
                        │   │   └── team.py
                        │   ├── ports/
                        │   │   ├── extractors/
                        │   │   │   └── html_extractor_strategy.py
                        │   │   ├── http/
                        │   │   │   └── http_requester_port.py
                        │   │   ├── notifications/
                        │   │   │   └── notification_port.py
                        │   │   ├── parser/
                        │   │   │   └── html_parser_port.py
                        │   │   ├── repositories/
                        │   │   │   ├── database_connection_port.py
                        │   │   │   ├── federation_repository_port.py
                        │   │   │   ├── manager_date_repository_port.py
                        │   │   │   └── team_repository_port.py
                        │   │   ├── services/
                        │   │   │   └── data_source_port.py
                        │   │   └── standings/
                        │   │       └── standings_web_parser_port.py
                        │   ├── repositories/
                        │   │   ├── competition_repository.py
                        │   │   └── team_repository.py
                        │   ├── services/
                        │   │   └── season_filter_service.py
                        │   └── value_objects/
                        │       ├── match_result.py
                        │       ├── match_score.py
                        │       ├── mongodb_config.py
                        │       └── notification_config.py
                        └── infrastructure/
                            ├── adapters/
                            │   ├── database/
                            │   │   └── mongodb_connection_adapter.py
                            │   ├── exceptions/
                            │   │   ├── html_extractor_exception_handler.py
                            │   │   └── selector_syntax_error_exception.py
                            │   ├── extractors/
                            │   │   └── beautifulsoup_html_extractor_strategy.py
                            │   ├── http/
                            │   │   ├── exceptions/
                            │   │   │   └── http_requester_exception.py
                            │   │   └── http_requester_adapter.py
                            │   ├── notifications/
                            │   │   └── telegram_notification_adapter.py
                            │   ├── parsers/
                            │   │   ├── lxml_parser_adapter.py
                            │   │   └── standings_web_parser_factory.py
                            │   ├── repositories/
                            │   │   ├── mongodb_federation_repository.py
                            │   │   ├── mongodb_manager_date_repository.py
                            │   │   └── mongodb_team_repository.py
                            │   ├── services/
                            │   │   ├── web_scrapping_competitions_by_federations_data_source_adapter.py
                            │   │   ├── web_scrapping_standings_data_source_adapter.py
                            │   │   ├── web_scrapping_team_data_source_adapter.py
                            │   │   └── web_scrapping_team_matches_data_source_adapter.py
                            │   ├── standings/
                            │   │   └── fifa_world_cup_web_standings_parser_adapter.py
                            │   └── web/
                            │       ├── app.py
                            │       └── routes/
                            │           ├── federation_routes.py
                            │           ├── manager_date_routes.py
                            │           ├── standings_routes.py
                            │           ├── stats_routes.py
                            │           └── team_routes.py
                            ├── container/
                            │   ├── notification_container.py
                            │   ├── web_container_federation.py
                            │   ├── web_container_manager_dates.py
                            │   ├── web_container_standings.py
                            │   ├── web_container_stats.py
                            │   ├── web_container_team.py
                            │   └── web_scrapping_data_source_container.py
                            └── helpers/
                                ├── competition_type_helper.py
                                ├── web_scrapping_calendar_data_live_football_helper.py
                                ├── web_scrapping_main_data_live_football_helper.py
                                ├── web_scrapping_standings_helper.py
                                ├── web_scrapping_team_matches_data_live_football_helper.py
                                └── web_scrapping_teams_data_live_football_helper.py

```

## 🏛️ Hexagonal Architecture

The project follows **Hexagonal Architecture (Ports & Adapters)** principles:

### **Domain Layer** (`src/main/python/com/football/analyzer/domain/`)
- **`entities/`**: Business entities (Match, Competition, etc.)
- **`ports/`**: Interface contracts (RepositoryPort, ServicePort, etc.)

### **Application Layer** (`src/main/python/com/football/analyzer/application/`)
- **`use_cases/`**: Use cases orchestrating business logic (organized by domain: federation, team, calendar, etc.)
- **`services/`**: Application services (notification service, etc.)
- **`dto/`**: Data Transfer Objects for requests and responses

### **Infrastructure Layer** (`src/main/python/com/football/analyzer/infrastructure/`)
- **`adapters/`**: Concrete implementations of ports
  - **`database/`**: MongoDB connection adapter
  - **`repositories/`**: MongoDB repository implementations
  - **`services/`**: Web scraping data source adapters
  - **`web/`**: Flask API routes and app factory
  - **`notifications/`**: Notification channels (Telegram, email, etc.)
- **`container/`**: Dependency injection containers for use cases

## 🚀 API Endpoints

| Method | Endpoint                             | Description                                           |
|--------|--------------------------------------|-------------------------------------------------------|
| POST   | `/federations/web-scrapping`         | Start background scraping of federations/competitions |
| GET    | `/federations`                       | Get specific federations by body payload              |
| GET    | `/federations/all`                   | Get all federations                                   |
| GET    | `/federations/calendars`             | Get calendars for specific federations/competitions   |
| GET    | `/federations/upcoming-matches`      | Get upcoming matches (limited by formula)             |
| DELETE | `/federations/<name>`                | Delete a federation                                   |
| POST   | `/teams/web-scrapping/by-federation` | Start background scraping of teams from federations   |
| POST   | `/teams/web-scrapping/by-list`       | Start background scraping of teams from a list        |
| GET    | `/teams/all`                         | Get all teams                                         |
| GET    | `/teams`                             | Get specific teams by body payload                    |
| DELETE | `/teams/<name>`                      | Soft delete a team                                    |
| POST   | `/manager-dates`                     | Create/update manager start dates                     |
| GET    | `/manager-dates/all`                 | Get all manager dates                                 |
| DELETE | `/manager-dates/<team>`              | Delete a manager date entry                           |

## 🔧 Configuration

Configuration is managed via `.ini` files:
- `deployment/config/config_files.ini` - Master file listing all config files
- `deployment/config/data_sources/web_scrapping/live_football.ini` - Web scraping selectors and URLs
- `deployment/config/notifications.ini` - Notification channels (Telegram, etc.)

## 🛠️ Technologies Used

- **Python 3.11+** - Main language
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client
- **Flask** - REST API framework
- **PyMongo** - MongoDB driver
- **MongoDB** - Database
- **Docker** - Containerization (MongoDB, Mongo Express)
- **python-telegram-bot** - Telegram notifications

## 📝 Design Patterns Implemented

| Pattern          | Location         | Purpose                                        |
|------------------|------------------|------------------------------------------------|
| **Strategy**     | `extractors/`    | Interchangeable HTML extraction strategies     |
| **Adapter**      | `adapters/`      | Adapt external interfaces to domain            |
| **Repository**   | `repositories/`  | Abstract data access (MongoDB)                 |
| **Use Case**     | `use_cases/`     | Encapsulate business logic                     |
| **Orchestrator** | `services/`      | Coordinate complex scraping processes          |
| **Container**    | `container/`     | Dependency injection for use cases             |
| **Singleton**    | `ConfigLoader`   | Single instance for configuration              |
| **Factory**      | `create_app()`   | Flask application factory                      |
| **Notification** | `notifications/` | Multi-channel notifications (Strategy pattern) |

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.