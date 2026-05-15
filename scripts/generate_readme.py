import os
from pathlib import Path


def generate_directory_tree(start_path, prefix=""):
    tree_lines = []

    try:
        items = sorted(os.listdir(start_path))
    except PermissionError:
        return tree_lines

    items = [item for item in items if not item.startswith('.') and item != '__pycache__']

    for i, item in enumerate(items):
        item_path = os.path.join(start_path, item)
        is_last = (i == len(items) - 1)

        connector = "└── " if is_last else "├── "

        if os.path.isdir(item_path):
            rel_path = os.path.relpath(item_path, Path(__file__).parent.parent)
            if any(rel_path.startswith(p) for p in ["src", "tests"]) or start_path.endswith(("src", "tests")):
                tree_lines.append(f"{prefix}{connector}{item}/")
                extension = "    " if is_last else "│   "
                tree_lines.extend(generate_directory_tree(item_path, prefix + extension))
        else:
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
        "- **`use_cases/`**: Use cases orchestrating business logic",
        "",
        "### **Infrastructure Layer** (`src/main/python/com/football/analyzer/infrastructure/`)",
        "- **`adapters/`**: Concrete implementations of ports",
        "  - `repositories/`: Repository adapters",
        "  - `services/`: Service adapters",
        "  - `extractors/`: Data extraction strategies",
        "  - `mappers/`: Entity-DTO mappers",
        "",
        "## 🚀 Installation & Usage",
        "",
        "# 1. Install dependencies",
        "pip install -r requirements.txt",
        "pip install -r requirements-dev.txt  # Development dependencies",
        "```",
        "",
        "```",
        "",
        "## 🛠️ Technologies Used",
        "",
        "- **Python 3.10+** - Main language",
        "- **BeautifulSoup4** - HTML parsing",
        "- **pytest** - Testing framework",
        "- **pytest-cov** - Test coverage",
        "- **lxml** - Fast XML/HTML parser",
        "- **unittest.mock** - Mocking for tests",
        "",
        "## 📝 Design Patterns Implemented",
        "",
        "| Pattern          | Location        | Purpose                             |",
        "|------------------|-----------------|-------------------------------------|",
        "| **Strategy**     | `extractors/`   | Swap HTML extraction strategies     |",
        "| **Adapter**      | `adapters/`     | Adapt external interfaces to domain |",
        "| **Repository**   | `repositories/` | Abstract data access                |",
        "| **Mapper**       | `mappers/`      | Convert between entities and DTOs   |",
        "| **Use Case**     | `use_cases/`    | Encapsulate business logic          |",
        "| **Orchestrator** | `services/`     | Coordinate complex processes        |",
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
