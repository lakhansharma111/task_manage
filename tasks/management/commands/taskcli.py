# tasks/management/commands/taskcli.py
from django.core.management.base import BaseCommand
from tasks.models import Task
from datetime import datetime

class Command(BaseCommand):
    help = "CLI to manage tasks (CRUD operations)"

    def add_arguments(self, parser):
        parser.add_argument("action", choices=["list", "create", "update", "delete", "complete", "incomplete"])
        parser.add_argument("--id", type=int)
        parser.add_argument("--title")
        parser.add_argument("--description")
        parser.add_argument("--priority", choices=["low", "medium", "high"])
        parser.add_argument("--due_date")

    def handle(self, *args, **options):
        action = options["action"]

        if action == "list":
            tasks = Task.objects.all().order_by("-created_at")
            for t in tasks:
                self.stdout.write(f"[{t.id}] {'✓' if t.completed else ' '} {t.title} ({t.priority}) — Due: {t.due_date}")
        elif action == "create":
            t = Task.objects.create(
                title=options["title"],
                description=options.get("description", ""),
                priority=options.get("priority", "medium"),
                due_date=options.get("due_date"),
            )
            self.stdout.write(f"Created task #{t.id}: {t.title}")
        elif action == "update":
            t = Task.objects.get(id=options["id"])
            for field in ["title", "description", "priority", "due_date"]:
                if options.get(field):
                    setattr(t, field, options[field])
            t.save()
            self.stdout.write(f"Updated task #{t.id}")
        elif action == "delete":
            Task.objects.filter(id=options["id"]).delete()
            self.stdout.write("Task deleted.")
        elif action == "complete":
            t = Task.objects.get(id=options["id"])
            t.completed = True
            t.save()
            self.stdout.write("Task marked complete.")
        elif action == "incomplete":
            t = Task.objects.get(id=options["id"])
            t.completed = False
            t.save()
            self.stdout.write("Task marked incomplete.")
# tasks/management/commands/taskcli.py
from django.core.management.base import BaseCommand, CommandError
from tasks.models import Task
from datetime import datetime

class Command(BaseCommand):
    help = "CLI to manage tasks (CRUD operations with validation and error handling)"

    def add_arguments(self, parser):
        parser.add_argument(
            "action",
            choices=["list", "create", "update", "delete", "complete", "incomplete"],
            help="Action to perform"
        )
        parser.add_argument("--id", type=int, help="Task ID for update/delete/complete")
        parser.add_argument("--title", type=str, help="Title of the task")
        parser.add_argument("--description", type=str, help="Description of the task")
        parser.add_argument("--priority", choices=["low", "medium", "high"], help="Priority of the task")
        parser.add_argument("--due_date", type=str, help="Due date in YYYY-MM-DD format")

    def handle(self, *args, **options):
        try:
            action = options["action"]

            if action == "list":
                self.list_tasks()

            elif action == "create":
                self.create_task(options)

            elif action == "update":
                self.update_task(options)

            elif action == "delete":
                self.delete_task(options)

            elif action == "complete":
                self.mark_complete(options, True)

            elif action == "incomplete":
                self.mark_complete(options, False)

        except CommandError as e:
            self.stderr.write(self.style.ERROR(f"Error: {str(e)}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected Error: {str(e)}"))

    # ---------------------- ACTION HANDLERS ----------------------

    def list_tasks(self):
        tasks = Task.objects.all().order_by("-created_at")
        if not tasks:
            self.stdout.write(self.style.WARNING("No tasks found."))
            return

        self.stdout.write(self.style.SUCCESS("Task List:"))
        for t in tasks:
            status = "✓" if t.completed else " "
            due = t.due_date or "-"
            self.stdout.write(
                f"[{t.id}] {status} {t.title} ({t.priority}) — Due: {due} | Created: {t.created_at.strftime('%Y-%m-%d')}"
            )

    def create_task(self, options):
        title = options.get("title")
        if not title:
            raise CommandError("Title is required for creating a task.")

        description = options.get("description", "")
        priority = options.get("priority", "medium")
        due_date_str = options.get("due_date")

        # Validate due_date format
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError:
                raise CommandError("Invalid due_date format. Use YYYY-MM-DD.")

        task = Task.objects.create(
            title=title.strip(),
            description=description.strip(),
            priority=priority,
            due_date=due_date
        )
        self.stdout.write(self.style.SUCCESS(f"✅ Created task #{task.id}: {task.title}"))

    def update_task(self, options):
        task_id = options.get("id")
        if not task_id:
            raise CommandError("Task ID (--id) is required to update a task.")

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise CommandError(f"Task with ID {task_id} not found.")

        updated_fields = []
        for field in ["title", "description", "priority", "due_date"]:
            value = options.get(field)
            if value:
                if field == "due_date":
                    try:
                        value = datetime.strptime(value, "%Y-%m-%d").date()
                    except ValueError:
                        raise CommandError("Invalid due_date format. Use YYYY-MM-DD.")
                setattr(task, field, value)
                updated_fields.append(field)

        if not updated_fields:
            raise CommandError("No update fields provided.")

        task.save()
        self.stdout.write(self.style.SUCCESS(f"✏️ Updated task #{task.id}: {', '.join(updated_fields)}"))

    def delete_task(self, options):
        task_id = options.get("id")
        if not task_id:
            raise CommandError("Task ID (--id) is required to delete a task.")

        deleted, _ = Task.objects.filter(id=task_id).delete()
        if deleted:
            self.stdout.write(self.style.SUCCESS(f"🗑️ Deleted task #{task_id}."))
        else:
            raise CommandError(f"Task with ID {task_id} not found.")

    def mark_complete(self, options, status: bool):
        task_id = options.get("id")
        if not task_id:
            raise CommandError("Task ID (--id) is required to mark complete/incomplete.")

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise CommandError(f"Task with ID {task_id} not found.")

        if task.completed == status:
            msg = "already completed" if status else "already incomplete"
            raise CommandError(f"Task #{task_id} is {msg}.")

        task.completed = status
        task.save()
        action = "✅ Marked complete" if status else "❌ Marked incomplete"
        self.stdout.write(self.style.SUCCESS(f"{action}: #{task_id} - {task.title}"))
