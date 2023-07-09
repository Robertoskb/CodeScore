from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

from utils.sidebar_mixin import SideBarMixin, get_user_type

required = login_required(login_url='profiles:login',
                          redirect_field_name='next')


@method_decorator(required, name='dispatch')
class TeacherMixin(SideBarMixin, object):
    def validation(self):
        user_type = get_user_type(self.request.user)

        if 'admin' != user_type != 'teacher':
            raise PermissionDenied

    def dispatch(self, *args, **kwargs):
        return super(TeacherMixin, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        self.validation()

        return super(TeacherMixin, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.validation()

        return super(TeacherMixin, self).post(*args, **kwargs)
