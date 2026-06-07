# Deployment Guide

## Render

1. Create a PostgreSQL database on Render.
2. Create a Web Service from the repository.
3. Set root directory to `cmpes`.
4. Use build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`.
5. Use start command: `gunicorn config.wsgi:application`.
6. Set environment variables:

`DEBUG=False`
`SECRET_KEY=<strong random value>`
`DATABASE_URL=<Render PostgreSQL internal URL>`
`ALLOWED_HOSTS=<your-render-domain>`
`CSRF_TRUSTED_ORIGINS=https://<your-render-domain>`
`ADMIN_URL=<private-admin-path>/`

7. Run migrations from the Render shell or release phase: `python manage.py migrate`.
8. Create the first admin: `python manage.py createsuperuser`.
9. For demo data, optionally run: `python manage.py seed_demo_data`.

Render terminates TLS before Gunicorn. If deploying behind your own VM, use Nginx or Apache as the HTTPS reverse proxy to the WSGI server.

## Media Storage

For real organizational use, do not rely on local app disk for uploaded contract documents. Configure S3-compatible storage:

`USE_S3=True`
`AWS_ACCESS_KEY_ID=<key>`
`AWS_SECRET_ACCESS_KEY=<secret>`
`AWS_STORAGE_BUCKET_NAME=<bucket>`
`AWS_S3_REGION_NAME=<region>`

Leave `USE_S3=False` for local academic demonstrations.

## Email Notifications

Configure SMTP or a provider-backed email backend before enabling email alerts:

`EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
`EMAIL_HOST=<smtp-host>`
`EMAIL_PORT=587`
`EMAIL_USE_TLS=True`
`EMAIL_HOST_USER=<smtp-user>`
`EMAIL_HOST_PASSWORD=<smtp-password>`

Then schedule: `python manage.py send_contract_alerts --email`.

## Backup Strategy

Use Render PostgreSQL automated backups for paid plans. For manual backups:

```bash
pg_dump "$DATABASE_URL" > cmpes-backup.sql
```

Store backups encrypted and test restores before relying on them.

## Production Security Notes

Use a long random `SECRET_KEY`, keep `DEBUG=False`, set `ALLOWED_HOSTS`, set `CSRF_TRUSTED_ORIGINS`, and consider a non-default `ADMIN_URL`. HSTS and secure cookies are enabled automatically when `DEBUG=False`.
