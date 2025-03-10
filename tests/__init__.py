import logging
import sys
import importlib.util
from typing import List, Tuple

def check_dependencies() -> Tuple[bool, List[str]]:
    """Check required dependencies"""
    required = [
        'psutil',
        'cv2',
        'torch',
        'numpy',
        'matplotlib',
        'PIL'
    ]
    
    missing = []
    for package in required:
        if importlib.util.find_spec(package) is None:
            missing.append(package)
            
    return len(missing) == 0, missing

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

# Check dependencies before running tests
deps_ok, missing_deps = check_dependencies()
if not deps_ok:
    logger.error(f"Missing required dependencies: {', '.join(missing_deps)}")
    logger.error("Please run: pip install -r requirements.txt")
    sys.exit(1)

logger.info("All required dependencies found")
