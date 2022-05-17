# Generated by Django 3.2.13 on 2022-04-23 23:14
import os

from django.db import migrations
import yaml


def create_status(apps, schedma_editor):
    """Initial subset of statuses."""

    statuses = ["active", "staged", "decommissioned"]
    ContentType = apps.get_model("contenttypes.ContentType")
    for i in statuses:
        status = apps.get_model("extras.Status").objects.get(slug=i)
        for model in apps.app_configs["nautobot_firewall_models"].get_models():
            ct = ContentType.objects.get_for_model(model)
            status.content_types.add(ct)


def create_default_objects(apps, schema_editor):
    """Initial subset of commonly used objects."""
    defaults = os.path.join(os.path.dirname(__file__), "services.yml")
    with open(defaults, "r") as f:
        services = yaml.safe_load(f)
    status = apps.get_model("extras.Status").objects.get(slug="active")

    apps.get_model("nautobot_firewall_models.AddressObjectGroup").objects.create(
        name="ANY", status=status, description="Used to signify ANY AddressObject."
    )
    apps.get_model("nautobot_firewall_models.UserObjectGroup").objects.create(
        name="ANY", status=status, description="Used to signify ANY UserObject."
    )
    apps.get_model("nautobot_firewall_models.ServiceObjectGroup").objects.create(
        name="ANY", status=status, description="Used to signify ANY ServiceObject."
    )
    for i in services:
        apps.get_model("nautobot_firewall_models.ServiceObject").objects.create(status=status, **i)


class Migration(migrations.Migration):

    dependencies = [
        ("extras", "0033_add__optimized_indexing"),
        ("nautobot_firewall_models", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(code=create_status),
        migrations.RunPython(code=create_default_objects),
    ]
