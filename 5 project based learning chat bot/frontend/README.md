# Django Gemini Chat

A simple, modern chat interface built with React and Tailwind CSS that connects to a local Django API.

## Features
- **Modern UI**: Styled with Tailwind CSS, featuring user/AI message bubbles.
- **Session Management**: Create, list, and view chat sessions.
- **Polling Architecture**: Handles async AI processing via status polling.
- **Responsive**: Mobile-friendly sidebar layout.

## Setup & Run

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Configure API**
   By default, the app connects to `http://localhost:8001`.
   To change this, create a `.env` file in the root directory:
   ```env
   VITE_API_HOST=http://localhost:8001
   ```

3. **Run Development Server**
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

## Backend Requirements (CORS)

Ensure your Django backend allows CORS requests from the frontend origin. 
If using `django-cors-headers`, add:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

## Mock Data for Design Review

If you want to visualize the UI without the backend, the `MessageBubble` component expects this data structure:

```json
[
  {
    "message": "Write a haiku about React.",
    "response": "Components unite,\nState flows like a river stream,\nVirtual DOM updates.",
    "created_at": "2023-10-27T10:00:00Z"
  },
  {
    "message": "How do I center a div?",
    "response": "You can use Flexbox:\n\n.parent {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}",
    "created_at": "2023-10-27T10:05:00Z"
  }
]
```

## Accessibility & Customization

- **Colors**: Colors are defined using Tailwind classes in `src/components/MessageBubble.tsx`. Look for `from-purple-500` to change the gradient.
- **Focus**: Inputs and buttons have `focus-visible` styles for keyboard navigation.
- **Aria**: aria-labels included on input forms.
