from celery import shared_task

# don't forgot to use the decorator
@shared_task
def hello_task(name):
    print(f"hello{name}. you will get {len(name)} amount of bamboo in your a$$")
    