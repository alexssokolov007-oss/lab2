from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / 'src'

HISTORY_FILE = PROJECT_ROOT / '.history'
TRASH_DIR = PROJECT_ROOT / '.trash'

LOG_DIR = PROJECT_ROOT
LOG_PATH = LOG_DIR / 'shell.log'
LOG_MAX_SIZE = 1_000_000
LOG_BACKUP_COUNT = 3
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

MAX_FILE_SIZE = 10 * 1024 * 1024
HISTORY_LIMIT = 100

SYSTEM_ROOT = Path(PROJECT_ROOT.anchor) if PROJECT_ROOT.anchor else Path('/')
PROTECTED_DIRS = [SYSTEM_ROOT, PROJECT_ROOT, PROJECT_ROOT.parent, Path.home()]

DATE_FORMAT = '%d %b %H:%M'
