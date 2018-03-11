#!/usr/bin/python3
""" Tests for the runtime dependency injection container """
# pylint: disable=invalid-name
import unittest
from ..runtime import RuntimeControllerDependencyInjector

class TestRuntime(unittest.TestCase):
    """ Tests for the runtime dependency injection container """

    def test_runtime_dependency_injector_caches_values(self):
        """ Tests that the DI container always returns the same (valid) instances for the
            dependencies instead of creating new ones every call """
        # Arrange

        # Act
        runtimedi = RuntimeControllerDependencyInjector("1234", True)
        tracer1 = runtimedi.tracer
        tracer2 = runtimedi.tracer
        todoist_api1 = runtimedi.todoist_api
        todoist_api2 = runtimedi.todoist_api
        backup_downloader1 = runtimedi.backup_downloader
        backup_downloader2 = runtimedi.backup_downloader
        backup_attachments_dl1 = runtimedi.backup_attachments_downloader
        backup_attachments_dl2 = runtimedi.backup_attachments_downloader

        # Assert
        self.assertIs(tracer1, tracer2)
        self.assertIsNotNone(tracer1)
        self.assertIs(todoist_api1, todoist_api2)
        self.assertIsNotNone(todoist_api1)
        self.assertIs(backup_downloader1, backup_downloader2)
        self.assertIsNotNone(backup_downloader1)
        self.assertIs(backup_attachments_dl1, backup_attachments_dl2)
        self.assertIsNotNone(backup_attachments_dl1)
