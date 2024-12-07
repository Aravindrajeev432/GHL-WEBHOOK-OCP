"""this is an example for showing Open-Closed-principle applied code for django webhook reciver for GoHighLevel,
   this example more focused on 2.0 webhooks

urls.py
path('webhook',WebhookReciver.as_view())

"""

from abc import ABC, abstractmethod

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class EventHandler(ABC):
    @abstractmethod
    def handle_event(self,request):
        return Response(status.HTTP_200_OK)

class NotesEventHandler(EventHandler):
    """This event handler processes "note created" and "update note" events from a webhook.

    Handles the event by checking the "type" in the request data and logs appropriate messages
    when a note is created or updated. Returns a successful response status.

    Args:
        request: The webhook request containing event data with a "type" field

    Returns:
        Response with HTTP 200 status code
    """
    def handle_event(self, request):
        if request.data.get('type') == 'NoteCreated':
            print("note created handled")
        if request.data.get('type') == 'NoteUpdated':
            print("note updation handled")
        return Response(status.HTTP_200_OK)


class ContactEventsHandler(EventHandler):
    def handle_event(self, request):
        if request.data.get('type') == "ContactCreated":
            print("contact creation handled")
        return Response(status.HTTP_200_OK)

# settings.py



class WebhookReciver(APIView):
    def post(self, request):

        # EVENT_HANDLERS can be moved into settings or anywhere you want
        EVENT_HANDLERS = {
           "ContactCreate": ContactEventsHandler(),
          "NoteCreate": NotesEventHandler(),
        }

        webhook_handler:EventHandler|None = EVENT_HANDLERS.get(request.data.get('type'))
        if webhook_handler:
            return webhook_handler.handle_event(request)
        else:
            return Response(status=status.HTTP_200_OK)
