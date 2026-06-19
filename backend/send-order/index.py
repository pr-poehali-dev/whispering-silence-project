import json
import os
import urllib.request
import urllib.parse
import base64
import boto3

def handler(event: dict, context) -> dict:
    """Принимает заявку с лендинга и отправляет её в Telegram."""

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

    token = os.environ['TELEGRAM_BOT_TOKEN']
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    text = (
        f"📸 *Новая заявка на bediff*\n\n"
        f"👤 *Имя:* {name}\n"
        f"📱 *Контакт:* {contact}\n"
        f"🎯 *Услуга:* {service}\n"
        f"💬 *Пожелание:* {wish if wish else '—'}\n"
        f"🖼 *Фото:* {'приложено' if photo_base64 else 'не приложено'}"
    )

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
        photo_url = f"https://cdn.poehali.dev/projects/{os.environ['AWS_ACCESS_KEY_ID']}/files/{key}"
        text += f"\n🔗 {photo_url}"

    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown',
    }).encode('utf-8')

    req = urllib.request.Request(api_url, data=payload, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

    return {
        'statusCode': 200,
        'headers': cors_headers,
        'body': json.dumps({'ok': True})
    }
