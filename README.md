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
                        │   │   └── team_request_dto.py
                        │   ├── services/
                        │   │   ├── web_scrapping_competitions_by_federations_orchestrator_service.py
                        │   │   ├── web_scrapping_team_matches_orchestrator_service.py
                        │   │   └── web_scrapping_team_orchestrator_service.py
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
                        │   │   ├── parser/
                        │   │   │   └── html_parser_port.py
                        │   │   ├── repositories/
                        │   │   │   ├── database_connection_port.py
                        │   │   │   ├── federation_repository_port.py
                        │   │   │   ├── manager_date_repository_port.py
                        │   │   │   └── team_repository_port.py
                        │   │   └── services/
                        │   │       └── data_source_port.py
                        │   ├── repositories/
                        │   │   ├── competition_repository.py
                        │   │   └── team_repository.py
                        │   ├── services/
                        │   │   └── season_filter_service.py
                        │   └── value_objects/
                        │       ├── match_result.py
                        │       ├── match_score.py
                        │       └── mongodb_config.py
                        └── infrastructure/
                            ├── adapters/
                            │   ├── api/
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
                            │   ├── parsers/
                            │   │   └── lxml_parser_adapter.py
                            │   ├── repositories/
                            │   │   ├── mongodb_federation_repository.py
                            │   │   ├── mongodb_manager_date_repository.py
                            │   │   └── mongodb_team_repository.py
                            │   ├── services/
                            │   │   ├── web_scrapping_competitions_by_federations_data_source_adapter.py
                            │   │   ├── web_scrapping_team_data_source_adapter.py
                            │   │   └── web_scrapping_team_matches_data_source_adapter.py
                            │   └── web/
                            │       ├── app.py
                            │       └── routes/
                            │           ├── federation_routes.py
                            │           ├── manager_date_routes.py
                            │           └── team_routes.py
                            ├── container/
                            │   ├── web_container_federation.py
                            │   ├── web_container_manager_dates.py
                            │   ├── web_container_team.py
                            │   └── web_scrapping_data_source_container.py
                            └── helpers/
                                ├── web_scrapping_calendar_data_live_football_helper.py
                                ├── web_scrapping_main_data_live_football_helper.py
                                ├── web_scrapping_team_matches_data_live_football_helper.py
                                └── web_scrapping_teams_data_live_football_helper.py

```

## 🏛️ Hexagonal Architecture

The project follows **Hexagonal Architecture (Ports & Adapters)** principles:

### **Domain Layer** (`src/main/python/com/football/analyzer/domain/`)
- **`entities/`**: Business entities (Match, Competition, etc.)
- **`ports/`**: Interface contracts (RepositoryPort, ServicePort, etc.)

### **Application Layer** (`src/main/python/com/football/analyzer/application/`)
- **`use_cases/`**: Use cases orchestrating business logic

### **Infrastructure Layer** (`src/main/python/com/football/analyzer/infrastructure/`)
- **`adapters/`**: Concrete implementations of ports
  - `repositories/`: Repository adapters
  - `services/`: Service adapters
  - `extractors/`: Data extraction strategies
  - `mappers/`: Entity-DTO mappers

## 🚀 Installation & Usage

# 1. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

```

## 🛠️ Technologies Used

- **Python 3.10+** - Main language
- **BeautifulSoup4** - HTML parsing
- **pytest** - Testing framework
- **pytest-cov** - Test coverage
- **lxml** - Fast XML/HTML parser
- **unittest.mock** - Mocking for tests

## 📝 Design Patterns Implemented

| Pattern          | Location        | Purpose                             |
|------------------|-----------------|-------------------------------------|
| **Strategy**     | `extractors/`   | Swap HTML extraction strategies     |
| **Adapter**      | `adapters/`     | Adapt external interfaces to domain |
| **Repository**   | `repositories/` | Abstract data access                |
| **Mapper**       | `mappers/`      | Convert between entities and DTOs   |
| **Use Case**     | `use_cases/`    | Encapsulate business logic          |
| **Orchestrator** | `services/`     | Coordinate complex processes        |

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.