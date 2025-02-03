from unittest.mock import patch
from django.core.management import call_command
from django.test import SimpleTestCase

from django.db.utils import OperationalError
from psycopg2.errors import OperationalError as PostgresOperationalError


# @patch("core.management.commands.wait_for_db.Command.check")
# class TestCommands(SimpleTestCase):


#     def test_db_ready(self, patched_result):
#         """Test to check when database service is already up."""

#         patched_result.return_value = True
#         call_command("wait_for_db")
#         self.assertEqual(patched_result.call_count, 1)
#         patched_result.asset_called_with(databases=["defafult"])

#     @patch("time.sleep")
#     def test_db_not_ready(self, patched_sleep, patched_result):
#         """Test to check if database service is not up."""

#         patched_result.side_effect = [OperationalError ]* 2 + [PostgresOperationalError ]* 2 + [True]
#         call_command("wait_for_db")
#         self.assertEqual(patched_result.call_count, 5)
#         patched_result.asset_called_with(databases=["defafult"])
