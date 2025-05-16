# students/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from students.models import Student

class StudentJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class for Student model.
    """

    def get_user(self, validated_token):
        """
        Override to get Student by student_id in token.
        """
        try:
            student_id = validated_token.get("student_id")
            if not student_id:
                raise AuthenticationFailed(_("Token contained no recognizable student identification"), code="token_not_valid")

            try:
                student = Student.objects.get(student_id=student_id)
            except Student.DoesNotExist:
                raise AuthenticationFailed(_("Student not found"), code="user_not_found")

            return student
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable student identification"))
