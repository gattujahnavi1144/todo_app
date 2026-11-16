import unittest

from app import app, tasks


class TaskTests(unittest.TestCase):
    def setUp(self):
        tasks.clear()
        self.client = app.test_client()
        self.task = {
            "task": "Prepare quarterly report",
            "priority": "High",
            "category": "Work",
            "due_date": "2026-12-01",
        }

    def tearDown(self):
        tasks.clear()

    def add_task(self, **changes):
        return self.client.post(
            "/", data={"action": "add", **self.task, **changes}
        )

    def test_form_has_required_fields(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        for field in self.task:
            self.assertRegex(html, rf'name="{field}"[^>]* required')
        self.assertIn('type="date"', html)
        self.assertIn("A clear slate.", html)

    def test_tasks_have_exact_keys_and_are_sorted_by_date(self):
        self.add_task(task="Later task", due_date="2027-01-01")
        self.add_task(task="Earlier task", due_date="2026-02-01")
        self.assertEqual(set(tasks[0]), set(self.task))
        self.assertEqual([task["task"] for task in tasks], ["Earlier task", "Later task"])
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn('<table class="task-table">', html)
        self.assertLess(html.index("Earlier task"), html.index("Later task"))
        for value in ("High", "Work", "2026-02-01"):
            self.assertIn(value, html)

    def test_all_priority_and_category_choices(self):
        for priority in ("High", "Medium", "Low"):
            for category in ("Work", "Personal", "Health"):
                with self.subTest(priority=priority, category=category):
                    response = self.add_task(priority=priority, category=category)
                    self.assertEqual(response.status_code, 302)
                    self.assertEqual(tasks[-1]["priority"], priority)
                    self.assertEqual(tasks[-1]["category"], category)

    def test_invalid_input_is_rejected_and_form_values_preserved(self):
        invalid_values = {
            "task": ("", "   ", "a" * 201),
            "priority": ("", "Urgent"),
            "category": ("", "Finance"),
            "due_date": ("", "not-a-date", "2026-02-30"),
        }
        for field, values in invalid_values.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    response = self.add_task(**{field: value})
                    self.assertEqual(response.status_code, 400)
                    self.assertIn(b'role="alert"', response.data)
                    self.assertEqual(tasks, [])
        response = self.add_task(priority="")
        self.assertIn(b'value="Prepare quarterly report"', response.data)

    def test_missing_fields_are_rejected(self):
        for field in self.task:
            with self.subTest(field=field):
                data = {"action": "add", **self.task}
                del data[field]
                self.assertEqual(self.client.post("/", data=data).status_code, 400)
                self.assertEqual(tasks, [])

    def test_delete_uses_sorted_row_and_removes_only_one_duplicate(self):
        self.add_task(task="Later task", due_date="2027-01-01")
        self.add_task(task="Earlier task", due_date="2026-02-01")
        self.add_task(task="Earlier task", due_date="2026-02-01")
        response = self.client.post("/", data={"action": "delete", "task_index": "0"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual([task["task"] for task in tasks], ["Earlier task", "Later task"])
        for index in ("-1", "99", "invalid", ""):
            with self.subTest(index=index):
                response = self.client.post(
                    "/", data={"action": "delete", "task_index": index}
                )
                self.assertEqual(response.status_code, 400)
                self.assertEqual(len(tasks), 2)

    def test_task_names_are_escaped(self):
        self.add_task(task="<script>alert(1)</script>")
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>", html)


if __name__ == "__main__":
    unittest.main()