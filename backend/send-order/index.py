import json
import os
import urllib.request
import urllib.error
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
        f"\U0001f4f8 *Новая заявка на bediff*\n\n"
        f"\U0001f464 *Имя:* {name}\n"
        f"\U0001f4f1 *Контакт:* {contact}\n"
        f"\U0001f3af *Услуга:* {service}\n"
        f"\U0001f4ac *Пожелание:* {wish if wish else chr(8212)}\n"
        f"\U0001f5bc *Фото:* {'приложено' if photo_base64 else 'не приложено'}"
    )

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
        text += f"\n\U0001f517 {photo_url}"

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
