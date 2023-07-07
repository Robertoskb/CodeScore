from .user_type import get_user_type


class SideBarMixin(object):

    def get_context_data(self, **kwargs):
        context = super(SideBarMixin, self).get_context_data(**kwargs)

        user_type = get_user_type(self.request.user)

        context["teacher_permision"] = not ('admin' != user_type != 'teacher')

        return context
