#!/usr/bin/python3
""" Integration test """
# pylint: disable=invalid-name
import unittest
from unittest.mock import patch
import urllib.request
import os
import glob
from pathlib import Path
import tempfile
import zipfile
import sys
from ..__init__ import main
from .test_url_downloader import TestStaticHTTPServer

class TestIntegration(unittest.TestCase):
    """ Integration test """

    def setUp(self):
        """ Creates the sample HTTP server for the test """

        # Move to a temp directory where the backup will be saved
        self.__test_dir = tempfile.mkdtemp()
        os.chdir(self.__test_dir)

        # Store a reference to the original urlopen function, since we are going to replace it
        self.__original_urlopen = urllib.request.urlopen

        # Set up the fake HTTP server with local responses
        # pylint: disable=line-too-long
        route_responses = {
            "/https://api.todoist.com/sync/v8/sync?token=mysecrettoken&sync_token=%2A&resource_types=%5B%22projects%22%5D":
                Path(self.__get_test_file("sources/project_list.json")).read_bytes(),
            "/https://api.todoist.com/sync/v8/templates/export_as_file?token=mysecrettoken&project_id=2181147955":
                Path(self.__get_test_file("sources/Project_2181147955.csv")).read_bytes(),
            "/https://api.todoist.com/sync/v8/templates/export_as_file?token=mysecrettoken&project_id=2181147714":
                Path(self.__get_test_file("sources/Project_2181147714.csv")).read_bytes(),
            "/https://api.todoist.com/sync/v8/templates/export_as_file?token=mysecrettoken&project_id=2181147709":
                Path(self.__get_test_file("sources/Project_2181147709.csv")).read_bytes(),
            "/https://api.todoist.com/sync/v8/templates/export_as_file?token=mysecrettoken&project_id=2181147715":
                Path(self.__get_test_file("sources/Project_2181147715.csv")).read_bytes(),
            "/https://api.todoist.com/sync/v8/templates/export_as_file?token=mysecrettoken&project_id=2181147711":
                Path(self.__get_test_file("sources/Project_2181147711.csv")).read_bytes(),
            "/https://api.todoist.com/sync/v8/templates/export_as_file?token=mysecrettoken&project_id=2181147712":
                Path(self.__get_test_file("sources/Project_2181147712.csv")).read_bytes(),
            "/https://api.todoist.com/sync/v8/templates/export_as_file?token=mysecrettoken&project_id=2181147713":
                Path(self.__get_test_file("sources/Project_2181147713.csv")).read_bytes(),
            "/https://d1x0mwiac2rqwt.cloudfront.net/g75-kL8pwVYNObSczLnVXe4FIyJd8YQL6b8yCilGyix09bMdJmxbtrGMW9jIeIwJ/by/16542905/as/bug.txt":
                Path(self.__get_test_file("sources/bug.txt")).read_bytes(),
            "/https://d1x0mwiac2rqwt.cloudfront.net/s0snyb7n9tJXYijOK2LV6hjVar4YUkwYbHv3PBFYM-N4nJEtujC046OlEdZpKfZm/by/16542905/as/sample_image.png":
                Path(self.__get_test_file("sources/sample_image.png")).read_bytes(),
        }

        self.__httpd = TestStaticHTTPServer(("127.0.0.1", 33327), route_responses)

    def tearDown(self):
        """ Destroys the sample HTTP server for the test """
        self.__httpd.shutdown()

    def __urlopen_redirect_to_local(self, url):
        """ Replaces the urlopen function of URLLib, in order to redirect all requests
            to a local server.
            This way, we are still able to do the integration test with actual HTTP requests,
            though being handled by a local test HTTP server """
        return self.__original_urlopen("http://127.0.0.1:33327/" + url)

    @staticmethod
    def __get_test_file(subpath):
        """ Gets the path of one of the files required by the integration test """
        source_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(source_path, "integration_files", subpath)

    def __compare_zip_files(self, zip_path_1, zip_path_2):
        """ Compares the contents of the given two zip files """
        with zipfile.ZipFile(zip_path_1, 'r') as zip_file_1:
            with zipfile.ZipFile(zip_path_2, 'r') as zip_file_2:
                # Compare the list of file names
                name_list_1 = sorted(zip_file_1.namelist())
                name_list_2 = sorted(zip_file_2.namelist())
                self.assertEqual(name_list_1, name_list_2)

                # Compare the contents of every file
                for filename in name_list_1:
                    content_1 = zip_file_1.read(filename)
                    content_2 = zip_file_2.read(filename)
                    self.assertEqual(content_1, content_2)

    @patch.object(sys, 'argv', ["program", "download", "--with-attachments"])
    @patch.object(os, 'environ', {"TODOIST_TOKEN": "mysecrettoken",
                                  "TODOIST_EMAIL": "asd@asd.asd",
                                  "TODOIST_PASSWORD": "mysecretpassword"})
    @patch.object(urllib.request, 'urlopen')
    @unittest.skip("Not yet adapted to mock the attachment download workaround")
    def test_integration_download_with_attachments(self, mock_urlopen):
        """ Integration test for downloading the backup with attachments """

        # Arrange
        mock_urlopen.side_effect = self.__urlopen_redirect_to_local

        # Act
        main()

        # Arrange
        expected_file = self.__get_test_file("expected/TodoistBackupWAttach.zip")
        actual_file = glob.glob(os.path.join(self.__test_dir, "*"))[0]
        self.__compare_zip_files(expected_file, actual_file)

    @patch.object(sys, 'argv', ["program", "download"])
    @patch.object(os, 'environ', {"TODOIST_TOKEN": "mysecrettoken"})
    @patch.object(urllib.request, 'urlopen')
    def test_integration_download_without_attachments(self, mock_urlopen):
        """ Integration test for downloading the backup without attachments """

        # Arrange
        mock_urlopen.side_effect = self.__urlopen_redirect_to_local

        # Act
        main()

        # Arrange
        expected_file = self.__get_test_file("expected/TodoistBackupNoAttach.zip")
        actual_file = glob.glob(os.path.join(self.__test_dir, "*"))[0]
        self.__compare_zip_files(expected_file, actual_file)
