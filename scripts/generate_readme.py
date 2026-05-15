import os
from pathlib import Path


def generate_directory_tree(start_path, prefix=""):
    """
    Recursively generates a directory tree structure as a list of strings.

    Args:
        start_path: The root directory path to start from.
        prefix: The prefix string for the current level (used for recursion).

    Returns:
        A list of strings representing the directory tree.
    """
    tree_lines = []

    try:
        items = sorted(os.listdir(start_path))
    except PermissionError:
        return tree_lines

    # Ignore hidden files/folders and __pycache__
    items = [item for item in items if not item.startswith('.') and item != '__pycache__']

    for i, item in enumerate(items):
        item_path = os.path.join(start_path, item)
        is_last = (i == len(items) - 1)

        connector = "└── " if is_last else "├── "

        if os.path.isdir(item_path):
            rel_path = os.path.relpath(item_path, Path(__file__).parent.parent)
            # Only include directories inside src/ or tests/
            if any(rel_path.startswith(p) for p in ["src", "tests"]) or start_path.endswith(("src", "tests")):
                tree_lines.append(f"{prefix}{connector}{item}/")
                extension = "    " if is_last else "│   "
                tree_lines.extend(generate_directory_tree(item_path, prefix + extension))
        else:
            # Only include .py files that are not __init__.py
            if item.endswith('.py') and item != '__init__.py':
                rel_path = os.path.relpath(start_path, Path(__file__).parent.parent)
                if any(rel_path.startswith(p) for p in ["src", "tests"]) or start_path.endswith(("src", "tests")):
                    tree_lines.append(f"{prefix}{connector}{item}")

    return tree_lines


def main():
    project_root = Path(__file__).parent.parent

    readme_content = [
        "# Football Analyzer 360",
        "",
        "Football match analysis system using Web Scraping and Hexagonal Architecture.",
        "",
        "## 🏗️ Project Structure",
        "",
        "```"
    ]

    src_path = project_root / "src"
    if src_path.exists():
        readme_content.append("src/")
        readme_content.extend(generate_directory_tree(src_path, ""))
    else:
        print(f"Warning: 'src' folder not found in {project_root}")

    readme_content.append("")

    tests_path = project_root / "tests"
    if tests_path.exists():
        readme_content.append("tests/")
        readme_content.extend(generate_directory_tree(tests_path, ""))
    else:
        print(f"Warning: 'tests' folder not found in {project_root}")

    readme_content.append("```")

    readme_content.extend([
        "",
        "## 🏛️ Hexagonal Architecture",
        "",
        "The project follows **Hexagonal Architecture (Ports & Adapters)** principles:",
        "",
        "### **Domain Layer** (`src/main/python/com/football/analyzer/domain/`)",
        "- **`entities/`**: Business entities (Match, Competition, etc.)",
        "- **`ports/`**: Interface contracts (RepositoryPort, ServicePort, etc.)",
        "",
        "### **Application Layer** (`src/main/python/com/football/analyzer/application/`)",
        "- **`use_cases/`**: Use cases orchestrating business logic (organized by domain: federation, team, calendar, etc.)",
        "- **`services/`**: Application services (notification service, etc.)",
        "- **`dto/`**: Data Transfer Objects for requests and responses",
        "",
        "### **Infrastructure Layer** (`src/main/python/com/football/analyzer/infrastructure/`)",
        "- **`adapters/`**: Concrete implementations of ports",
        "  - **`database/`**: MongoDB connection adapter",
        "  - **`repositories/`**: MongoDB repository implementations",
        "  - **`services/`**: Web scraping data source adapters",
        "  - **`web/`**: Flask API routes and app factory",
        "  - **`notifications/`**: Notification channels (Telegram, email, etc.)",
        "- **`container/`**: Dependency injection containers for use cases",
        "",
        "## 🚀 API Endpoints",
        "",
        "| Method | Endpoint | Description |",
        "|--------|----------|-------------|",
        "| POST   | `/federations/web-scrapping` | Start background scraping of federations/competitions |",
        "| GET    | `/federations` | Get specific federations by body payload |",
        "| GET    | `/federations/all` | Get all federations |",
        "| GET    | `/federations/calendars` | Get calendars for specific federations/competitions |",
        "| GET    | `/federations/upcoming-matches` | Get upcoming matches (limited by formula) |",
        "| DELETE | `/federations/<name>` | Delete a federation |",
        "| POST   | `/teams/web-scrapping/by-federation` | Start background scraping of teams from federations |",
        "| POST   | `/teams/web-scrapping/by-list` | Start background scraping of teams from a list |",
        "| GET    | `/teams/all` | Get all teams |",
        "| GET    | `/teams` | Get specific teams by body payload |",
        "| DELETE | `/teams/<name>` | Soft delete a team |",
        "| POST   | `/manager-dates` | Create/update manager start dates |",
        "| GET    | `/manager-dates/all` | Get all manager dates |",
        "| DELETE | `/manager-dates/<team>` | Delete a manager date entry |",
        "",
        "## 🔧 Configuration",
        "",
        "Configuration is managed via `.ini` files:",
        "- `deployment/config/config_files.ini` - Master file listing all config files",
        "- `deployment/config/data_sources/web_scrapping/live_football.ini` - Web scraping selectors and URLs",
        "- `deployment/config/notifications.ini` - Notification channels (Telegram, etc.)",
        "",
        "## 🛠️ Technologies Used",
        "",
        "- **Python 3.11+** - Main language",
        "- **BeautifulSoup4** - HTML parsing",
        "- **Requests** - HTTP client",
        "- **Flask** - REST API framework",
        "- **PyMongo** - MongoDB driver",
        "- **MongoDB** - Database",
        "- **Docker** - Containerization (MongoDB, Mongo Express)",
        "- **python-telegram-bot** - Telegram notifications",
        "",
        "## 📝 Design Patterns Implemented",
        "",
        "| Pattern          | Location        | Purpose                             |",
        "|------------------|-----------------|-------------------------------------|",
        "| **Strategy**     | `extractors/`   | Interchangeable HTML extraction strategies |",
        "| **Adapter**      | `adapters/`     | Adapt external interfaces to domain |",
        "| **Repository**   | `repositories/` | Abstract data access (MongoDB)      |",
        "| **Use Case**     | `use_cases/`    | Encapsulate business logic          |",
        "| **Orchestrator** | `services/`     | Coordinate complex scraping processes |",
        "| **Container**    | `container/`    | Dependency injection for use cases  |",
        "| **Singleton**    | `ConfigLoader`  | Single instance for configuration   |",
        "| **Factory**      | `create_app()`  | Flask application factory           |",
        "| **Notification** | `notifications/`| Multi-channel notifications (Strategy pattern) |",
        "",
        "## 📄 License",
        "",
        "This project is licensed under the MIT License. See `LICENSE` file for details."
    ])

    readme_path = project_root / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(readme_content))

    print(f"✅ README.md successfully generated at: {readme_path}")
    print(f"📏 Total lines: {len(readme_content)}")


if __name__ == "__main__":
    main()
