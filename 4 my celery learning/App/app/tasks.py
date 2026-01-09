from celery import shared_task
from django.apps import apps

@shared_task
def delete_marked_basicapp():
    BasicApp = apps.get_model('app', 'BasicApp')  # lazy import avoids circular import
    # Get the first marked record and delete it
    marked_record = BasicApp.objects.filter(is_deleted=True).first()
    if marked_record:
        deleted_count, _ = marked_record.delete()
        print(f"Deleted {deleted_count} marked BasicApp record: {marked_record}")
    else:
        deleted_count = 0
        print("No marked BasicApp records found to delete")
    return deleted_count
