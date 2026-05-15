import os
import sys
from pathlib import Path

from src.main.python.com.football.analyzer.data.infrastructure.adapters.web.app import create_app

project_root = Path(__file__).parent.absolute()
os.environ['FOOTBALL_ANALYZER_ROOT'] = str(project_root)
sys.path.insert(0, str(project_root / 'src' / 'main' / 'python'))
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
