from django.contrib.auth.mixins import UserPassesTestMixin

from utils.sidebar_mixin import SideBarMixin
from utils.user_type import get_user_type


class TeacherMixin(SideBarMixin, UserPassesTestMixin):
    def test_func(self):
        user_type = get_user_type(self.request.user)

        return 'admin' == user_type or user_type == 'teacher'
