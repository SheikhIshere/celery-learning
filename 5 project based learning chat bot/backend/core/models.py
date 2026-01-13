# app/models.py
import os
import uuid
from google import genai

from django.db import models
from django.utils import timezone

import re

class Recipe(models.Model):
    """Represents a recipe in the system."""
    name = models.CharField(max_length=255)
    steps = models.TextField()

    def __str__(self):
        return self.name

class AiChatSession(models.Model):
    """Tracks an AI chat session."""
    title = models.CharField(max_length=255, blank=True)
    messages = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _queue_job(self):
        """Schedule background AI title generation."""
        from .tasks import handle_ai_session_title_name
        # pass id as positional arg for simplicity
        handle_ai_session_title_name.delay(self.id)

    def _conversation_text(self) -> str:
        """Render messages into a readable conversation string for the model prompt."""
        parts = []
        for m in self.messages:
            user = m.get("message", "")
            bot = m.get("response", "")
            parts.append(f"User: {user}")
            if bot:
                parts.append(f"Assistant: {bot}")
        return "\n".join(parts).strip()

    def handle(self):
        """Main engine to generate a short title (run inside Celery worker)."""
        try:
            client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
            model_name = "gemma-3-27b-it"

            conversation_text = self._conversation_text() or "No conversation text available."

            prompt = (
                "You are a title generator.\n"
                "Return ONLY a short title following these STRICT rules:\n"
                "- Exactly 4 or5 words\n"
                "- No punctuation or quotation marks\n"
                "- No prefixes like 'Title:' or any explanations\n"
                "- Output plain text only\n\n"
                f"Conversation:\n{conversation_text}\n"
            )

            result = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            # defensive text extraction
            raw = None
            if hasattr(result, "text"):
                raw = result.text
            elif isinstance(result, dict):
                raw = result.get("text") or result.get("output") or result.get("result")
                if isinstance(raw, list) and raw:
                    raw = raw[0] if not isinstance(raw[0], dict) else raw[0].get("content") or ""
            raw = (raw or "").strip()

            # sanitize: remove newlines, prefixes, punctuation; keep first 3 words
            raw = raw.splitlines()[0].strip()
            raw = re.sub(r'^(title[:\s\-]+)', '', raw, flags=re.IGNORECASE).strip()
            raw = re.sub(r'[^\w\s]', '', raw)  # remove punctuation
            words = [w for w in raw.split() if w]
            if not words:
                # fallback to uuid short
                cleaned = f"New Chat {uuid.uuid4().hex[:4]}"
            else:
                cleaned = " ".join(words[:3]).title()  # 2-3 words, title-cased

            # persist the cleaned title (trim to 255)
            self.title = cleaned[:255]
            self.save(update_fields=["title", "updated_at"])

        except Exception as exc:
            # not silent — helps debugging in logs
            print("AiChatSession.handle() failed:", exc)

    def add_message(self, message, response, created_at=None):
        """Add a message to the session history and queue AI title generation once."""
        if created_at is None:
            created_at = timezone.now()

        is_first_message = len(self.messages) == 0

        next_count = len(self.messages) + 1
        self.messages.append({
            "count": next_count,
            "message": message,
            "response": response,
            "created_at": created_at.isoformat() if hasattr(created_at, "isoformat") else str(created_at),
        })

        # instant fallback title (first message only)
        if is_first_message and message:
            # short immediate title so UX feels responsive
            self.title = str(message).strip()[:60]

        # save messages (and title if set)
        update_fields = ["messages", "updated_at"]
        if is_first_message and message:
            update_fields.insert(0, "title")
        self.save(update_fields=update_fields)

        # queue AI title generation only when first message was added
        if is_first_message:
            try:
                self._queue_job()
            except Exception as exc:
                print("Failed to queue AI title job:", exc)



class AiRequest(models.Model):
    """Represents an AI request with lifecycle tracking."""

    PENDING, RUNNING, COMPLETED, FAILED = "pending", "running", "completed", "failed"
    STATUS_OPTIONS = [
        (PENDING, "Pending"),
        (RUNNING, "Running"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default=PENDING)
    session = models.ForeignKey(
        AiChatSession, on_delete=models.CASCADE, null=True, blank=True
    )
    message = models.TextField()
    response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _queue_job(self):
        """Dispatches the request to Celery."""
        from .tasks import handle_ai_request_job
        handle_ai_request_job.delay(self.id)

    def handle(self):
        """
        The core logic executed by the Celery worker.
        """
        self.status = self.RUNNING
        # update status immediately
        self.save(update_fields=['status', 'updated_at'])

        try:
            client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
            model_name = "gemma-3-27b-it"

            completion = client.models.generate_content(
                model=model_name,
                contents=self.message
            )

            # defensive extraction of text
            text = None
            if hasattr(completion, 'text'):
                text = completion.text
            elif isinstance(completion, dict):
                text = completion.get('text') or completion.get('output') or completion.get('result')
                # if nested structure like {'output': [{'content': '...'}]}
                if isinstance(text, list) and text:
                    first = text[0]
                    if isinstance(first, dict):
                        text = first.get('content') or first.get('text') or str(first)
                    else:
                        text = str(first)
            if text is None:
                # fallback to string representation
                text = str(completion)

            self.response = text
            self.status = self.COMPLETED

            # storing in session to track history
            if self.session:
                self.session.add_message(
                    message=self.message,
                    response=self.response
                )

        except Exception as e:
            self.status = self.FAILED
            self.response = str(e)  # Store error for debugging

        # final save
        self.save(update_fields=['status', 'response', 'updated_at'])

    def save(self, **kwargs):
        is_new = self._state.adding

        # First save to get an ID (and allow FK creation)
        super().save(**kwargs)

        # If new and no session, create one (use message as title)
        if is_new and not self.session:
            title_candidate = (self.message or "").strip()[:60]
            if not title_candidate:
                title_candidate = f"new chat {uuid.uuid4().hex[:8]}"

            session = AiChatSession.objects.create(title=title_candidate)
            self.session = session
            # Save only the session FK field to avoid re-saving everything
            super().save(update_fields=['session'])

        # queue background job if newly created
        if is_new:
            try:
                # prefer transaction.on_commit in more complex apps, but keep simple:
                self._queue_job()
            except Exception:
                # if queuing fails, don't break saving; let the exception propagate in handle()
                pass
