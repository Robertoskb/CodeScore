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
