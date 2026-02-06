from django.test import TestCase

# Create your tests here.

from posts.singletons.config_manager import ConfigManager
from posts.singletons.logger_singleton import LoggerSingleton
import logging

# config1 = ConfigManager()
# config2 = ConfigManager()

# assert config1 is config2   #both instances should be the same
# config1.set_setting("DEFAULT_PAGE_SIZE", 50)
# assert config2.get_setting("DEFAULT_PAGE_SIZE") == 50


class ConfigManagerTest(TestCase):

    def test_singleton_instance(self):
        config1 = ConfigManager()
        config2 = ConfigManager()

        self.assertIs(config1, config2)

    def test_shared_settings(self):
        config1 = ConfigManager()
        config2 = ConfigManager()

        config1.set_setting("DEFAULT_PAGE_SIZE", 50)

        self.assertEqual(
            config2.get_setting("DEFAULT_PAGE_SIZE"),
            50
        )


    # def test_singleton_instance(self):
    #     logger1 = LoggerSingleton()
    #     logger2 = LoggerSingleton()

    #     self.assertIs(logger1, logger2)

    # def test_returns_logger(self):
    #     logger1 = LoggerSingleton()
    #     logger2 = logger1.get_logger()

    #     self.assertIsInstance(logger1, logger2)

    # def test_logger_name(self):
    #     logger1 = LoggerSingleton()
    #     logger2 = logger1.get_logger()

    #     self.assertEqual(self.logger.name, "connectly_logger")

    # def test_logger_level(self):
    #     logger1 = LoggerSingleton()
    #     logger2 = logger1.get_logger()

    #     self.assertEqual(self.logger.level, logging.INFO)
