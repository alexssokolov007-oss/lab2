import json
import shutil
from datetime import datetime
from pathlib import Path
from src.constants import HISTORY_FILE, TRASH_DIR


class HistoryManager:
    def __init__(self, history_file=None, trash_dir=None, shutil_module=shutil):
        self.history_file = history_file or HISTORY_FILE
        self.trash_dir = trash_dir or TRASH_DIR
        self.shutil = shutil_module
        self.history = []
        self.load_history()
        self.trash_dir.mkdir(exist_ok=True)

    def load_history(self):
        '''Загружает историю из файла'''
        if self.history_file.exists():
            try:
                self.history = json.loads(self.history_file.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, Exception):
                self.history = []

    def save_history(self):
        '''Сохраняет историю в файл'''
        self.history_file.write_text(
            json.dumps(self.history[-100:], ensure_ascii=False, indent=2), encoding='utf-8')

    def add_command(self, command, operation_type=None, source=None, destination=None):
        '''Добавляет команду в историю'''
        e = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'command': command,
            'type': operation_type,
            'source': source,
            'destination': destination
        }
        self.history.append(e)
        self.save_history()

    def show_history(self, count=10, print_func=print):
        '''Показывает историю команд'''
        if not self.history:
            print_func('История пуста')
            return

        recent = self.history[-count:] if count else self.history
        print_func(f'Последние {len(recent)} команд:')

        for i, e in enumerate(recent, 1):
            idx = len(self.history) - len(recent) + i
            time = e['timestamp'][11:19]
            print_func(f"{idx}. [{time}] {e['command']}")

    def undo_last(self, print_func=print):
        '''Отменяет последнюю операцию'''
        for i in range(len(self.history) - 1, -1, -1):
            entry = self.history[i]
            if entry['type'] in ['cp', 'mv', 'rm']:
                return self.undo_operation(entry, i, print_func)

        msg = 'Ошибка: нет операций для отмены'
        print_func(msg)
        return msg

    def undo_operation(self, e, index, print_func):
        '''Отменяет конкретную операцию'''
        try:
            op_type = e['type']
            src, dst = e.get('source'), e.get('destination')

            if op_type == 'cp' and dst and Path(dst).exists():
                self.safe_remove(Path(dst))
                print_func(f'Отменено копирование: удален {dst}')

            elif op_type == 'mv' and src and dst:
                if Path(dst).exists():
                    self.shutil.move(dst, src)
                    print_func(f'Отменено перемещение: {dst} → {src}')

            elif op_type == 'rm' and src:
                trash_path = self.trash_dir / Path(src).name

                if trash_path.exists():
                    if Path(src).exists():
                        counter = 1
                        while True:
                            new_path = Path(src).parent / f'{Path(src).stem}_{counter}{Path(src).suffix}'
                            if not new_path.exists():
                                self.shutil.move(str(trash_path), str(new_path))
                                print_func(f'Восстановлено как: {new_path.name}')
                                break
                            counter += 1
                    else:
                        self.shutil.move(str(trash_path), src)
                        print_func(f'Восстановлено: {src}')

            self.history.pop(index)
            self.save_history()
            return 'Успешно'

        except Exception as ex:
            msg = f'Ошибка при отмене: {ex}'
            print_func(msg)
            return msg

    def safe_remove(self, path):
        '''Безопасно удаляет файл или директорию (перемещает в корзину)'''
        path_obj = Path(path)
        trash_path = self.trash_dir / path_obj.name

        cnt = 1
        while trash_path.exists():
            trash_path = self.trash_dir / f'{path_obj.stem}_{cnt}{path_obj.suffix}'
            cnt += 1
        self.shutil.move(str(path_obj), str(trash_path))

history_manager = HistoryManager()


def show_history(count=10):
    '''Показывает историю команд'''
    history_manager.show_history(count)
    return 'Успешно'


def undo_last():
    '''Отменяет последнюю операцию'''
    return history_manager.undo_last()


def safe_remove(path):
    '''Безопасно удаляет файл или директорию (перемещает в корзину)'''
    history_manager.safe_remove(path)


def clear_trash():
    '''Очищает корзину (.trash)'''
    try:
        if TRASH_DIR.exists():
            shutil.rmtree(TRASH_DIR)
            TRASH_DIR.mkdir(exist_ok=True)
            return 'Корзина очищена'
        return 'Корзина пуста'
    except Exception as e:
        return f'Ошибка при очистке: {e}'