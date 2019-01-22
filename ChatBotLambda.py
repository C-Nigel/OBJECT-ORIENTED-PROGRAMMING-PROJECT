import json
import time
import os
import logging
import boto3
import uuid
import re
import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Helper that build the response

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


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


def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None


def safe_int(i):
    """
    Safely convert n value to int.
    """
    if i is not None:
        return int(i)
    return i

def safe_str(i):
    """
    Safely convert n value to int.
    """
    if i is not None:
        return str(i)
    return i


def isvalid_role(role):
    valid_roles = ['donor', 'transporter', 'receiver']
    return role.lower() in valid_roles


def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


""" --- Functions that control the bot's behavior --- """


def volunteer_qualifications(intent_request):


    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': uuid.uuid4().hex,
            'Title': 'Job qualifications',
            'invoked on': str(datetime.datetime.now())

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
            'Request': uuid.uuid4().hex,
            'Title': 'Jobs available',
            'invoked on': str(datetime.datetime.now())

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
            'Request': uuid.uuid4().hex,
            'Title': 'Donor job scope',
            'invoked on': str(datetime.datetime.now())

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
            'Request': uuid.uuid4().hex,
            'Title': 'Driver job scope',
            'invoked on': str(datetime.datetime.now())

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


def validate_sign_up(intent_request):
    name = try_ex(lambda: intent_request['name'])
    password = try_ex(lambda: intent_request['password'])
    contact_number = safe_int(try_ex(lambda: intent_request['contact_number']))
    role = try_ex(lambda: intent_request['role'])
    email = try_ex(lambda: intent_request['email'])
    company_name = try_ex(lambda: intent_request['company_name'])

    if name:
        pass

    if password:
        pass

    if contact_number:
        pass

    if role and not isvalid_role(role):
        return build_validation_result(
            False,
            'role',
            'Role not available yet. Please retry.'
        )

    if email:
        pass
        '''email_verifier = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)@[a-z0-9-]+(\.[a-z0-9-]+)(\.[a-z]{2,4})$', email)
        if email_verifier == None:
            return build_validation_result(False, 'Email', 'Email not recognised. Please retry.')'''

    if company_name:
        pass

    return{'isValid': True}



def sign_up(intent_request):
    """
        Performs dialog management and fulfillment for booking a hotel.

        Beyond fulfillment, the implementation for this intent demonstrates the following:
        1) Use of elicitSlot in slot validation and re-prompting
        2) Use of sessionAttributes to pass information that can be used to guide conversation
        """

    name = try_ex(lambda: intent_request['currentIntent']['slots']['name'])
    email = try_ex(lambda: intent_request['currentIntent']['slots']['email'])
    password = try_ex(lambda: intent_request['currentIntent']['slots']['password'])
    contact_number = safe_int(try_ex(lambda: intent_request['currentIntent']['slots']['contact_number']))
    company_name = try_ex(lambda: intent_request['currentIntent']['slots']['company_name'])
    role = try_ex(lambda: intent_request['currentIntent']['slots']['role'])


    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    # Load confirmation history and track the current reservation.
    user_info = json.dumps({
        'RequestType': 'User Sign Up',
        'name': name,
        'email': email,
        'password': password,
        'contact_number': contact_number,
        'company_name': company_name,
        'role': role
    })

    session_attributes['currentRequest'] = user_info

    if intent_request['invocationSource'] == 'DialogCodeHook':
        # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
        validation_result = validate_sign_up(intent_request['currentIntent']['slots'])
        if not validation_result['isValid']:
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        session_attributes['currentRequest'] = user_info
        return delegate(session_attributes, intent_request['currentIntent']['slots'])

    # writing the data to dynamodb by giving value to a attribute
    slots = intent_request['currentIntent']['slots']
    sign_up_name = slots['name']
    sign_up_email = slots['email']
    sign_up_password = slots['password']
    sign_up_contact_number = slots['contact_number']
    sign_up_company_name = slots['company_name']
    sign_up_role = slots['role']

    # writing the attribute to dynamoDB
    dynamodb = boto3.resource('dynamodb')
    dynamo_table = dynamodb.Table('user_credentials')
    dynamo_table.put_item(

        Item={
            'email': sign_up_email,
            'password': sign_up_password,
            'name': sign_up_name,
            'contact number': sign_up_contact_number,
            'company name': sign_up_company_name,
            'role': sign_up_role,
            'created on': str(datetime.datetime.now())

        }
    )

    # Booking the hotel.  In a real application, this would likely involve a call to a backend service.
    logger.debug('signed user up')

    try_ex(lambda: session_attributes.pop('currentRequest'))
    session_attributes['lastConfirmedReservation'] = user_info

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Sign up successful.you may login in from the top left. '
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
    elif intent_name == 'Sign_up_user':
        return sign_up(intent_request)
    else:
        dynamodb = boto3.resource('dynamodb')
        dynamo_table = dynamodb.Table('Test12345')
        dynamo_table.put_item(

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

    # By default, treat the user request as coming from the GMT(+8:00) zone.
    os.environ['TZ'] = 'Singapore'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)


