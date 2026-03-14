from datetime import timedelta

from odoo.exceptions import ValidationError
from odoo.fields import Datetime
from odoo.tests.common import TransactionCase


class TestWorklogTimeEntry(TransactionCase):

    def setUp(self):
        super().setUp()
        self.project = self.env["worklog.project"].create({"name": "Test Project"})
        self.task = self.env["worklog.project.task"].create({"name": "Test Task"})
        self.entry = self.env["worklog.time.entry"].create({
            "name": "Test Entry",
            "task_id": self.task.id,
        })

    def test_action_start(self):
        self.entry.action_start()
        self.assertTrue(self.entry.is_running)
        self.assertFalse(self.entry.end_time)

    def test_action_stop(self):
        self.entry.action_start()
        self.entry.action_stop()
        self.assertFalse(self.entry.is_running)
        self.assertTrue(self.entry.end_time)

    def test_duration_computed(self):
        now = Datetime.now()
        self.entry.write({
            "start_time": now,
            "end_time": now + timedelta(hours=2),
        })
        self.assertAlmostEqual(self.entry.duration_hours, 2.0, places=1)

    def test_single_running_entry_constraint(self):
        self.entry.action_start()
        second = self.env["worklog.time.entry"].create({
            "name": "Second Entry",
            "task_id": self.task.id,
        })
        with self.assertRaises(ValidationError):
            second.write({"is_running": True})

    def test_time_order_constraint(self):
        now = Datetime.now()
        with self.assertRaises(ValidationError):
            self.entry.write({
                "start_time": now,
                "end_time": now - timedelta(hours=1),
            })

    def test_project_total_time(self):
        now = Datetime.now()
        self.entry.write({
            "start_time": now,
            "end_time": now + timedelta(hours=3),
        })
        self.assertAlmostEqual(self.project.total_time_hours, 3.0, places=1)
