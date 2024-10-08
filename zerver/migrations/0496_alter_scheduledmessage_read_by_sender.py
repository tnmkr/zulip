# Generated by Django 4.2.8 on 2023-12-14 06:18

from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps
from django.db.models import F, Q
from django.db.models.functions import Lower


def populate_read_by_sender(apps: StateApps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    ScheduledMessage = apps.get_model("zerver", "ScheduledMessage")
    ScheduledMessage.objects.annotate(
        sending_client_name_lower=Lower("sending_client__name")
    ).filter(
        Q(
            sending_client_name_lower__in=(
                "zulipandroid",
                "zulipios",
                "zulipdesktop",
                "zulipmobile",
                "zulipelectron",
                "zulipterminal",
                "snipe",
                "website",
                "ios",
                "android",
            )
        )
        | Q(sending_client_name_lower__contains="desktop app"),
        ~Q(recipient=F("sender__recipient")),
        read_by_sender=None,
    ).update(read_by_sender=True)
    ScheduledMessage.objects.filter(read_by_sender=None).update(read_by_sender=False)


class Migration(migrations.Migration):
    dependencies = [
        ("zerver", "0495_scheduledmessage_read_by_sender"),
    ]

    operations = [
        migrations.RunPython(
            populate_read_by_sender,
            reverse_code=migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.AlterField(
            model_name="scheduledmessage",
            name="read_by_sender",
            field=models.BooleanField(),
        ),
    ]
