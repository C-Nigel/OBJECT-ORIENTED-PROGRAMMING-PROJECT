import json
import time
import os
import logging
import boto3
import uuid
import re

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


def safe_int(n):
    """
    Safely convert n value to int.
    """
    if n is not None:
        return int(n)
    return n


def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def isvalid_country(city):
    valid_cities = ['afghanistan','albania','algeria','andorra','angola','antigua and barbuda','argentina','armenia',
                    'aruba','australia','austria','azerbaijan','bahamas','bahrain','bangladesh','barbados','belarus',
                    'belgium','belize','benin','bhutan','bolivia','bosnia and herzegovina','botswana','brazil','brunei',
                    'bulgaria','burkina faso','burma','burundi','cambodia','cameroon','canada','cabo verde',
                    'central african republic','chad','chile','china','colombia','comoros',
                    'congo, democratic republic of the','congo, republic of the','costa rica',"cote d'ivoire",'croatia',
                    'cuba','curacao','cyprus','czechia','denmark','djibouti','dominica','dominican republic',
                    'east timor','ecuador','egypt','el salvador','equatorial guinea','eritrea','estonia','eswatini',
                    'ethiopia','fiji','finland','france','gabon','gambia','georgia','germany','ghana','greece',
                    'grenada','guatemala','guinea','guinea-bissau','guyana','haiti','holy see','honduras','hong kong',
                    'hungary','iceland','india','indonesia','iran','iraq','ireland','israel','italy','jamaica','japan',
                    'jordan','kazakhstan','kenya','kiribati','north korea','south korea','kosovo','kuwait','kyrgyzstan',
                    'laos','latvia','lebanon','lesotho','liberia','libya','liechtenstein','lithuania','luxembourg',
                    'macau','macedonia','madagascar','malawi','malaysia','maldives','mali','malta','marshall islands',
                    'mauritania','mauritius','mexico','micronesia','moldova','monaco','mongolia','montenegro','morocco',
                    'mozambique','namibia','nauru','nepal','netherlands','new zealand','nicaragua','niger','nigeria',
                    'norway','oman','pakist,an''palau','palestinian territories','panama','papua new guinea','paraguay',
                    'peru','philippines','poland','portugal','qatar','romania','russia','rwanda',
                    'saint kitts and nevis','saint lucia','saint vincent and the grenadines','samoa','san marino',
                    'sao tome and principe','saudi arabia','senegal','serbia','seychelles','sierra leone','singapore',
                    'sint maarten','slovakia','slovenia','solomon islands','somalia','south africa','south sudan',
                    'spain','sri lanka','sudan','suriname','swaziland','sweden','switzerland','syria','taiwan',
                    'tajikistan','tanzania','thailand','timor-leste','togo','tonga','trinidad and tobago','tunisia',
                    'turkey','turkmenistan','tuvalu','uganda','ukraine','united arab emirates','united kingdom',
                    'uruguay','uzbekistan','vanuatu','venezuela','vietnam','yemen','zambia','zimbabwe'
]
    return city.lower() in valid_cities


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


def sign_up(slots):
    username = try_ex(lambda: slots['username'])
    password = try_ex(lambda: slots['password'])
    firstname = safe_int(try_ex(lambda: slots['firstname']))
    lastname = try_ex(lambda: slots['lastname'])
    email = try_ex(lambda: slots['email'])
    country_of_residence = try_ex(lambda: slots['residence'])

# have to add username, password, firstname and lastname checks here

    if email:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
        if match == None:
            return build_validation_result(False, 'Email', 'Email not recognised. Please retry.')

    if country_of_residence and not isvalid_country(country_of_residence):
        return build_validation_result(
            False,
            'Location',
            'We believe your country {} does not exist.  Please retry with full spelling?'.format(country_of_residence)
        )

# have to do confirmation
# have to write to  DynamoDB after confirmation
#    return {'isValid': True}


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
    elif intent_name == 'Sign_up':
        return sign_up(intent_request)
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


