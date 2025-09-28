from botocore.exceptions import ClientError
from django.core.mail import send_mail
from decouple import config
import boto3
import json


# ------------------------------------------------------
# *                  SMS Utils
# ------------------------------------------------------


def send_sms_notification_to_number(
    message: str,
    phone_number: str,
    queue: bool = False,
):
    if not queue:
        return send_sms(message, phone_number)
    else:
        res = add_to_sms_queue(
            message={"message_text": message, "phone_number": phone_number}
        )
        return 1 if res == 200 else 0


def send_sms(
    message: str,
    phone_number: str,
):
    # mock sms
    if config("MOCK_SEND_SMS") == "1":
        print("MOCKED SMS")
        return 1

    # sending sms
    try:
        sns_client = boto3.client("sns")
        response = sns_client.publish(PhoneNumber=phone_number, Message=message)
        print(response)
        return 1 if response["ResponseMetadata"]["HTTPStatusCode"] == 200 else 0
    except ClientError as error:
        print(error)
        return error


def add_to_sms_queue(message: dict):
    sqs_client = boto3.client("sqs")
    if config("MOCK_SEND_SMS") == "1":
        print("MOCKED SMS")
        return 200
    else:
        try:
            response = sqs_client.send_message(
                QueueUrl=config("SMS_QUEUE_NAME"), MessageBody=json.dumps(message)
            )
            return response["ResponseMetadata"]["HTTPStatusCode"]
        except ClientError as error:
            print(error)
            return error


# ------------------------------------------------------
# *                  Email Utils
# ------------------------------------------------------


def send_email_notification_to_list(
    subject: str,
    email_body: str,
    to_email_list: list[str],
    from_email: str = "haiderjuttearner@gmail.com",
    queue: bool = False,
):
    if not queue:
        return send_mail(subject, email_body, from_email, to_email_list)
    else:
        res = add_to_email_queue(
            message={
                "subject": subject,
                "email_body": email_body,
                "from_email": from_email,
                "to_email_list": to_email_list,
            }
        )
        return 1 if res == 200 else 0


def add_to_email_queue(message: dict):
    sqs_client = boto3.client("sqs")
    if config("MOCK_SEND_EMAIL") == "1":
        return 200
    else:
        try:
            response = sqs_client.send_message(
                QueueUrl=config("EMAIL_QUEUE_NAME"), MessageBody=json.dumps(message)
            )
            return response["ResponseMetadata"]["HTTPStatusCode"]
        except ClientError as error:
            print(error)
            return error
