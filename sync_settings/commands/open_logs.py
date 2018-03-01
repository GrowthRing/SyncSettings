import sublime_plugin
from ..libs import logger


class SyncSettingsOpenLogsCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.open_file(logger.logger_path)
