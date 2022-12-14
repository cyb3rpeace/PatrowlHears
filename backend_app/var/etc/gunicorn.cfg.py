bind = "0.0.0.0:8303"
workers = 2
debug = False
errorlog = "/opt/patrowl-hears/backend_app/var/log/gunicorn.patrowlhears.error.log"
raw_env = [
  "APP_DEBUG=False",
  "LOGGING_LEVEL=INFO,WARNING,ERROR,DEBUG",
  "PATROWL_PROXY_HTTP=''",
  "PATROWL_PROXY_HTTPS=''",
  "SECRET_KEY='*** omg this is the secret !***'",
  "DB_ENV_DB=patrowlhears_db",
  "DB_ENV_POSTGRES_USER=patrowlhears",
  "DB_ENV_POSTGRES_PASSWORD=patrowlhears",
  "DB_PORT_5432_TCP_HOST=db",
  "DB_PORT_5432_TCP_PORT=5432",
  "RABBIT_PORT_5672_TCP=rabbitmq",
  "TWITTER_ENABLED=False",
  "EMAIL_USE_TLS={{patrowlhears_email_use_tls}}",
  "EMAIL_HOST={{patrowlhears_email_host}}",
  "EMAIL_HOST_USER={{patrowlhears_email_host_user}}",
  "EMAIL_HOST_PASSWORD={{patrowlhears_email_host_passwd}}",
  "EMAIL_PORT={{patrowlhears_email_port}}",
  "DEFAULT_FROM_EMAIL={{patrowlhears_default_from_email}}",
  "EMAIL_RCPT_USER=john@foo.bar",
  "BASE_URL=https://mydemo.hears.patrowl.io"
]
