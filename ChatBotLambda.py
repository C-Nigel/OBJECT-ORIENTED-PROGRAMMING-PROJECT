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
    # Safely convert n value to int.
    if i is not None:
        return int(i)
    return i


def safe_str(i):

    # Safely convert n value to int.

    if i is not None:
        return str(i)
    return i


def isvalid_role(role):

    # roles that currently exist

    valid_roles = ['donor', 'transporter', 'receiver']
    return role.lower() in valid_roles


def isvalid_category(role):

    # list of category that user is able to change through the chat bot

    valid_roles = ['address', 'contact number', 'name', 'company name', 'contact']
    return role.lower() in valid_roles


def build_validation_result(isvalid, violated_slot, message_content):

    # check if the values is valid and show end message if true

    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


class Write:

    def __init__(self, intent_request):
        # writing the data to dynamodb by giving value to a attribute
        slots = intent_request['currentIntent']['slots']
        self.__sign_up_name = slots['name']
        self.__sign_up_email = slots['email']
        self.__sign_up_password = slots['password']
        self.__sign_up_contact_number = slots['contact_number']
        self.__sign_up_company_name = slots['company_name']
        self.__sign_up_address = slots['address']
        self.__sign_up_role = slots['role']

    def get_name(self):
        return self.__sign_up_name

    def get_email(self):
        return self.__sign_up_email

    def get_password(self):
        return self.__sign_up_password

    def get_contact_number(self):
        return self.__sign_up_contact_number

    def get_company_name(self):
        return self.__sign_up_company_name

    def get_address(self):
        return self.__sign_up_address

    def get_role(self):
        return self.__sign_up_role


""" --- Functions that control the bot's behavior --- """


def welcome_message(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': uuid.uuid4().hex,
            'Title': 'Welcome message',
            'invoked on': str(datetime.datetime.now())

        }


    )

    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'Welcome message',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': "Hi there, how may I help you today? you may ask me anything or sign up/update "
                       "an account through me. "

        }
    )


def sign_in(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': uuid.uuid4().hex,
            'Title': 'Sign in',
            'invoked on': str(datetime.datetime.now())

        }


    )

    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'Sign in',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': "Sorry, I am unable to help you sign in but you will be "
                       "able to sign in at the top right corner of the web page. You may sign up for an account here "
                       "by typing 'sign me up' if you do not have an account yet."

        }
    )


def register_account(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': uuid.uuid4().hex,
            'Title': 'Register account',
            'invoked on': str(datetime.datetime.now())

        }


    )

    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'Register account',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': "You may sign up for an account on the top right corner "
                       "or sign up for an account through me by typing 'sign up' here. "

        }
    )


def receiver_users(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': uuid.uuid4().hex,
            'Title': 'Receiver_users',
            'invoked on': str(datetime.datetime.now())

        }


    )

    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'Receiver users',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Companies/Organisations such as elderly home care receives edible consumables from us.'

        }
    )


def feedback(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': uuid.uuid4().hex,
            'Title': 'feedback',
            'invoked on': str(datetime.datetime.now())

        }


    )

    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'Feedback',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'We would like to hear your feedback! drop as a feedback under our FAQ page '
                       'and we will reply to you as soon as possible.'

        }
    )


def ending_message(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': uuid.uuid4().hex,
            'Title': 'Ending message',
            'invoked on': str(datetime.datetime.now())

        }


    )

    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'Ending message',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': "It has been my pleasure helping you out. Do ask me if you require any query!"

        }
    )


def about_us(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': uuid.uuid4().hex,
            'Title': 'About us',
            'invoked on': str(datetime.datetime.now())

        }


    )

    session_attributes = intent_request['sessionAttributes']if intent_request['sessionAttributes'] is not None else {}

    request = json.dumps({
        'RequestType': 'About us',
    })

    session_attributes['currentRequest'] = request

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'We are a company that strives to help save our planet by collecting consumable '
                       'food and redistributing it to the less fortunate.'

        }
    )


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
                       'Head over to our FAQ page to find out more. '

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
            'content':  'Here are some roles currently available: '
                        '- Donor '
                        "- Driver (Drivers' license required) "
                        '- Receiver '
                        "sign up for an account by typing 'sign me up' here. "

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
            'content': 'Donators can donate at any amount* of at their own will and '
                       'a driver will come to your location to pickup. '
                       "sign up as a donor by typing 'sign me up' here. "

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
            'content': 'Drive with us during your free time! Transporter will be picking up goods '
                       "from the donor's location and sending it to it's destination. "
                       "sign up as a driver by typing 'sign me up' here. "

        }
    )


