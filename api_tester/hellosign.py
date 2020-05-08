from hellosign_sdk import HSClient
import time
import requests
import yaml
import os
import json

global apikey
import re

creds = yaml.load(open('creds.yml'))

########################################################################################################################
accountName = 'main'

if accountName is 'main':
    apikey = creds['mainHSAPIKEY']
    clientID = creds['mainHSClientID']
elif accountName is '':
    apikey = creds['']
    clientID = creds['']
elif accountName is 'al':
    apikey = creds['a']
    clientID = creds['al']
elif accountName is '':
    apikey = creds['']
    clientID = creds['']
elif accountName is 'freeAccount':
    apikey = creds['']
    clientID = creds['']
elif accountName is 'teamAdminTopRock':  # TEAM TESTING
    apikey = creds['']
    clientID = creds['']
elif accountName is 'teamManagerTopRock':
    apikey = creds['']
    clientID = creds['']
elif accountName is 'OAUTH_TESTING':  # OAUTH TESTING
    apikey = creds['']
    clientID = creds['']
    secret = creds['oAuth_customerPaysSecret']
elif accountName is '':
    apikey = creds['']
    clientID = creds['']
elif accountName is 'testAccount':
    apikey = creds['APIKEY']
    clientID = 'test'
elif accountName is '4':
    apikey = creds['4HSAPIKEY']
    clientID = creds['4HSClientID']

client = HSClient(api_key=apikey)
print(client.version)

########################################################################################################################

########################################################################################################################

_myRecentSigRequest = ''  # set in exploreSignatureRequestResponseObject

listOfSignRequests = []  # used in exploreSignatureRequestResponseObject

global lastSigRequest  # used in exploreSignatureRequestResponseObject
lastSigRequest = 'lastSigRequestXXX'
global lastSigID  # used in exploreSignatureRequestResponseObject
lastSigID = 'lastSigIdXXXX'

_myDictSignatureRequestID_ToEmail = {}  # used in exploreSignatureRequestResponseObject

# Test Emails
fletch_email = creds['fletch_email']
fletch2_email = creds['fletch2_email']


######################################################################################################################

# used in exploreSignatureRequestResponseObject
def convertUTCtoLocal(utcValue):
    if utcValue != None:
        print('nonempty time value given')
        return time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(float(utcValue)))
    else:
        return "Empty time value given"


# Used in various test scripts in this file
# Create a function to get a text file and put it into a string
# http://www.blindtextgenerator.com/lorem-ipsum
# 400.txt has 400 characters
def readInFile(filetype):
    if filetype is 'large':
        file = open("1000.txt", "r")
    else:
        file = open("200.txt", "r")
    mytext = file.read()
    return mytext


# used in test scripts
def exploreTemplateResponseObject(templateResponseObject):
    print("********************************************BEGIN exploreTemplateResponseObject********************")
    print(templateResponseObject.template_id)
    print(" = template ID \n")
    print(templateResponseObject.template_id)
    print(" = template ID \n")
    print(templateResponseObject.custom_fields)
    print(" = custom_fields")
    for field in templateResponseObject.custom_fields:
        print(field)
    print(" = roles")
    print(templateResponseObject.signer_roles)

    print("********************************************END exploreTemplateResponseObject********************")


# used in test scripts
def exploreUnclaimedDraftResponseObject(responseObject):
    print("********************************************BEGIN exploreTemplateResponseObject********************")
    print(responseObject)
    print(" = responseObject\n")
    print(responseObject.claim_url)
    print(" = claim_url\n")
    print(responseObject.signing_redirect_url)
    print(" = signing_redirect_url\n")
    # print(responseObject.expires_at)
    # print(" = expires_at\n")
    print(responseObject.test_mode)
    print(" = test_mode\n")
    print(responseObject.signature_request_id)

    print(" = signature_request_id")
    print("********************************************END exploreTemplateResponseObject********************")


def exploreSignatureRequestResponseObject(responseObject):
    print("********************************************BEGIN exploreSignatureRequestResponseObject********************")
    print(responseObject.files_url)
    print(" = files_url\n")
    print(responseObject.signing_url)
    print(" = signing_url")
    print(responseObject.details_url)
    print(" = details_url")

    print(type(responseObject.custom_fields))
    print(" = custom_fields - LIST")
    print(len(responseObject.custom_fields))
    for field in responseObject.custom_fields:
        print(field)

    print(responseObject.test_mode)
    print(" =TEST MODE\n")
    print(responseObject.requester_email_address + " =Requester_email_address\n")
    print(responseObject.title)
    print(" =title\n")
    # print(responseObject.message + " =message\n") ----WHY IS THIS CAUSING AN ERROR????
    print(responseObject.has_error)
    print(" =has_error\n")
    print(responseObject.final_copy_uri + " = final_copy_uri\n")
    print(responseObject.subject + " =subject\n")
    print(responseObject.is_complete)
    print(" = is_complete\n")
    print(responseObject.response_data)
    print(" = response_data\n")
    print(responseObject.signatures)
    global _myRecentSigRequest
    for x in responseObject.signatures:
        print(x)
        print(" = x\n")
        print(x.signature_id)
        global lastSigID
        lastSigID = x.signature_id
        # _myRecentSigRequest = x.signature_id
        print(" = x.signature_id\n")
        listOfSignRequests.append(x.signature_id)
        print(x.signer_email_address)
        print(" = x.signer_email_address\n")

        _myDictSignatureRequestID_ToEmail[x.signature_id] = x.signer_email_address

        print(x.signer_name)
        print(" = x.signer_name\n")
        print(x.status_code)
        print(" = x.status_code\n")

        print("--------Begin last reminded at")
        print(x.last_reminded_at)
        print(" = x.last_reminded_at")
        print(convertUTCtoLocal(x.last_reminded_at))
        print("--------END last reminded at")
        print("--------Begin last signed at")
        print(x.signed_at)
        print(" = x.signed_at")
        print(convertUTCtoLocal(x.signed_at))
        print("--------END last signed at")
        print("--------BEGIN last viewed at")
        print(x.last_viewed_at)
        print(" = x.last_viewed_at")
        print(convertUTCtoLocal(x.last_viewed_at))
        global lastSigRequest
        lastSigRequest = responseObject.signature_request_id
        _myRecentSigRequest = responseObject.signature_request_id
        print('lastSigRequest')
        print(lastSigRequest)
        print('lastSigID')
        print(lastSigID)
        print("--------END last viewed at")
    print("********************************************END exploreSignatureRequestResponseObject********************")
    print(" = signatures\n")
    print(type(responseObject))
    print("The above is the type of response object just explored\n")
    # To find things I can pump out, just go to the documentation and look at response.
    print(
        "****************************************************exploreSignatureRequestResponseObject********************")


