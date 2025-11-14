import zipfile
import tarfile
from pathlib import Path
from src.errors import validate_path_exists


class ArchiveManager:
    def __init__(self, zip_module=zipfile, tar_module=tarfile):
        self.zipfile = zip_module
        self.tarfile = tar_module

    def zip_folder(self, folder_path: str, archive_name: str = None) -> str:
        '''Создает ZIP архив из папки'''
        folder = Path(folder_path)
        validate_path_exists(folder)

        if not folder.is_dir():
            raise ValueError(f"'{folder_path}' не является папкой")

        if not archive_name:
            archive_name = f"{folder.name}.zip"

        with self.zipfile.ZipFile(archive_name, 'w', self.zipfile.ZIP_DEFLATED) as zip_file:
            for file_item in folder.rglob('*'):
                if file_item.is_file():
                    zip_file.write(file_item, file_item.relative_to(folder))
                else:
                    arcname = file_item.relative_to(folder) / ''
                    zip_file.writestr(str(arcname), '')

        return 'Успешно'

    def unzip_archive(self, archive_path: str) -> str:
        '''Распаковывает ZIP архив'''
        archive = Path(archive_path)
        validate_path_exists(archive)

        with self.zipfile.ZipFile(archive, 'r') as zip_file:
            zip_file.extractall()

        return 'Успешно'

    def tar_folder(self, folder_path: str, archive_name: str) -> str:
        '''Создает TAR.GZ архив из папки'''
        folder = Path(folder_path)
        validate_path_exists(folder)

        if not folder.is_dir():
            raise ValueError(f"'{folder_path}' не является папкой")

        with self.tarfile.open(archive_name, 'w:gz') as tar_file:
            tar_file.add(folder, arcname=folder.name)

        return 'Успешно'

    def untar_archive(self, archive_path: str) -> str:
        '''Распаковывает TAR.GZ архив'''
        archive = Path(archive_path)
        validate_path_exists(archive)

        with self.tarfile.open(archive, 'r:gz') as tar_file:
            try:
                tar_file.extractall(filter='data')
            except TypeError:
                tar_file.extractall()

        return 'Успешно'


archive_manager = ArchiveManager()

# Функции для обратной совместимости
def zip_folder(folder_path: str, archive_name: str = None) -> str:
    return archive_manager.zip_folder(folder_path, archive_name)

def unzip_archive(archive_path: str) -> str:
    return archive_manager.unzip_archive(archive_path)

def tar_folder(folder_path: str, archive_name: str) -> str:
    return archive_manager.tar_folder(folder_path, archive_name)

def untar_archive(archive_path: str) -> str:
    return archive_manager.untar_archive(archive_path)