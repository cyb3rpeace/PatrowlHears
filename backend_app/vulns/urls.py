from django.urls import path
from . import apis


urlpatterns = [
    path('<vuln_id>/refresh_score', apis.refresh_vuln_score, name='refresh_vuln_score'),
    path('<vuln_id>/history', apis.get_vuln_history, name='get_vuln_history'),
    path('<vuln_id>/cpes', apis.get_vuln_cpes, name='get_vuln_cpes'),
    path('<vuln_id>/counter', apis.get_number_exploits_threats, name='get_number_exploits_threats'),
    path('<vuln_id>/exploits', apis.get_exploits, name='get_exploits'),
    path('<vuln_id>/exploits/add', apis.add_exploit, name='add_exploit'),
    path('<vuln_id>/exploits/edit', apis.edit_exploit, name='edit_exploit'),
    path('<vuln_id>/exploits/<exploit_id>/del', apis.del_exploit, name='del_exploit'),
    path('<vuln_id>/threats', apis.get_threats, name='get_threats'),
    path('<vuln_id>/threats/add', apis.add_threat, name='add_threat'),
    path('<vuln_id>/threats/edit', apis.edit_threat, name='edit_threat'),
    path('<vuln_id>/threats/<threat_id>/del', apis.del_threat, name='del_threat'),
    path('<vuln_id>/toggle', apis.toggle_monitor_vuln, name='toggle_monitor_vuln'),
    path('<vuln_id>/export/json', apis.export_vuln_json, name='export_vuln_json'),
    path('<vuln_id>/export/email', apis.export_vuln_sendmail, name='export_vuln_sendmail'),
    path('refresh_scores', apis.refresh_vulns_score_async, name='refresh_vulns_score_async'),
    path('refresh_vulnerable_versions', apis.refresh_vulns_product_versions_async, name='refresh_vulns_product_versions_async'),
    path('add', apis.add_vuln, name='add_vuln'),
    path('edit', apis.edit_vuln, name='edit_vuln'),
    path('stats', apis.get_vuln_stats, name='get_vuln_stats'),
    path('stats/monitored', apis.get_monitored_vuln_stats, name='get_monitored_vuln_stats'),
    path('latest', apis.get_latest_vulns, name='get_latest_vulns'),
    path('admin/email-report/daily', apis.email_daily_report, name='email_daily_report'),
    path('admin/email-report/weekly', apis.email_weekly_report, name='email_weekly_report'),
    path('admin/email-report/monthly', apis.email_monthly_report, name='email_monthly_report'),
    path('admin/slack-alert/<vuln_id>', apis.slack_alert_vuln, name='slack_alert_vuln'),
]
