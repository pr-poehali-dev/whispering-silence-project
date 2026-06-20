import json
import os
import base64
import smtplib
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def handler(event: dict, context) -> dict:
    """Принимает заявку с лендинга и отправляет её на почту через Gmail."""

    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': cors_headers, 'body': ''}

    body = json.loads(event.get('body', '{}'))
    name = body.get('name', '').strip()
    contact = body.get('contact', '').strip()
    service = body.get('service', '').strip()
    wish = body.get('wish', '').strip()
    photo_base64 = body.get('photo', None)
    photo_name = body.get('photo_name', 'photo.jpg')

    if not name or not contact:
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps({'error': 'Имя и контакт обязательны'})
        }

    photo_url = None
    if photo_base64:
        s3 = boto3.client(
            's3',
            endpoint_url='https://bucket.poehali.dev',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        )
        photo_data = base64.b64decode(photo_base64)
        key = f"orders/{contact.replace('@', '_')}_{photo_name}"
        s3.put_object(Bucket='files', Key=key, Body=photo_data, ContentType='image/jpeg')
        photo_url = f"https://cdn.poehali.dev/projects/{os.environ['AWS_ACCESS_KEY_ID']}/bucket/{key}"

    gmail_user = 'burntime.dota@gmail.com'
    gmail_password = os.environ['GMAIL_APP_PASSWORD'].replace(' ', '')

    if photo_url:
        photo_html = f'''
        <tr>
          <td colspan="2" style="padding: 16px 0 8px 0; color: #666;">Фото клиента</td>
        </tr>
        <tr>
          <td colspan="2" style="padding-bottom: 16px;">
            <a href="{photo_url}">
              <img src="{photo_url}" alt="Фото клиента" style="max-width: 400px; width: 100%; border-radius: 4px; display: block;" />
            </a>
          </td>
        </tr>'''
    else:
        photo_html = '<tr><td style="padding: 8px 0; color: #666;">Фото</td><td style="padding: 8px 0;">—</td></tr>'

    html = f"""
    <html><body style="font-family: Arial, sans-serif; color: #222; max-width: 600px;">
      <h2 style="border-bottom: 2px solid #000; padding-bottom: 8px;">Новая заявка на bediff</h2>
      <table style="width:100%; border-collapse: collapse;">
        <tr><td style="padding: 8px 0; color: #666; width: 140px;">Имя</td><td style="padding: 8px 0;"><b>{name}</b></td></tr>
        <tr><td style="padding: 8px 0; color: #666;">Контакт</td><td style="padding: 8px 0;"><b>{contact}</b></td></tr>
        <tr><td style="padding: 8px 0; color: #666;">Услуга</td><td style="padding: 8px 0;"><b>{service}</b></td></tr>
        <tr><td style="padding: 8px 0; color: #666;">Пожелание</td><td style="padding: 8px 0;">{wish if wish else '—'}</td></tr>
        {photo_html}
      </table>
    </body></html>
    """

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'Новая заявка от {name} — bediff'
    msg['From'] = gmail_user
    msg['To'] = gmail_user
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, gmail_user, msg.as_string())

    return {
        'statusCode': 200,
        'headers': cors_headers,
        'body': json.dumps({'ok': True})
    }