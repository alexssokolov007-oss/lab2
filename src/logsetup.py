import logging
from logging.handlers import RotatingFileHandler
from src.constants import LOG_DIR, LOG_PATH, LOG_MAX_SIZE, LOG_BACKUP_COUNT, LOG_DATE_FORMAT

def setup_logging(log_dir=None, log_path=None, logger_name='shell'):
    '''Настраивает логирование'''
    logger = logging.getLogger(logger_name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_dir_obj = log_dir or LOG_DIR
    log_path_obj = log_path or LOG_PATH
    
    log_dir_obj.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_path_obj, 
        maxBytes=LOG_MAX_SIZE, 
        backupCount=LOG_BACKUP_COUNT, 
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(levelname)s %(message)s', 
        datefmt=LOG_DATE_FORMAT
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.propagate = False
    
    return logger