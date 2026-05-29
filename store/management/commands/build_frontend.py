import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Собирает Vite/React из FRONTEND_SOURCE_ROOT в static/frontend/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--if-missing",
            action="store_true",
            help="Пропустить сборку, если уже есть static/frontend/index.html",
        )

    def handle(self, *args, **options):
        if_missing = options["if_missing"]
        root: Path = settings.FRONTEND_SOURCE_ROOT
        if not root.is_dir():
            raise CommandError(f"Папка фронтенда не найдена: {root}")

        out_index = Path(settings.BASE_DIR) / "static" / "frontend" / "index.html"
        if if_missing and out_index.is_file():
            self.stdout.write(self.style.SUCCESS("Витрина уже собрана."))
            return

        npm = shutil.which("npm")
        if not npm:
            raise CommandError("npm не найден в PATH. Установите Node.js LTS.")

        lock = root / "package-lock.json"
        install_cmd = [npm, "ci", "--no-audit"] if lock.is_file() else [npm, "install", "--no-audit"]
        self.stdout.write(self.style.NOTICE(f"{' '.join(install_cmd)} (cwd={root})"))
        r = subprocess.run(install_cmd, cwd=str(root), shell=False)
        if r.returncode != 0:
            raise CommandError("npm install завершился с ошибкой.")

        self.stdout.write(self.style.NOTICE("npm run build"))
        r = subprocess.run([npm, "run", "build"], cwd=str(root), shell=False)
        if r.returncode != 0:
            raise CommandError("npm run build завершился с ошибкой.")

        if not out_index.is_file():
            raise CommandError(f"Не найден {out_index} после сборки.")

        self.stdout.write(self.style.SUCCESS("Готово: static/frontend/"))
