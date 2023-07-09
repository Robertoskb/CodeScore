from utils.sidebar_mixin import SideBarMixin


class TeacherMixin(SideBarMixin, object):
    def get(self, *args, **kwargs):
        self.validation()

        return super(TeacherMixin, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.validation()

        return super(TeacherMixin, self).post(*args, **kwargs)
