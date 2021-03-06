# Generated by Django 2.2.20 on 2021-06-15 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lti1p3_tool_config', '0001_initial'),
        ('content_libraries', '0005_ltigradedresource_ltiprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentlibrary',
            name='lti_tool',
            field=models.ForeignKey(default=None, help_text="Authorize the  LTI tool selected to expose this library's content through LTI launches, leave unselected to disable LTI launches.", null=True, on_delete=django.db.models.deletion.SET_NULL, to='lti1p3_tool_config.LtiTool'),
        ),
        migrations.AlterField(
            model_name='ltiprofile',
            name='subject_id',
            field=models.CharField(help_text='Identifies the entity that initiated the launch request, commonly a user.', max_length=255, verbose_name='subject identifier'),
        ),
    ]
