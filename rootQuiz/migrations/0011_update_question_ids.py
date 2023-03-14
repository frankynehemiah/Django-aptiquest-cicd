from django.db import migrations
import uuid

def update_question_ids(apps, schema_editor):
    Question = apps.get_model('rootQuiz', 'Question')
    for question in Question.objects.all():
        question.questionID = uuid.uuid4()
        question.save()

class Migration(migrations.Migration):

    dependencies = [
        ('rootQuiz', '0010_question_number'),
    ]

    operations = [
        migrations.RunPython(update_question_ids),
    ]
