import logging
import uuid
from google.appengine.ext import ndb


class Event(ndb.Model):
    """
    NDB model class for a Event.
    """
    description = ndb.StringProperty()
    startdt = ndb.DateTimeProperty()
    enddt = ndb.DateTimeProperty()
    teacher_name = ndb.StringProperty()
    teacher_email = ndb.StringProperty()
    location = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def _get_key(cls, event_uuid):
        return ndb.Key(cls, event_uuid)

    @classmethod
    def get_all_events(cls):
        """Fetches all events.

        Events are ordered them by date created, with most recent note added
        first.
        """
        query = cls.query().order(-cls.created)
        events = query.fetch()

        return_events = []

        for event in events:

            return_events.append({
                'key': event.key.id(),
                'description': event.description,
                'startdt': event.startdt,
                'enddt': event.enddt,
                'location': event.location,
                'teacher_name': event.teacher_name,
                'teacher_email': event.teacher_email,
                'enrolled': False
            })

        return return_events

    @classmethod
    def add_event(cls, event_data, teacher_name, teacher_email):
        try:
            key = cls._get_key(uuid.uuid4().hex)
            event = cls()
            event.key = key

            # TODO : format dates for startdt enddt
            event.description = event_data['description']
            event.startdt = event_data['startdt']
            event.enddt = event_data['enddt']
            event.location = event_data['location']
            event.teacher_name = teacher_name
            event.teacher_email = teacher_email
            return event.put()
        except Exception as e:
            logging.error("Error inserting data ", str(e))
        return None