def runmain():
    menu_item = 'tom'
    while (menu_item is not 111):
        print("\n")
        print("\n")
        print("MENU\n")
        print("")

        print("1 - Signature Request Get files - Get a copy of the document")
        print("2 - GET signature_request")
        print("3 - Send signature_request")
        print("4 - Send_with_template NO CUSTOM FIELDS")
        print("5 - Embedded Requesting")
        print("6 - Embedded Signature request with template")
        print("7 - Embedded Signature - part two - get the URL with the signature ID")

        print("8 - Delete all unsigned documents that are out for signature")
        print("9 - Delete all unsigned documents that are out for signature")
        print("10 - Embedded Signature request")

        print("11 - Get a url for an unathenticated link to a file to download")
        print("12 - Create an unclaimed draft embedded")
        print("13 - Create a nonembedded signature request")
        print("14: Create embedded unclaimed draft with template\n")
        print("15: AccountInfoReturned\n")

        print("16: Send a reminder for a request")
        print("17: Cancel a signature request")

        print("18: Get template info ")
        print("19 - TO BE IMPLEMENTED")
        print("20 - TO BE IMPLEMENTED")
        print("21 - Unclaimed Draft Edit and Resend")
        print("22 - Requests - blah")

        print("23 - Embedded Template Walkthrough STEP 1 - Create a template draft (create embedded draft)")
        print("24 - Embedded Template Walkthrough STEP 2 - Embedded signing using template from 23 ")
        print("25 - Get Template object")
        print("26 - Previewing a signature request - part of embedded template walkthrough")
        print("27 - Do a non-embedded signature request with an email")
        print("28  - template ordering ticket ")

        # REQUESTING
        print("29  - non-embedded requesting")

        # Embedded Templates
        print("30  - Embedded Templates")

        print("31 - Update embedded signature request")

        print("32 - Delete all templates function ")

        # REQUESTS FUNCTIONS
        print("33 - OLD4 - Send_with_template BUT WITH REQUESTS NOT SDK")
        print("34 - OLD6 - Embedded Signature request with template BUT WITH REQUESTS NOT SDK")

        print("35 - Update a signature request")

        print("36 - Delete a template draft")

        # OAUTH EXPLORATION

        print("37 - OAuth embedded call part one")
        print("38 - OAUTH embedded call part two")

        print("39 - OAuth nonembedded signature call with template")
        print("40 - hardcode getting an embedded temp URL")
        print("41 - Search fields")

        print("42 - Basic Template with Custom Fields")

        print("44 - Open up a test embedded page")
        print("45 - Update the Callback URL for the app you are using")
        print("46 - Non-embedded signature request passing Client ID")
        print("47 - Get a temporary URL from a signature ID ")
        print("48 - Signer Reassignment")

        print("50 - getTemplate")

        # API APP STUFF
        print("51 - Get API App - function missing from SDK using requests")
        print("52 - List API Apps - function missing from SDK using requests")

        print("53 - 53 Create API Apps - function missing from SDK using request")
        print("54 - 54 Update API Apps - function missing from SDK using request")

        # OAuth walkthrough stuff
        print("55 - Retrieving the OAuth token")
        print("56 - Verify an existing account")
        print("57 - Create an account")
        print("58 - token refresh")

        print("59 - signer group")
        print("60 - Requests Send embedded with text tag custom fields")

        print("110: Get current state data for application")
        print("111: EXIT because these go to 11!!!!\n")

        # From the API get the account email and client ID to print out.
        print("BEGIN ACCOUNT INFO")
        account_info = client.get_account_info()
        print(clientID)
        print(account_info.email_address)
        print(str(account_info.is_paid_hs) + " is a paid account")
        print(account_info.quotas)
        print("END ACCOUNT INFO")

        menu_item = input("Enter a number")
        patternToMatch = '^[A-Za-z0-9]{30,}$'  # later we check if the number is a signature request ID

        if menu_item == "1":

            print("****************************************************1 - client.get_signature_request_file START***************")

            # sample = 964146cf5afa0bbfdde817ca9d000d718706e27d'
            current_signatureRequestID = input("Enter the SignatureRequestID to update that you want to download\n")

            whatDoIReturn = client.get_signature_request_file(
                # current_signatureRequestID,
                signature_request_id=current_signatureRequestID,
                filename='FriendGreenTomatoes3.zip',  # or .zip
                file_type='pdf'  # or .pdf
                )

            print(type(whatDoIReturn))
            print(whatDoIReturn)
            print(os.path.realpath(__file__))

            print(
                "****************************************************1 - client.get_signature_request_file END**********")
        elif menu_item == "2":
            print(
                "****************************************************2 GET signature_request - START**********************")

            # test example 51211b2cb66cca5ddb1c00d553f340f528262eef
            current_signatureRequestID = input("Enter the SignatureRequestID to update that you want to download\n")

            response = client.get_signature_request(current_signatureRequestID)

            exploreSignatureRequestResponseObject(response)
            print(response)

            print(
                "****************************************************2 GET signature_request - END**********************")
        elif menu_item == "3":
            print(
                "****************************************************3 - client.send_signature_request START************")

            # readInFile is an internal function in this file. It reads files 1000.txt if name is large otherwise 200.txt
            # 200.txt is 1000 characters.
            # reallylongfromfile = readInFile('largeuuu')
            # reallylongfromfile = "happy"
            # print(reallylongfromfile)

            response = client.send_signature_request(
                test_mode=True,

                # client_id=clientID, SDK can't take client id!
                title="testing query",
                subject="testing query",
                message="Testing query parameter",
                # hide_text_tags=False,
                use_text_tags=False,
                signers=[
                    {'email_address': fletch_email, 'name': 'Ed'},
                    {'email_address': fletch2_email, 'name': 'Jill'}

                    ],
                # metadata={
                #        'client_id': '1234',
                #        'custom_text': reallylongfromfile
                #    },
                files=['nda.pdf']
                )

            exploreSignatureRequestResponseObject(response)
            print(response)

            print(
                "****************************************************3 - client.send_signature_request END**************")

        elif menu_item == "4":
            print(
                "****************************************************4 - client.send_with_template NO CUSTOM FIELDS - START***************")

            try:
                response = client.send_signature_request_with_template(
                    test_mode=True,
                    template_id='e1b807e58b10ddf8ca841eb05ebeae81a9f5a300',
                    message='Template with no custom fields',
                    metadata={
                        'client_id': '1234'
                        },
                    signers=[{'role_name': 'signer1', 'name': 'George', 'email_address': fletch_email}],
                    # custom_fields=[{"name":"fName", "value":"Helaine", "editor":"Client", "required":True}, {"name":"lName", "value":"OConnor", "editor":"Client", "required":True}]
                    custom_fields=[{"fName": "Helaine", "lName": "OConnner"}]

                    )

                exploreSignatureRequestResponseObject(response)
                print(response)
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print("\n")

            print(
                "****************************************************4 - client.send_with_template NO CUSTOM FIELDS - END*****************")

        elif menu_item == "5":
            print(
                "****************************************************5 Embedded requesting - START**********************")

            # Embedded Requesting - allows you to have users create and send signature requests on your site as an iFrame

            # First step is to create a draft signature request from your backend using our API

            # YOU NEED TO WRITE DOWN CALLBACK PROCESS FOR THIS - and code this up in the callbacks.

            embeddedSigning = True

            response = client.create_embedded_unclaimed_draft(
                test_mode=True,
                client_id=clientID,
                draft_type='request_signature',
                requester_email_address=fletch_email,  # not sure what requester is in this case
                files=['NDA.pdf'],
                is_for_embedded_signing=embeddedSigning
                )

            print(response)
            exploreUnclaimedDraftResponseObject(response)

            '''
    
                Is_for_embedded_signing = True
                - you get the signature_request_sent callback
                - get the signature ID from that (no email is sent for this even though that is the callback)
                - use get embedded url to get the url to get to the user. Number 47 in this app
                - signature_request_signed, signature_request_downloadable, signature_request_all_signed callbacks
    
                Is_for_embedded_signing = False
                - signature_request_sent
    
    
            '''

            print(
                "****************************************************5 Embedded requesting - END**********************")
        elif menu_item == "6":
            print(
                "****************************6 - Embedded Signature request with template - START**********************")

            reallylongfromfile = readInFile('largeuuu')
            # print(reallylongfromfile)

            response = client.send_signature_request_embedded_with_template(
                test_mode=True,
                metadata={
                    'client_id': '1234',
                    'custom_text': reallylongfromfile
                    },
                client_id=clientID,
                # file["NDA.pdf"],
                template_id='f7778c9a357c7ab5f8bc696754db1b7be105c705',
                title='ticket 256438',
                subject='ticket 256438',
                message='ticket 256438',
                signers=[{'role_name': 'Signer1', 'name': 'George', 'email_address': fletch_email},
                         {'role_name': 'Signer2', 'name': 'George', 'email_address': fletch2_email}]

                )

            print(response)
            print(type(response))
            exploreSignatureRequestResponseObject(response)

            print(
                "****************************6 - Embedded Signature request with template - END**********************")
        elif menu_item == "7":

            if len(listOfSignRequests) > 0:
                mySignatureID = listOfSignRequests.pop(0)
                response = client.get_embedded_object(mySignatureID)
                print(mySignatureID + " =signatureID")
                print(_myDictSignatureRequestID_ToEmail[mySignatureID])

                _mySignID_ToCancel = mySignatureID
                print(response)
            else:
                print("There are no signature requests left")
        elif menu_item == "8":

            print(
                "*************8 - Delete all unsigned documents that are out for signature - START**********************")
            print("TEST8")
            response = client.get_signature_request_list()

            for x in response:
                strSigRequest = str(x)
                mylist = strSigRequest.split()
                print(mylist)

                if x.is_complete == False:

                    print(mylist[1] + " Not Complete")
                    # exploreSignatureRequestResponseObject(x)

                    if str(mylist[1]) == '70ed1261cbd8ef8d361b62110e291bbc7a7aceba':
                        print("This is the one created by the end-user product")

                    if str(mylist[1]) == 'd3a751bd8bdb1d2a7f48960ff400f9c5ac60d046':
                        print("This is the one created by the API")
                else:
                    # The request is complete
                    print(mylist[1] + " Complete!")

            print(
                "*************8 - Delete all unsigned documents that are out for signature - END**********************")
        elif menu_item == "9":

            print(
                "****************************************************Delete a sign request - START**********************")
            try:
                print("hello")
                cancelResponse = client.cancel_signature_request('98be5903de697cddbdf35b5c0c8f7dfdb37ad8b7')
                print(cancelResponse)
                print('\n')
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print("\n")

            print(
                "****************************************************Delete a sign request - END**********************")
        elif menu_item == "10":

            print("****************************************************Embedded Request - START**********************")
            # reallylongfromfile = readInFile('large')
            # print(reallylongfromfile)

            response = client.send_signature_request_embedded(

                test_mode=True,
                client_id=clientID,
                # files=["Viva-Finance-Draft-Loan-Contract.pdf"],
                files=["nda.pdf"],
                title="embedded",
                subject="This is a test sig request embedded SUBJECT",
                message="This is a test sign request embedded MESSAGE",
                signers=[
                    {'email_address': fletch_email, 'name': 'andrew'},
                    {'email_address': fletch_email, 'name': 'freedom'}

                    ],
                cc_email_addresses=[fletch2_email],

                )
            exploreSignatureRequestResponseObject(response)
            print(response)
            print("****************************************************Embedded Request - END**********************")
        elif menu_item == "11":

            print(
                "****************************************************11 Get a link to download the document - START**********************")

            response = client.get_signature_request_file(
                signature_request_id='d347d8f9c5cc30fa0b10c0cd2168a9f2de6375a4',
                filename='filesWHAT.pdf',
                file_type='pdf'
                # get_url = True #not in the SDK I don't think
                )

            print(response)

            print(
                "****************************************************11 Get a link to download the document - END**********************")
        elif menu_item == "12":

            print("**********************12 Create embedded unclaimed draft - START**********************")

            reallylongfromfile = readInFile('largeuuu')
            print(reallylongfromfile)

            response = client.create_embedded_unclaimed_draft(
                test_mode=True,
                client_id=clientID,
                metadata={
                    'client_id': '1234',
                    'custom_text': reallylongfromfile
                    },
                draft_type='request_signature',
                requester_email_address=fletch2_email,
                is_for_embedded_signing=True,
                subject='Ticket 206582',
                files=['nda.pdf']
                )

            print("**********************12 Create embedded unclaimed draft - END**********************")
            print("A change")
        elif menu_item == "13":

            print(
                "***********************13 non embedded signature request (with Text Tags) - START**********************")
            response = client.send_signature_request(
                test_mode=True,
                use_text_tags=True,
                title="nonembedded signature request with text tags",
                subject="nonembedded signature request with text tags",
                message="Please sign this NDA and then we can discuss more. Let me know if you have any questions.",
                signers=[
                    {'email_address': fletch_email, 'name': 'fletch'},
                    {'email_address': fletch_email, 'name': 'spike'}
                    ],
                files=['nda.pdf'],
                metadata={
                    'client_id': '1234',
                    'custom_text': 'NDA #9'
                    }
                )

            print(response)
            print(
                "******************************13 non embedded signature request (with Text Tags) - END**********************")
        elif menu_item == "14":

            print("***************14 embeded request with template - START**********************")

            signers = [{
                "name": "Signer Name",
                "email_address": "signer@example.com",
                "role_name": "Signer"
                }]
            metadata = {
                'account_id': '123',
                'company_name': 'Acme Co.'
                }

            templateDraft = client.create_embedded_unclaimed_draft_with_template(
                test_mode=True,
                client_id=clientID,
                is_for_embedded_signing=True,
                template_id='b71e165713bffb1dcd6bcb9a9d184250bb829a64',
                requester_email_address=fletch2_email,
                title='MyDraft',
                subject='Unclaimed Draft Email Subject',
                message='Email Message',
                signers=signers,
                signing_redirect_url='http://url.com',
                requesting_redirect_url='http://url.com',
                metadata=metadata
                )
            url = templateDraft.claim_url
            print(templateDraft)
            print("*************14 embedded request with template - END**********************")

        elif menu_item == "15":

            print(
                "****************************************************15 HIT Account info - START**********************")

            response = client.get_account_info()
            print(response.account_id)
            print(response.email_address)
            print(response.is_paid_hs)
            print(response.quotas)

            client.update_account_info()
            print("****************************************************15 Account info - END**********************")

        elif menu_item == "16":

            print("***************************************16 Send Reminder Request- START**********************")
            response = client.remind_signature_request(
                signature_request_id='a790f030ed1946937ff1e1345efbeb5753a1b3e1',
                email_address=fletch_email
                )

            print(response)
            print("****************************************16 Send Reminder Request - END**********************")

        elif menu_item == "17":

            print("***************************************17 Cancel a signature request START**********************")
            #https://app.hellosign.com/api/reference#cancel_incomplete_signature_request
            # Must listen to the callback handler for this test
            response = client.cancel_signature_request('d1d5372cbaa5e769fc64042a71d420a1ee3404ea')

            print(response)
            print("****************************************17 Cancel a signature request END**********************")
        elif menu_item == "18":

            print("***************************************18 Get template info**********************")

            response = client.get_template('b71e165713bffb1dcd6bcb9a9d184250bb829a6418')

            print(response)
            exploreTemplateResponseObject(response)

            print("****************************************18 Get template info*****************")

        elif menu_item == "19":
            print("***************************************19 TO BE IMPLEMENTED**********************")

            print("***************************************19 TO BE IMPLEMENTED**********************")

        elif menu_item == "20":
            print("************************************20 TO BE IMPLEMENTED ************************************")

            print("************************************20 TO BE IMPLEMENTED ************************************")

        elif menu_item == "21":

            print(
                "***************************************20 TO BE IMPLEMENTED START**********************")

            current_signatureRequestID = 'd347d8f9c5cc30fa0b10c0cd2168a9f2de6375a4'
            buildTheRequest = 'https://' + apikey + ':@api.hellosign.com/v3/signature_request/files/' \
                              + current_signatureRequestID + "?get_url=True"

            r = requests.get(buildTheRequest)
            urlOfDocument = r.text
            urlOfDocument = urlOfDocument.replace("\\", "")
            print(urlOfDocument)

            print(
                "***************************************21 Unclaimed Draft Enit and Resend - END**********************")
            print("A change")

        elif menu_item == "22":

            print("****************************************************22 - START**********************")

            buildTheRequest = 'https://' + apikey + ':@api.hellosign.com/v3/signature_request/send_with_template'

            data = {
                'client_id': clientID,
                'template_id': 'cab3aad3f35b529b5af0bc07d77888aa0d3f4bde',
                'subject': 'ticket',
                'allow_decline': '1',
                'message': 'ticket214090',
                'signers[Signer1][name]': 'George',
                'signers[Signer1][email_address]': fletch2_email,
                'custom_fields': '[{"name":"name", "value":"a", "editor":"Signer1", "required":"True"]',
                'test_mode': '1'
                }
            print(buildTheRequest)

            r = requests.post(buildTheRequest, data)
            print(r.text)
            stringData = r.text
            print(type(stringData))

            result = json.loads(stringData)
            print("****************************************************22 - END**********************")

        elif menu_item == "23":

            print(
                "*********23 Embedded Template Walkthrough STEP 1 - Create a template draft (create embedded draft) - START**********************")

            files = ["nda.pdf"]
            # signer_roles = [
            #    {'name': 'Baltar', 'order': 1},
            #    {'name': 'Madame President', 'order': 2},
            #    {'name': 'Lee Adama', 'order': 3},
            # ]
            signer_roles = [
                {'name': 'Baltar'},
                {'name': 'Madame President'},
                ]
            cc_roles = ['Deck Chief', 'Admiral', 'Starbuck_Alen']
            merge_fields = [{'name': 'mymerge', 'type': 'text'}]

            template_draft = client.create_embedded_template_draft(
                client_id=clientID,
                signer_roles=signer_roles,
                test_mode=True,
                files=files,
                title='Battlestar Test Draft',
                # subject='There are cylons onboard',
                message='Halp',
                cc_roles=cc_roles,
                merge_fields=merge_fields,

                )

            template_id = template_draft.template_id

            template_url = template_draft.edit_url
            print(template_url)

            # signer_roles = [
            #    {'name': 'SignerNumber1', 'order': 1},
            #    {'name': 'SignerNumber2', 'order': 2},
            #    {'name': 'SignerNumber3', 'order': 3},
            # ]

            # cc_roles = ['Chief', 'Admiral', 'Starbuck']
            # merge_fields = [{'name': 'mergeField0', 'type': 'text'}, {'name':'mergeField1', 'type':'text'}, {'name':'mergeField2', 'type':'text'},
            #                {'name': 'mergeField3', 'type': 'text'},{'name':'mergeField4', 'type':'text'},{'name':'mergeField5', 'type':'text'},
            #                {'name': 'mergeField6', 'type': 'text'},{'name':'mergeField7', 'type':'text'},{'name':'mergeField8', 'type':'text'}]

            print(
                "********23 Embedded Template Walkthrough STEP 1 - Create a template draft (create embedded draft) - END**********************")

        elif menu_item == "24":

            print(
                "********Embedded signing With the template created from embedded template - START**********************")

            response = client.send_signature_request_embedded_with_template(
                # test_mode=True,
                client_id=clientID,
                template_id='0c0f704c28001e583413a824a43784176b1d0cd1',
                # subject='My First embedded signature request with a template',
                # message='Awesome, right?',
                signers=[
                    {'role_name': 'Baltar', 'email_address': fletch_email, 'name': 'JackFirst'},
                    # dcce76f1016a40001c01420747f8db00
                    {'role_name': 'Madame President', 'email_address': fletch_email, 'name': 'JillSecond'},
                    # 5ccf259e9d69bc16b1aab21ef9bc2531
                    {'role_name': 'Lee Adama', 'email_address': fletch_email, 'name': 'BillThird'}
                    # c9aac5100deaa344d0a5b3f132575068
                    ],
                )

            print("******Embedded signing with the template created from embedded template - END**********************")
            print(response)
            exploreSignatureRequestResponseObject(response)



        elif menu_item == "25":

            print("*****************GET TEMPLATE - START**********************")


            response = client.get_template('b71e165713bffb1dcd6bcb9a9d184250bb829a64')

            exploreTemplateResponseObject(response)

            print("*****************GET TEMPLATE - END**********************")
        elif menu_item == "26":

            print( "********26 - Previewing a signature request - part of embedded template walkthrough - START************")

            signers = [
                {'role_name': 'Baltar', 'email_address': fletch2_email, 'name': 'JackFirst'},
                {'role_name': 'Madame President', 'email_address': fletch2_email, 'name': 'JillSecond'},
                {'role_name': 'Lee Adama', 'email_address': fletch2_email, 'name': 'BillThird'}
                ]
            metadata = {
                'account_id': '123',
                'company_name': 'Acme Co.'
                }



            custom_fields = [{'mymerge': 'George'}]

            templateDraft = client.create_embedded_unclaimed_draft_with_template(
                # test_mode=True,
                client_id=clientID,
                is_for_embedded_signing=True,
                template_id='29963830f417f01d1b99202c0029fe21348649d8',  # _templateIDHardCode,
                requester_email_address=fletch_email,
                title='MyDraft',
                subject='WHAT IS HAPPENING HERE ????????',
                message='Email Message',
                signers=signers,
                # custom_fields=custom_fields,
                signing_redirect_url='http://url.com',
                requesting_redirect_url='http://url.com',
                metadata=metadata
                )
            url = templateDraft.claim_url
            print(url)
            exploreUnclaimedDraftResponseObject(templateDraft)

            print("********26 - Previewing a signature request - part of embedded template walkthrough  - END*************")
        elif menu_item == "27":

            print(
                "***************************27 - Generate embedded signining from template draft - START****************")

            print(
                "***************************27 - Generate embedded signing from template draft - END********************")

        elif menu_item == "28":

            print("*******************************28 Template ordering ticket - START**********************")

            template1IssuerOnly = 'edc774ff42f21aeca9ca8a09b538634a9312443e'
            template2SubscriberOnly = '1e1fc38122edb1405ea3ff3a6f15e5e4e1d51a20'
            template3_IssuerFirst = '99b73eec927c10ddb7a96a1da76ef80a45466d56'
            template3_SubscriberFirst = '2345e6f4a3a03693d57413b011d9655295c90738'
            response = client.send_signature_request_with_template(
                test_mode=True,
                template_ids=[template1IssuerOnly, template2SubscriberOnly, template1IssuerOnly,
                              template2SubscriberOnly,
                              template3_IssuerFirst],
                title='simple test',
                subject='Ticket 216247 - simple test',
                message='Recreation of 216247 TICKET ',
                signers=[
                    {'role_name': 'Issuer', 'email_address': fletch_email, 'name': 'Jack'},
                    {'role_name': 'Subscriber', 'email_address': fletch_email, 'name': 'Jill'}
                    ]
                )

            exploreSignatureRequestResponseObject(response)
            print(response)

            print("*******************************28 Template ordering ticket - END**********************")

        elif menu_item == "29":

            print("***********************************29 NON Embedded Requesting - START**********************")

            response = client.create_unclaimed_draft(test_mode=True,
                                                     draft_type='request_signature',
                                                     files=['NDA.pdf'])

            print(response.signature_request_id)
            print(response.claim_url)

            print("***********************************29 NON Embedded Requesting - END**********************")

        elif menu_item == "30":

            print("***************************Edit Embedded Templates - START**********************")

            embeddedObj = client.get_template_edit_url('279aca04dc4d3505a65e3ccab2c23c623c38a012')
            edit_url = embeddedObj.edit_url
            print(edit_url)

            #  https://www.npmjs.com/package/local-web-server

            print("***************************Edit Embedded Templates - END**********************")

        elif menu_item == "31":

            print("***************31 Update embedded signature request 31 - START**********************")

            # non-embedded signature request
            updateSignatureRequest = input("Enter the SignatureRequest to update without an appended signature page\n")

            response = client.get_signature_request(updateSignatureRequest)

            for x in response.signatures:
                print(x.signature_id)
                print(x.signer_email_address)
                changeAddress = input("Enter a 1 to change this email address and a 0 to leave it as is:")
                if changeAddress == "1":
                    updateEmailAddress = input("Enter the new email address for this signer")
                    response = client.update_signature_request(updateSignatureRequest, x.signature_id,
                                                               updateEmailAddress)

            response = client.get_signature_request(updateSignatureRequest)
            for x in response.signatures:
                print(x.signature_id)
                print(x.signer_email_address)

            print("*************31 Update embedded signature request 31 - END**********************")

        elif menu_item == "32":

            print("**********************************32 - Delete all templates function  - START**********************")

            response = client.get_template_list(page_size=1)
            count = 0
            for templateObj in response:
                temp = Template
                temp.template_id = templateObj.template_id
                temp.message = templateObj.message

                for item in templateObj.documents:
                    print(len(item))

                for sr in templateObj.signer_roles:
                    temp.add_signerRole(sr)

                print(temp.__str__())
                print(temp.__dict__)
            print("**********************************32 - Delete all templates function  - END**********************")

        elif menu_item == "33":
            print("*****33 - OLD4 - Send_with_template BUT WITH REQUESTS NOT SDK - START**********************")

            # POST https://[api key]:@api.hellosign.com/v3/signature_request/send_with_template
            buildTheRequest = 'https://' + apikey + \
                              ':@api.hellosign.com/v3/signature_request/send_with_template'

            data = {
                'signers': {
                    {'role_name': 'client1', 'name': 'George', 'email_address': fletch_email},
                    {'role_name': 'client2', 'name': 'Sally', 'email_address': fletch_email}}
                ,
                'test_mode': True,
                'template_id': '22de7156f350fac8d4100b558219aa6eb8cc2601',
                'subject': 'TEST TICKET NUMBER - 209257',
                'message': 'TEST ticket number - 209257'
                }
            print(buildTheRequest)

            r = requests.post(buildTheRequest, data)
            print(r.text)
            stringData = r.text
            # print(type(stringData))

            result = json.loads(stringData)
            print(result)

            print("*****33 - OLD4 - Send_with_template BUT WITH REQUESTS NOT SDK - END**********************")


        # print("34 - OLD6 - Embedded Signature request with template BUT WITH REQUESTS NOT SDK")
        elif menu_item is "34":

            print(
                "***34 - OLD6 - Embedded Signature request with template BUT WITH REQUESTS NOT SDK - START*************")
            print("***34 - OLD6 - Embedded Signature request with template BUT WITH REQUESTS NOT SDK - END********")

        elif menu_item is "35":

            print(
                "****************************************************35 Update signature_request - START**********************")

            # print(lastSigRequest)
            # print(lastSigID)
            signatureID = '9ffd827fca0b7fce1842102485fec3e0'
            signatureRequestID = 'c9bb689a76257f36412920e6a2be2adca9a11131'

            buildTheRequest = 'https://' + apikey + \
                              ':@api.hellosign.com/v3/signature_request/update/' + signatureRequestID

            # r = requests.post('http://httpbin.org/post', data={'key': 'value'})

            data = {
                'signature_id': signatureID,
                'email_address': fletch_email
                }
            print(buildTheRequest)

            r = requests.post(buildTheRequest, data)
            print(r.text)
            stringData = r.text

            result = json.loads(stringData)

            print(result)

            print(
                "**********************************************35 Update signature_request -  END**********************")

        elif menu_item is "36":

            # Drafts have document id: 65a7eafb50cae3eabd4a52e6727d42ec39749f9a

            print("***36 - Delete a template draft  - START*************")
            client.delete_template('65a7eafb50cae3eabd4a52e6727d42ec39749f9a')
            print("***36 - Delete a template draft END********")

        elif menu_item is 37:

            print("*************37 OAuth embedded call part one - START**********************")

            response = client_OAUTH.send_signature_request_embedded(
                # test_mode=True,
                client_id=clientID,
                title='Sent Through OAUTH',
                subject='OAUTH',
                message='Please sign this NDA and then we can discuss more. Let me know if you have any questions.',
                signers=[
                    {'email_address': fletch_email, 'name': 'Jack'},
                    {'email_address': fletch_email, 'name': 'Jill'}
                    ],
                cc_email_addresses=['lawyer@example.com', 'lawyer2@example.com'],
                files=['NDA.pdf']
                )
            print(response)

            exploreSignatureRequestResponseObject(response)

            print("*************37 OAuth embedded call part one - END**********************")

        elif menu_item is "38":

            print("************38 OAuth embedded call part two - START**********************")

            print("************38 OAuth embedded call part two - END**********************")

        elif menu_item is "40":
            print("************40 Hardcode an embedded 2nd call  START**********************")

            client.get_embedded_object('d43657ea2a2a6d4fcd7f069036eee8dd')
            print("************40  Hardcode an embedded 2nd call END**********************")
        elif menu_item is "41":
            print("*************41 Search fields*******************************************")

            # does the Python SDK pass these queryies?
            response = client.get_signature_request_list(page=1)

            print(response)

            for sig in response:
                print(sig.signature_request_id)

            print("*************41 Search fields ******************************************")

        elif menu_item is "42":
            print(
                "***********************42 - Basic Template with Custom Fields non-embedded    ******************************")

            response = client.send_signature_request_with_template(
                test_mode=True,
                template_id=basicTemplateCustomField,
                subject='Purchase Order',
                message='Glad we could come to an agreement.',
                signers=[{'role_name': 'Client', 'name': 'George', 'email_address': fletch2_email}],
                custom_fields=[{'firstName': 'Alex'}, {'lastName': 'OConnor'}]
                )

            print(response)

            print(
                "***********************42 - Basic Template with Custom Fields non-embedded ********************************")
        elif menu_item is "43":
            print(
                "****************************************************43 - client.send_with_template CUSTOM FIELDS - START***************")

            reallylongfromfile = readInFile('largeuuu')
            print(reallylongfromfile)

            response = client.send_signature_request_with_template(
                # test_mode=True,
                template_id='dc9972a8c3ef5f5667759e65d12a56497ae7ce4a',
                # subject='TEST TICKET NUMBER - 209257',
                # message='TEST ticket number - 209257',
                metadata={
                    'client_id': '1234',
                    'custom_text': reallylongfromfile
                    },
                signers=[{'role_name': 'Client1', 'name': 'George', 'email_address': fletch_email}],
                custom_fields=[{'test': 'George Clooney'}]

                )

            exploreSignatureRequestResponseObject(response)
            print(response)

            print(
                "****************************************************43 - client.send_with_template  CUSTOM FIELDS - END*****************")

        elif menu_item is "44":

            print("*************44 open up an embedded teste site - START**********************")

            # import codecs
            # f = codecs.open("index.html", 'r')
            # print(f.read())

            import webbrowser

            url = "https://my-static-site-alexmcferron.herokuapp.com/"
            webbrowser.open(url, new=2)

            print("************44 open up an embedded test site END**********************")
            print("45 - Update the Callback URL for the app you are using")

        elif menu_item is "45":

            print("*************45 Update the callback url for the app you are using  START**********************")

            buildTheRequest = 'https://' + apikey + \
                              ':@api.hellosign.com/v3/api_app/' + clientID

            # r = requests.post('http://httpbin.org/post', data={'key': 'value'})

            data = {
                'callback_url': 'http://b816ec9e.ngrok.io/post'  # ,

                }
            print(buildTheRequest)  # fletch_email

            r = requests.post(buildTheRequest, data)
            print(r.text)
            stringData = r.text

            result = json.loads(stringData)

            print(result)

            print("************45 Update the callback url for the app you are using**********************")
            print("46 - Non-embedded signature request passing Client ID")

        elif menu_item is "46":

            print("*************46 - Non-embedded signature request passing Client ID  START**********************")

            buildTheRequest = 'https://' + apikey + \
                              ':@api.hellosign.com/v3/signature_request/send'

            # r = requests.post('http://httpbin.org/post', data={'key': 'value'})

            data = {
                'client_id': clientID,
                'file_url': 'https://i.ytimg.com/vi/JPA_rzHDy6o/maxresdefault.jpg',
                'subject': 'test production',
                'allow_decline': '0',
                'message': 'test',
                'signers[0][group]': 'groupie',
                'signers[0][0][name]': 'George',
                'signers[0][0][email_address]': fletch_email,
                'signers[0][1][name]': 'Ed',
                'signers[0][1][email_address]': fletch_email,
                'test_mode': '1'

                }

            print(buildTheRequest)

            r = requests.post(buildTheRequest, data)
            print(r.text)
            stringData = r.text
            # print(type(stringData))

            result = json.loads(stringData)

            myList = (result['signature_request']['signatures'])

            print(myList)
            print("\n")
            print(result)

            print("************46 - Non-embedded signature request passing Client ID END**********************")
        elif menu_item is "47":

            print("*************47 - Get a temporary URL from a signature ID  START**********************")

            response = client.get_embedded_object('a6cdca86b37cae60e3e32dab6a7a8b5c')
            print(response)

            print("************47 - Get a temporary URL from a signature ID END**********************")
        elif menu_item is "48":

            print("*************48 - Signer Reassignment non embedded START**********************")

            buildTheRequest = 'https://' + apikey + \
                              ':@api.hellosign.com/v3/signature_request/send'

            # r = requests.post('http://httpbin.org/post', data={'key': 'value'})

            data = {
                'client_id': clientID,
                'file_url': 'https://i.ytimg.com/vi/JPA_rzHDy6o/maxresdefault.jpg',
                'subject': 'test',
                'allow_decline': '1',
                'allow_reassign': 1,
                'message': 'test',
                'signers[0][name]': 'George',
                'signers[0][email_address]': fletch_email,
                'test_mode': '1'
                }

            print(buildTheRequest)

            r = requests.post(buildTheRequest, data)
            print(r.text)
            stringData = r.text
            # print(type(stringData))

            result = json.loads(stringData)

            myList = (result['signature_request']['signatures'])

            print(myList)
            print("\n")
            print(result)

            print("************48 Signer Reassignment non embedded  END**********************")

        elif menu_item is "49":
            print("****************************************************X - START**********************")

            buildTheRequest = 'https://' + apikey + \
                              ':@api.hellosign.com/v3/signature_request/create_embedded'

            # r = requests.post('http://httpbin.org/post', data={'key': 'value'})

            data = {
                'client_id': clientID,
                'file_url': 'https://i.ytimg.com/vi/JPA_rzHDy6o/maxresdefault.jpg',
                'subject': 'test',
                'allow_decline': '1',
                'allow_reassign': 1,
                'message': 'test',
                'signers[0][name]': 'George',
                'signers[0][email_address]': fletch2_email,
                'test_mode': '1'
                }

            print(buildTheRequest)

            r = requests.post(buildTheRequest, data)
            print(r.text)
            stringData = r.text
            # print(type(stringData))

            result = json.loads(stringData)

            myList = (result['signature_request']['signatures'])

            myInnerDict = myList[0]
            sigIDtemp = 0

            for key, value in myInnerDict.iteritems():
                # print(key, value)
                if 'signature_id' in key:
                    sigIDtemp = value
            print(sigIDtemp)
            print("\n")
            # print(result)

            # PART TWO
            # embedded/sign_url/78caf2a1d01cd39cea2bc1cbb340dac3

            buildTheRequest = 'https://' + apikey + \
                              ':@api.hellosign.com/v3/embedded/sign_url/' + sigIDtemp

            r = requests.get(buildTheRequest)
            print(r.text)
            stringData = r.text
            # print(type(stringData))

            result = json.loads(stringData)
            print(result)

            myList = (result['embedded']['sign_url'])

            print(myList)

            print("****************************************************X - END**********************")

        elif menu_item is "50":

            print("***************50 getTemplate **********************")
            # sample for testing cab3aad3f35b529b5af0bc07d77888aa0d3f4bde
            templateInput = input("Enter the template id that you want to report regarding")

            response = client.get_template(templateInput)

            print(response)
            print(exploreTemplateResponseObject(response))

            print("***************50 getTemplate - END**********************")
            print("A change")
        elif menu_item is 55:

            print("***************55 - Retrieving the oAuth Token  **********************")

            try:

                response = client.get_oauth_data(
                    client_id=clientID,
                    client_secret=secret,
                    code='f6896b4eccdc8670',
                    state='f94b2bb8'
                    )

            except Exception as e:
                print('Failed ' + str(e))
                print(response)

            # print(response)

            print("***************55  - Retrieving the oAuth Token **********************")
        elif menu_item is "56":

            print("***************56 verify an existing account **********************")
            response = client.verify_account(fletch_email)
            print(type(response))
            print(response)

            response = client.verify_account('gargabge@helalkjsdf.com')
            print(response)
            print("***************56 verify an existing account - END**********************")

        elif menu_item is "57":

            print("***************57 Create an account  **********************")

            response = client.create_account(
                email_address=fletch2_email,
                client_id=clientID,
                client_secret=secret
                )

            print(response)

            print("***************50 Create an account - END**********************")
        elif menu_item is "58":

            print("***************58 token refresh **********************")

            print("***************50 token refresh END**********************")

        elif menu_item is "59":

            print("***************59 - signer group BEGIN **********************")

            buildTheRequest = 'https://' + apikey + ':@api.hellosign.com/v3/signature_request/send_with_template'

            # r = requests.post('http://httpbin.org/post', data={'key': 'value'})

            data = {
                'client_id': clientID,
                'template_id': 'cab3aad3f35b529b5af0bc07d77888aa0d3f4bde',
                'subject': 'ticket',
                'allow_decline': '1',
                'message': 'ticket214090',
                'signers[Signer1][name]': 'George',
                'signers[Signer1][email_address]': fletch2_email,
                'custom_fields': '[{"name":"name", "value":"a", "editor":"Signer1", "required":"True"]',
                'test_mode': '1'
                }
            print(buildTheRequest)

            r = requests.post(buildTheRequest, data)
            print(r.text)
            stringData = r.text
            print(type(stringData))
            print("***************59 - signer group END**********************")
        elif menu_item is "60":

            print("***************60 Requests Send embedded with custom fields on text tags  **********************")

            buildTheRequest = 'https://' + apikey + ':@api.hellosign.com/v3/signature_request/create_embedded'

            # r = requests.post('http://httpbin.org/post', data={'key': 'value'})

            data = {
                'client_id': clientID,
                'subject': 'ticket',
                'allow_decline': '1',
                'message': 'BUGREP-2874',
                'signers[0][name]': 'Anne Lister',
                'signers[0][email_address]': fletch2_email,
                'signers[1][name]': 'Ann Walker',
                'signers[1][email_address]': fletch2_email,
                # 'custom_fields': '[{"name":"name", "value":"a", "editor":"Signer1", "required":"True"]',
                'test_mode': '1'
                }
            print(buildTheRequest)

            files = {'upload_file': open('NDA.pdf', 'rb')}

            r = requests.post(buildTheRequest, files, data)

            print(r.text)
            stringData = r.text
            print(type(stringData))

            print("***************60 Send embedded with custom fields on text tags - END**********************")
            print("A change")


        elif re.match(patternToMatch, menu_item):

            # pre claim url processing 3e1d6218d7e977b0af7bdcd01f48a0aa97322586
            # post claim url processing 6bfec0c3f6ff77c9aa749aec72a51e3bd956c69c
            # response = client.get_signature_request('3e1d6218d7e977b0af7bdcd01f48a0aa97322586')
            # print(response)
            # exploreSignatureRequestResponseObject(response)

            # c8f2b9018c11a90c2b9035b20ca09f35db97040c with three signers

            try:
                response = client.get_signature_request(menu_item)

                for x in response.signatures:
                    print(x.signature_id)
                    print(" = x.signature_id")
                    sign_url = client.get_embedded_object(x.signature_id)
                    print(sign_url)
                    print(x.signer_email_address)
                    print("\n")

            except:
                print("Did you claim the URL for this signature request?")


        elif menu_item is "111":
            continue


if __name__ == "__main__":
    runmain()
