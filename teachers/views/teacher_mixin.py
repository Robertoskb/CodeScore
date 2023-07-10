from django.core.exceptions import PermissionDenied

from utils.sidebar_mixin import SideBarMixin
from utils.user_type import get_user_type


class TeacherMixin(SideBarMixin, object):
    def validation(self):
        user_type = get_user_type(self.request.user)

        if 'admin' != user_type != 'teacher':
            raise PermissionDenied

    def get(self, *args, **kwargs):
        self.validation()

        return super(TeacherMixin, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.validation()

        return super(TeacherMixin, self).post(*args, **kwargs)
