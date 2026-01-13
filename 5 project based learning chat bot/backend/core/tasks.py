from celery import shared_task


@shared_task
def handle_ai_request_job(ai_request_id):
    from .models import AiRequest
    AiRequest.objects.get(id=ai_request_id).handle()

@shared_task
def handle_ai_session_title_name(session_id):
    from .models import AiChatSession
    AiChatSession.objects.get(id=session_id).handle()

@shared_task
def hello_task(name):
    print(f"Hello {name}. You have {len(name)} characters in your name.")

