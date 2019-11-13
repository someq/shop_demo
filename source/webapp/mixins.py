from django.views.generic import View


class TimeCounterMixin():


    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class VisitsCounterMixin():
    pass


#
# class StatsView(TimeCounterMixin, VisitsCounterMixin, View):
#     def dispatch(self, request, *args, **kwargs):