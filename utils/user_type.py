from django.core.exceptions import PermissionDenied


def get_user_type(user):
    if len(user.username) == 14:
        return 'student'
    if len(user.username) == 7:
        return 'teacher'
    if user.is_superuser:
        return 'admin'
    if user.is_staff:
        return 'staff'
    return 'user'


def check_user_type(user, other_username):
    user_type = get_user_type(user)

    username_validation = user.username != other_username
    user_type_validation = 'admin' != user_type != 'teacher'

    if username_validation and user_type_validation:
        raise PermissionDenied

    if not username_validation and user_type == 'teacher':
        user_type = 'student'

    return user_type


def check_teacher(user, other_username, exam):
    user_type = get_user_type(user)

    if user.username == other_username:
        return

    if user_type == 'admin':
        return

    if user == exam.author:
        return

    raise PermissionDenied
