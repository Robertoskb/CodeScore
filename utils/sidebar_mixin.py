from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .user_type import get_user_type

required = login_required(login_url='profiles:login',
                          redirect_field_name='next')


@method_decorator(required, name='dispatch')
class SideBarMixin(object):
    def dispatch(self, *args, **kwargs):
        return super(SideBarMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SideBarMixin, self).get_context_data(**kwargs)

        user_type = get_user_type(self.request.user)

        context["teacher_permision"] = not ('admin' != user_type != 'teacher')

        return context