def receiver_job(intent_request):

    dynamodb = boto3.resource('dynamodb')
    dynamoTable = dynamodb.Table('User_requests')
    dynamoTable.put_item(

        Item={
            'Request': uuid.uuid4().hex,
            'Title': 'receiver job scope',
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
            'content': 'Sign up with us as a receiver, give us details and our admins will '
                       "plan and send edible consumables to you. "
                       "sign up as a receiver by typing 'sign me up' here. "

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

    # Performs dialog management and fulfillment for creating an account.

    name = try_ex(lambda: intent_request['currentIntent']['slots']['name'])
    email = try_ex(lambda: intent_request['currentIntent']['slots']['email'])
    password = try_ex(lambda: intent_request['currentIntent']['slots']['password'])
    contact_number = safe_int(try_ex(lambda: intent_request['currentIntent']['slots']['contact_number']))
    company_name = try_ex(lambda: intent_request['currentIntent']['slots']['company_name'])
    role = try_ex(lambda: intent_request['currentIntent']['slots']['role'])

    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    user_info = json.dumps({
        'RequestType': 'User Sign Up',
        'person_name': name,
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

    # writing the attribute to dynamoDB
    s1 = Write(intent_request)
    dynamodb = boto3.resource('dynamodb')
    dynamo_table = dynamodb.Table('user_credentials')
    dynamo_table.put_item(

        Item={
            'email': s1.get_email(),
            'password': s1.get_password(),
            'person_name': s1.get_name(),
            'contact_number': s1.get_contact_number(),
            'company_name': s1.get_company_name(),
            'address': s1.get_address(),
            'role': s1.get_role(),
            'created on': str(datetime.datetime.now())


        }
    )

    logger.debug('signed user up')

    try_ex(lambda: session_attributes.pop('currentRequest'))
    session_attributes['lastConfirmedRequest'] = user_info

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Sign up successful. You may login into your account from the top right of the web page. '
        }
    )


def validate_account_update(intent_request):
    password = try_ex(lambda: intent_request['password'])
    category = try_ex(lambda: intent_request['category'])
    email = try_ex(lambda: intent_request['email'])
    data = try_ex(lambda: intent_request['data'])

    if password:
        pass

    if category and not isvalid_category(category):
        return build_validation_result(
            False,
            'role',
            'Please enter a valid option to update.'
        )

    if email:
        pass
        '''email_verifier = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)@[a-z0-9-]+(\.[a-z0-9-]+)(\.[a-z]{2,4})$', email)
        if email_verifier == None:
            return build_validation_result(False, 'Email', 'Email not recognised. Please retry.')'''

    if data:
        pass

    return{'isValid': True}


def account_update(intent_request):

    email = try_ex(lambda: intent_request['currentIntent']['slots']['email'])
    password = try_ex(lambda: intent_request['currentIntent']['slots']['password'])
    category = try_ex(lambda: intent_request['currentIntent']['slots']['password'])
    data = try_ex(lambda: intent_request['currentIntent']['slots']['data'])

    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    user_updated_info = json.dumps({
        'RequestType': 'User Account Update',
        'email': email,
        'password': password,
        'category': category,
        'data': data
    })

    session_attributes['currentRequest'] = user_updated_info

    if intent_request['invocationSource'] == 'DialogCodeHook':
        # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
        validation_result = validate_account_update(intent_request['currentIntent']['slots'])
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

        session_attributes['currentRequest'] = user_updated_info
        return delegate(session_attributes, intent_request['currentIntent']['slots'])

    slots = intent_request['currentIntent']['slots']
    # writing the attribute to dynamoDB
    dynamodb = boto3.resource('dynamodb')
    dynamo_table = dynamodb.Table('user_credentials')

    if slots['category'] == 'address':
        dynamo_table.update_item(

            Key={
                'email': slots['email'],
                'password': slots['password']
            },
            UpdateExpression='SET address = :value1',
            ExpressionAttributeValues={
                ':value1': slots['data']
            }

        )

    elif slots['category'] == 'contact number':
        dynamo_table.update_item(

            Key={
                'email': slots['email'],
                'password': slots['password']
            },
            UpdateExpression='SET contact_number = :value1',
            ExpressionAttributeValues={
                ':value1': slots['data']
            }

        )

    elif slots['category'] == 'company name':
        dynamo_table.update_item(

            Key={
                'email': slots['email'],
                'password': slots['password']
            },
            UpdateExpression='SET company_name = :value1',
            ExpressionAttributeValues={
                ':value1': slots['data']
            }

        )

    elif slots['category'] == 'name':
        dynamo_table.update_item(

            Key={
                'email': slots['email'],
                'password': slots['password']
            },
            UpdateExpression='SET person_name = :value1',
            ExpressionAttributeValues={
                ':value1': slots['data']
            }

        )

    logger.debug('user account updated')

    try_ex(lambda: session_attributes.pop('currentRequest'))
    session_attributes['lastConfirmedRequest'] = user_updated_info

    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Update for account {} successful. '.format(slots['email'])
        }
    )


def dispatch(intent_request):

    # Called when the user specifies an intent for this bot.

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'],
                                                            intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to the bot's intent handlers
    if intent_name == 'Volunteer_qualification':
        return volunteer_qualifications(intent_request)
    elif intent_name == 'Volunteer_jobs':
        return volunteer_jobs(intent_request)
    elif intent_name == 'Donator_job':
        return donator_job(intent_request)
    elif intent_name == 'Driver_job':
        return driver_job(intent_request)
    elif intent_name == 'Receiver_job':
        return receiver_job(intent_request)
    elif intent_name == 'Sign_up_user':
        return sign_up(intent_request)
    elif intent_name == 'Account_update':
        return account_update(intent_request)
    elif intent_name == 'About_us':
        return about_us(intent_request)
    elif intent_name == 'Ending_message':
        return ending_message(intent_request)
    elif intent_name == 'Feedback':
        return feedback(intent_request)
    elif intent_name == 'Receiver_users':
        return receiver_users(intent_request)
    elif intent_name == 'Register_account':
        return register_account(intent_request)
    elif intent_name == 'Sign_in':
        return sign_in(intent_request)
    elif intent_name == 'Welcome_Message':
        return welcome_message(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):

    os.environ['TZ'] = 'Singapore'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
