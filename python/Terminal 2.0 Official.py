import os
import sys
import shutil
from time import sleep

# Попытка импортировать winsound (только для Windows)
try:
    import winsound
except ImportError:
    winsound = None


class HexOS:
    def __init__(self):
        self.data_path = "logs_data"
        self.current_language = 'en'
        self.current_user = None
        self.current_category = None
        self.in_logmode = False

        # Переводы (можно вынести в отдельный JSON файл)
        self.translations = {
            'en': {
                'system_start': "System start, please wait.",
                'terminal_version': "HexOS Terminal v2.0",
                'enter_username': "Please enter your username: ",
                'enter_password': "Please enter your password: ",
                'login_success': "User {username} successfully logged in",
                'logout_message': "User {user} logged out",
                'no_user_logged': "No user is currently logged in",
                'unknown_command': "Unknown command: '{cmd}'. Type 'cmds' for help.",
                'commands_title': "\n--- SYSTEM COMMANDS ---",
                'cmd_cmds': "cmds - Shows all commands",
                'cmd_stop': "stop - System shutdown",
                'cmd_logout': "logout - Logout from system",
                'cmd_logmode': "logmode - Enter log management mode",
                'system_stop': "System stop, please wait.",
                'logmode_enter': "Entering log management mode...",
                'logmode_exit': "Exiting log management mode.",
                'log_created': "Log '{logname}' created.",
                'category_created': "Category '{catname}' created.",
                'log_already_exists': "Log '{logname}' already exists.",
                'category_already_exists': "Category '{catname}' already exists.",
                'log_not_found': "Log '{logname}' not found.",
                'category_not_found': "Category '{catname}' not found.",
                'log_deleted': "Log '{logname}' deleted.",
                'category_deleted': "Category '{catname}' deleted.",
                'entered_category': "Entered category '{catname}'.",
                'exited_category': "Exited category.",
                'input_log_content': "Enter content for log '{logname}': ",
                'log_updated': "Log '{logname}' updated.",
                'current_category': "Current category: {catname}",
                'no_current_category': "No current category (root).",
                'logcmds_title': "\n--- LOG MODE COMMANDS ---",
                'cmd_mklog': "mklog <name> - Create log",
                'cmd_mkcat': "mkcat <name> - Create category",
                'cmd_edit': "edit <name> - Edit log",
                'cmd_enter': "enter <name> - Enter category",
                'cmd_exitcat': "exitcat - Exit category",
                'cmd_dellog': "dellog <name> - Delete log",
                'cmd_delcat': "delcat <name> - Delete category",
                'cmd_exit': "exit - Exit log mode",
                'cmd_logcmds': "logcmds - Show log commands",
                'cmd_viewlog': "viewlog <name> - View log",
                'log_content': "Content of '{logname}':",
                'cmd_listlogs': "listlogs - List all logs",
                'logs_list': "Available logs:",
                'no_logs_found': "No logs found.",
                'cmd_listcats': "listcats - List all categories",
                'categories_list': "Categories:",
                'no_categories_found': "No categories found.",
                'cmd_rename': "rename <old> <new> - Rename log",
                'log_renamed': "Log '{oldname}' renamed to '{newname}'."
            }
        }

    # --- Вспомогательные методы ---
    def t(self, key, **kwargs):
        """Краткий метод для получения перевода"""
        text = self.translations[self.current_language].get(key, key)
        return text.format(**kwargs)

    def beep(self, freq=750, dur=150):
        if winsound:
            winsound.Beep(freq, dur)

    def get_full_path(self, logname):
        """Централизованное управление путями к файлам"""
        if self.current_category:
            return os.path.join(self.data_path, self.current_category, f"{logname}.txt")
        return os.path.join(self.data_path, f"{logname}.txt")

    # --- Системные функции ---
    def boot(self):
        print(self.t('system_start'))
        steps = [
            "Loading HexOS...", "Checking system memory...", "Checking servers...",
            "Checking networks...", "Checking storage...", "Checking disks...",
            "Checking CPU...", "Checking RAM...", "Checking Python...",
            "Importing modules...", "Loading data..."
        ]
        for step in steps:
            print(step)
            self.beep()
            sleep(0.5)  # Ускорил загрузку для удобства, можно вернуть 1

        print("\nAll systems working correctly.")
        print(self.t('terminal_version'))
        print("Type 'cmds' to see all commands\n")
        self.beep(500, 500)

    def sys_stop(self, *args):
        print(self.t('system_stop'))
        self.beep()
        sleep(2)
        sys.exit()

    def login(self):
        user = input(self.t('enter_username'))
        pwd = input(self.t('enter_password'))
        self.current_user = user
        print(self.t('login_success', username=user))

    def logout(self, *args):
        if self.current_user:
            print(self.t('logout_message', user=self.current_user))
            self.current_user = None
        else:
            print(self.t('no_user_logged'))

    def show_cmds(self, *args):
        if not self.in_logmode:
            print(self.t('commands_title'))
            print(self.t('cmd_cmds'))
            print(self.t('cmd_stop'))
            print(self.t('cmd_logout'))
            print(self.t('cmd_logmode'))
            print(self.t('cmd_listlogs'))
            print(self.t('cmd_listcats'))
        else:
            print(self.t('logcmds_title'))
            print(self.t('cmd_mklog'))
            print(self.t('cmd_mkcat'))
            print(self.t('cmd_edit'))
            print(self.t('cmd_enter'))
            print(self.t('cmd_exitcat'))
            print(self.t('cmd_dellog'))
            print(self.t('cmd_delcat'))
            print(self.t('cmd_exit'))
            print(self.t('cmd_logcmds'))
            print(self.t('cmd_viewlog'))
            print(self.t('cmd_listlogs'))
            print(self.t('cmd_listcats'))
            print(self.t('cmd_rename'))

    # --- Работа с логами ---
    def mklog(self, args):
        if not args: return print("Usage: mklog <name>")
        name = args[0]
        path = self.get_full_path(name)
        if os.path.exists(path):
            print(self.t('log_already_exists', logname=name))
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("")
            print(self.t('log_created', logname=name))

    def mkcat(self, args):
        if not args: return print("Usage: mkcat <name>")
        name = args[0]
        path = os.path.join(self.data_path, name)
        if os.path.exists(path):
            print(self.t('category_already_exists', catname=name))
        else:
            os.makedirs(path)
            print(self.t('category_created', catname=name))

    def viewlog(self, args):
        if not args: return print("Usage: viewlog <name>")
        name = args[0]
        path = self.get_full_path(name)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                print(f"\n{self.t('log_content', logname=name)}\n{f.read()}\n")
        except FileNotFoundError:
            print(self.t('log_not_found', logname=name))

    def edit_log(self, args):
        if not args: return print("Usage: edit <name>")
        name = args[0]
        path = self.get_full_path(name)
        if not os.path.exists(path):
            return print(self.t('log_not_found', logname=name))

        content = input(self.t('input_log_content', logname=name))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(self.t('log_updated', logname=name))

    def enter_cat(self, args):
        if not args: return print("Usage: enter <name>")
        name = args[0]
        path = os.path.join(self.data_path, name)
        if os.path.isdir(path):
            self.current_category = name
            print(self.t('entered_category', catname=name))
        else:
            print(self.t('category_not_found', catname=name))

    def exit_cat(self, *args):
        self.current_category = None
        print(self.t('exited_category'))

    def dellog(self, args):
        if not args: return print("Usage: dellog <name>")
        path = self.get_full_path(args[0])
        if os.path.exists(path):
            os.remove(path)
            print(self.t('log_deleted', logname=args[0]))
        else:
            print(self.t('log_not_found', logname=args[0]))

    def delcat(self, args):
        if not args: return print("Usage: delcat <name>")
        path = os.path.join(self.data_path, args[0])
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(self.t('category_deleted', catname=args[0]))
            if self.current_category == args[0]:
                self.current_category = None
        else:
            print(self.t('category_not_found', catname=args[0]))

    def list_logs(self, *args):
        path = self.data_path if not self.current_category else os.path.join(self.data_path, self.current_category)
        files = [f[:-4] for f in os.listdir(path) if f.endswith('.txt')]
        if not files:
            print(self.t('no_logs_found'))
        else:
            print(self.t('logs_list'))
            for f in files: print(f"  - {f}")

    def list_cats(self, *args):
        cats = [d for d in os.listdir(self.data_path) if os.path.isdir(os.path.join(self.data_path, d))]
        if not cats:
            print(self.t('no_categories_found'))
        else:
            print(self.t('categories_list'))
            for c in cats:
                print(f"  Category: {c}")
                # Показываем содержимое категорий
                cat_path = os.path.join(self.data_path, c)
                logs = [f[:-4] for f in os.listdir(cat_path) if f.endswith('.txt')]
                for l in logs: print(f"    - {l}")

    def rename_log(self, args):
        if len(args) < 2: return print("Usage: rename <old> <new>")
        old_path = self.get_full_path(args[0])
        new_path = self.get_full_path(args[1])
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(self.t('log_renamed', oldname=args[0], newname=args[1]))
        else:
            print(self.t('log_not_found', logname=args[0]))

    # --- Основной цикл ---
    def run(self):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        self.boot()
        self.login()

        # Маппинг команд
        commands = {
            "stop": self.sys_stop,
            "logout": self.logout,
            "cmds": self.show_cmds,
            "logmode": self.toggle_logmode,
            "exit": self.exit_logmode,
            "mklog": self.mklog,
            "mkcat": self.mkcat,
            "edit": self.edit_log,
            "viewlog": self.viewlog,
            "enter": self.enter_cat,
            "exitcat": self.exit_cat,
            "dellog": self.dellog,
            "delcat": self.delcat,
            "listlogs": self.list_logs,
            "listcats": self.list_cats,
            "rename": self.rename_log,
            "logcmds": self.show_cmds
        }

        while True:
            if self.in_logmode:
                prefix = f"[{self.current_category or 'root'}]"
                print(
                    f"{prefix} {self.t('no_current_category' if not self.current_category else 'current_category', catname=self.current_category)}")

            try:
                user_input = input("> ").strip()
                if not user_input: continue

                parts = user_input.split()
                cmd_name = parts[0].lower()
                args = parts[1:]

                if not self.in_logmode:
                    if cmd_name in ["stop", "logout", "cmds", "logmode"]:
                        commands[cmd_name](args)
                    else:
                        print(self.t('unknown_command', cmd=cmd_name))
                else:
                    if cmd_name in commands:
                        commands[cmd_name](args)
                    else:
                        print(self.t('unknown_command', cmd=cmd_name))
            except KeyboardInterrupt:
                self.sys_stop()

    def toggle_logmode(self, *args):
        self.in_logmode = True
        print(self.t('logmode_enter'))

    def exit_logmode(self, *args):
        if self.in_logmode:
            self.in_logmode = False
            print(self.t('logmode_exit'))


if __name__ == "__main__":
    os_system = HexOS()
    os_system.run()
