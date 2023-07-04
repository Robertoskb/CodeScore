from django.contrib.auth.models import User


def get_user_type(self):
    if len(self.username) == 14:
        return 'student'
    if len(self.username) == 7:
        return 'teacher'
    if self.is_superuser:
        return 'admin'
    if self.is_staff:
        return 'staff'
    return 'user'


User.add_to_class('user_type', get_user_type)
