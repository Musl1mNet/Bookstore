from django.core.management.base import BaseCommand
from telegram.ext import Updater
from django.conf import settings
from datetime import datetime
import pathlib
import time

class Command(BaseCommand):

    def handle(self, *args, **options):
        updater = Updater(settings.TELEGRAM_BOT_TOKEN)
        all_app_stat = dict()
        for app in settings.INSTALLED_APPS:
            if "." in app:
                continue
            files = pathlib.Path(settings.BASE_DIR / app).rglob("*.py")
            apps_stat = {app: {"total_lines": 0, "total_files": 0}}
            total_lines = 0
            total_files = 0
            for file in files:
                with open(f"{file}", "r") as f:
                    for n_line, kms in enumerate(f, 1):
                        pass
                total_lines += n_line
                total_files += 1
            apps_stat[app]["total_lines"] = total_lines
            apps_stat[app]["total_files"] = total_files
            total_lines, total_files = 0, 0
            all_app_stat.update(apps_stat)
        for key, val in all_app_stat.items():
            print(f"App nomi {str(key).upper()}\nJami fayllar {val['total_files']} ta\nJami kodlar {val['total_lines']} qator")
        files_mtime = {}
        is_scan = True
        while True:
            cp_mtime = files_mtime.copy()

            for app in settings.INSTALLED_APPS:
                if "." in app:
                    continue
                files = list(pathlib.Path(settings.BASE_DIR / app).rglob("*.py"))
                for f in files:
                    st = f.lstat()
                    mtime = datetime.fromtimestamp(st.st_mtime)
                    mtime_str = f"{mtime:%d.%m.%Y %H:%M:%S}"
                    if is_scan:
                        pass
                    elif f.name not in files_mtime:
                        updater.bot.send_message(chat_id=settings.CHAT_ID,
                                                 text=f"{f.parent.name} ga {f.name} nomli fayl qo'shildi")
                    elif files_mtime[f.name] != mtime_str:
                        updater.bot.send_message(chat_id=settings.CHAT_ID,
                                                 text=f"{f.parent.name} dagi {f.name} faylda o'zgarish")
                    files_mtime[f.name] = mtime_str
                    if f.name in cp_mtime:
                        del cp_mtime[f.name]
            is_scan = False
            if cp_mtime:
                for del_f, _ in cp_mtime.items():
                    updater.bot.send_message(chat_id=settings.CHAT_ID,
                                             text=f"{del_f} fayl o'chirildi")
                    del cp_mtime[del_f]

            time.sleep(1)
