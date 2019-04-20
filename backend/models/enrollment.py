import logging
from google.appengine.ext import ndb


class Enrollment(ndb.Model):
    """
    NDB model class for a UserType
    """

    student_email = ndb.StringProperty()
    event_id = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_key(cls, email, event_key):
        return ndb.Key(Enrollment, str(email)+str(event_key))

    @classmethod
    def getAllEnrollments(cls, email):
        query = Enrollment.query(
            Enrollment.student_email == email).order(-Enrollment.created)

        enrollments = query.fetch()

        return_enrollments = []

        for enrollment in enrollments:
            return_enrollments.append({
                'key': enrollment.key.id(),
                'student_email': enrollment.student_email,
                'event_id': enrollment.event_id
            })
            pass

        return return_enrollments

    @classmethod
    def enroll(cls, student_email, event_key):
        enrollment = cls()
        enrollment.key = cls.get_key(student_email, event_key)
        enrollment.student_email = student_email
        enrollment.event_id = event_key
        return enrollment.put()
