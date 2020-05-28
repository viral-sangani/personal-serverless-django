import boto3
from django.conf import settings
import json

client = boto3.client('ses', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name='ap-south-1')


'''
Template variable: {
    name: "email"
}
'''
NEW_SUBSCRIBER_TEMPLATE = {
    "template_name": "new_subscriber",
    "subject": "Newsletter: Welcome Aboard",
    "text": "Newsletter: Welcome Aboard",
    "template_html": open("templates/email/newSubscriber.html", "r").read(),
}


def send(to, action):
    """
     Uses the boto3 to send email to user.

     :param string to: email address of the target user.
     :action: contains META data for email, like template_name, template_data
    """

    response = client.send_templated_email(
        Source='newsletter@viralsangani.me',
        Destination={
            'ToAddresses': [to]
        },
        ReplyToAddresses=[
            'viral.sangani2011@gmail.com',
        ],
        Template=action['template_name'],
        TemplateData=json.dumps(action['template_data'])
    )
    print(">>>>>>>>>> Email send to template " + action['template_name'] + " with email : " + to)
    return response


def create_template(template):
    response = client.create_template(
        Template={
            'TemplateName': template['template_name'],
            'SubjectPart': template['subject'],
            'TextPart': template['text'],
            'HtmlPart': template['template_html']
        }
    )
    return response


def update_template(template):
    response = client.update_template(
        Template={
            'TemplateName': template['template_name'],
            'SubjectPart': template['subject'],
            'TextPart': template['text'],
            'HtmlPart': template['template_html']
        }
    )
    return response


def delete_template(template):
    response = client.delete_template(
        TemplateName=template['template_name']
    )
    return response


def actions(obj, action_name):
    if action_name == "NEW_SUBSCRIBER":
        template_obj = {
            'template_name': 'new_subscriber',
            'template_data': {
                'name': obj.name,
                'email': obj.email
            }
        }
    send(obj.email, template_obj)
