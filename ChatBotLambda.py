import json
import time
import os
import logging
import boto3
import uuid

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Helper that build the response

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


""" --- Functions that control the bot's behavior --- """


def volunteer_qualifications(intent_request):


    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': 'Job qualifications',
            'Date': time.strftime('%a, %d %b %Y'),
            'Time': time.strftime('%H:%M:%S')

        }


    )

    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'Volunteer Qualification',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'No Minimum qualifications required. '
                       'People from all ages are welcome to join! '
                       'To find out more: question 1 at https://www.FoodForLife.com/faq '

    }
    )


def volunteer_jobs(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': 'Jobs available',
            'Date': time.strftime('%a, %d %b %Y'),
            'Time': time.strftime('%H:%M:%S')

        }

    )

    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'Volunteer jobs available',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'we have some roles available: '
                       '- Donor '
                       '- Driver (license required) '
                       'To find out more: question 2 at https://www.FoodForLife.com/faq '

    }
    )


def donator_job(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': 'Donor job scope',
            'Date': time.strftime('%a, %d %b %Y'),
            'Time': time.strftime('%H:%M:%S')

        }


    )


    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'Volunteer Qualifications (donator)',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Donators can donate at any amount* at their own will. '
                       'A driver will come to your location to pickup after conformation '
                       "and your donations will be on it's way to its destination. "
                       'Please visit www.foodforlife.com/donate to check the list of accepted food products.'

    }
    )


def driver_job(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': 'Driver job scope',
            'Date': time.strftime('%a, %d %b %Y'),
            'Time': time.strftime('%H:%M:%S')

        }


    )


    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'Volunteer Qualifications (driver)',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Drive with us during your free time! Transporter will ne picking up goods '
                       "from the donor's location and sending it to it's destination "
                       'Find out more at www.foodforlife.com/faq '

    }
    )


# Intents


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Volunteer_qualification':
        return volunteer_qualifications(intent_request)
    elif intent_name == 'Volunteer_jobs':
        return volunteer_jobs(intent_request)
    elif intent_name == 'Donator_job':
        return donator_job(intent_request)
    elif intent_name == 'Driver_job':
        return driver_job(intent_request)
    else:
        dynamodb = boto3.resource('dynamodb')
        dynamoTable = dynamodb.Table('Test12345')
        dynamoTable.put_item(

            Item={
                'Invalid request': intent_request,
                'Date': time.strftime('%a, %d %b %Y'),
                'Time': time.strftime('%H:%M:%S')

            }

        )

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'Singapore'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)


