from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView

from expertsessions.models import Expertsessions

class DashboardListView(SuccessMessageMixin, TemplateView):
    permission_required = 'dashboard.view_dashboard'
    template_name = 'dashboard/dashboard_list.html'

