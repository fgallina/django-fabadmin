from django.conf.urls.defaults import patterns

urlpatterns = patterns('fabadmin.views',
    (r'^admin/fabadmin/task_list/$', 'task_list'),
)
