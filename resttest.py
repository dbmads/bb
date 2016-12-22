from json import dumps
from dateutil import parser
keys =['1mh2LeYfMLK/iAxtKai8lu', 'SuXizFpb4UkxGQBThfT2LO', 'V5RgcXhy9.eM25mtAvo3Me']
from operator import itemgetter
import requests
import time
from requests import Session
from random import randint
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def extract( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

CODE_TO_STATE = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AS': 'American Samoa',
    'AZ': 'Arizona', 'AR': 'Arkansas', 'AA': 'Armed Forces Americas',
    'AE': 'Armed Forces Middle East', 'AP': 'Armed Forces Pacific',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut',
    'DE': 'Delaware', 'DC': 'District of Columbia',
    'FM': 'Federated States of Micronesia', 'FL': 'Florida',
    'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MH': 'Marshall Islands',
    'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
    'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska',
    'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
    'MP': 'Northern Mariana Islands', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon',
    'PW': 'Palau', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island',
    'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
    'UT': 'Utah', 'VT': 'Vermont', 'VI': 'Virgin Islands', 'VA': 'Virginia',
    'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
}
USPS_BASE_URL = 'https://tools.usps.com/go/ZipLookupResultsAction!input.action'
def usps_request(**kwargs):
	# construct get parameters string
	params = {
		'resultMode': 0,
		'companyName': '',
		'address1': kwargs.get('street_address', ''),
		'address2': '',
		'city': kwargs.get('city', ''),
		'state': kwargs.get('state',''),
		'urbanCode': '',
		'postalCode': '',
		'zip': kwargs.get('zip5', '')
	}

	# make request. need to spoof headers or get infinite redirect
	return requests.get(USPS_BASE_URL, params=params, verify=False,
						headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'},
						timeout=5)


def usps_address_lookup(**kwargs):
    address = None
    soup = BeautifulSoup(usps_request(**kwargs).text)

    # get container div for results
    results_content = soup.find(id='results-content')

    # build return dict
    address = {
        'street_address': '',
        'city': '',
        'state': '',
        'zip5': '',
        'zip4': ''
    }

    try:
        address['street_address'] = str(results_content.find('span', class_='address1').text).strip()
    except:
        print "Can't find street address"
        address.pop('street_address')
    try:
        address['city'] = str(results_content.find('span', class_='city').text).strip().title()
    except:
        print "Can't find city"
        address.pop('city')
    try:
        address['state'] = str(results_content.find('span', class_='state').text).strip()
    except:
        print "Can't find state"
        address.pop('state')
    try:
        address['zip5'] = str(results_content.find('span', class_='zip').text).strip()
    except:
        print "Can't find zip5"
        address.pop('zip5')

    return address


def usps_zip_lookup(street_address, city, state, z5=''):

    address = usps_address_lookup(street_address=street_address, city=city, state=state, zip5=z5)
    if 'zip5' not in address:
        address['zip5'] = raw_input("Please Enter Zip Code")
        address['zip4'] = ''
    if 'state' not in address:
        address['state'] = raw_input("Please Enter State")
    if 'city' not in address:
        address['city'] = raw_input("Please Enter City")
    if 'street_address' not in address:
        address['street_address'] = raw_input("Please Enter Street Address")
    return address

def gen_card(firstname,lastname,street_address,zipcode,city,state,country='US',password='Deskjet123$$$$'):
    empid = randint(5555,55141231231)
    empid = str(empid)

    if country=='US':
        zipcode = str(zipcode)
        address = usps_zip_lookup(street_address,z5 = zipcode,state=state,city=city)
        zipcode = str(address['zip5'])+address['zip4']
        if address['street_address'] != street_address:
            street_address = address['street_address']

        if address['city'] != city:
                city = address['city']


        if address['state'] != state:
            if 'state' in address:
                state = address['state']
                state = state.upper()

    URL = "https://w6.iconnectdata.com/Login/login"
    SEC_PAGE = "https://w6.iconnectdata.com/Login/securityAnswer"
    AUTH_PAGE  = "https://w6.iconnectdata.com/Login/auth"
    ADD_CARD_PAGE = "https://w6.iconnectdata.com/Login/quickLinkForward?wrap=Y&url=https://w6.iconnectdata.com%2Fblam%2FController%3FXFunction%3DCardAddPrelim%26fromNewIcd%3DY"
    PRE_CARD_PAGE = "https://w6.iconnectdata.com/Login/leftNav?LVL1=manage&LVL2=cards"
    POST_CARD_PAGE = "https://w6.iconnectdata.com/blam/Controller"
    question1 = "What street did you live on when you were 10 years old?"
    question2 = "What was your high school mascot?"
    postdata = {}
    postdata['username'] = "dr357ah"

    headers = {
        "Referer":"https://w6.iconnectdata.com/Login/logout",
        "User-Agent":"User-Agent:Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
        }
    postdata2={'machineSignature':'machineSignature:director=false&flashVersion=&mimeTypesCount=0&pluginsCount=0&quickTime=false&realPlayer=false&windowsMediaPlayer=false&accrobatReader=false&svgViewer=false&clearType=false&screenColorDepth=24&screenHeight=640&screenPixelDepth=24&screenWidth=360&screenAvailHeigth=640&screenAvailWidth=360&screenBufferDepth=undefined&appName=Netscape&appVersion=5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30&appMinorVersion=undefined&cookieEnabled=true&cpuClass=undefined&systemLanguage=undefined&userAgent=Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30&userLanguage=undefined&javaEnabled=false&platform=MacIntel&appCodeName=Mozilla&language=en-US&oscpu=undefined&vendor=Google Inc.&vendorSub=&product=Gecko&productSub=20030107'}
    postdata2['password']=password
    postdata3 = {}
    postdata3['machineSignature']='machineSignature:director=false&flashVersion=&mimeTypesCount=0&pluginsCount=0&quickTime=false&realPlayer=false&windowsMediaPlayer=false&accrobatReader=false&svgViewer=false&clearType=false&screenColorDepth=24&screenHeight=640&screenPixelDepth=24&screenWidth=360&screenAvailHeigth=640&screenAvailWidth=360&screenBufferDepth=undefined&appName=Netscape&appVersion=5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30&appMinorVersion=undefined&cookieEnabled=true&cpuClass=undefined&systemLanguage=undefined&userAgent=Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30&userLanguage=undefined&javaEnabled=false&platform=MacIntel&appCodeName=Mozilla&language=en-US&oscpu=undefined&vendor=Google Inc.&vendorSub=&product=Gecko&productSub=20030107'
    session = Session()
    session.cookies['ICDMode']="WRAPPED"
    session.cookies['icdBrand']="CSI"
    session.cookies['jsAndCookieEnabled']="True"
    resp = session.get(url=URL,headers = headers)
    resp2 = session.post(url=URL, data = postdata,headers = headers)
    resp2 = session.post(url=AUTH_PAGE, data = postdata2,headers = headers)
    html = resp2.text
    if question1 in html:
        postdata3['answer']="winchester"
        postdata3['questionId']="51"

    elif question2 in html:
        postdata3['answer']="panther"
        postdata3['questionId']="44"

    else:
        pass
        #postdata['']

    resp3 = session.post(url=SEC_PAGE, data = postdata3,headers = headers)
    #print resp3.text
    #https://github.com/jaapbakker88/deeplinking
    resp4 = session.get(url=ADD_CARD_PAGE,headers = headers)
    #print resp4.text
    state = state.upper()
    city  = city.upper()
    firstname = firstname.upper()
    lastname = lastname.upper()
    postdatacc = {'XFunction':'CardAddDriver',
                  'expeditedFeeExempted':'N',
                  'cardUseCompanyStandards':'Y',
                  'cardCompanyStandardID':'001',
                  'cardCardStatusIn':'Y',
                  'cardNumberofCards':'0',
                  'cardNumberofCardsInput':'0',
                  'custCustomerName':'DREAM BIG MEDIA',
                  'cardDriversLicenseState': state,
                  'custCorporateCountry': country,
                  'cardHolderCCEmailAddr': '',
                  'cardAddressCountry':'', 'custZip': zipcode,
                  'cardAddressCity': city, 'cardAddressZip':  zipcode,
                  'cardHolderMobile':'',
                  'cardAddressState':state,
                  'custCorporateName': 'CSI ENTERPRISES, INC.',
                  'cardUnitNumber': '', 'custAccountCountry': country,
                  'cardLastName': lastname, 'custAccountCity':city,
                  'custCorporateAddress2': '3301 BONITA BEACH RD SUITE 300',
                  'custCorporateAddress1': 'DO NOT SHIP CARDS HERE',
                  'cardHolderUsageDelTypeDefault': 'N', 'cardEmployeeNumber': str(empid),
                  'custAccountAddress1': street_address, 'custAccountAddress2': '',
                  'cardHolderEmailAddr': '', 'cardAddressShipToName': firstname+" "+lastname,
                  'custAccountZip': zipcode, 'custAddress1':street_address, 'custAddress2': '',
                  'custCorporateZip': '34134', 'custCity': city, 'custCorporateCity': 'BONITA SPRINGS',
                  'cardFirstName': firstname, 'custCorporateState': 'FL', 'custAccountState': state,
                  'cardHolderUsageDelTypeOverride': 'N', 'cardCardStatus': 'A', 'custCountry': 'US',
                  'cardDriversLicenseNumber': '', 'custState': state, 'custAccountName': firstname+ ' '+lastname,
                  'cardAddressState': state, 'cardAddressLine1': street_address, 'cardAddressLine2': '',
                  'cardAddressAttention':firstname+ " "+lastname,'cardAddressShipToName': firstname+ " "+lastname,
                  'cardCardExpirationDate':'0718'}

    #resppre = session


    resp5 = session.post(POST_CARD_PAGE,postdatacc,headers = headers)
    htmlparse = resp5.text
    empid =extract(htmlparse,'cardEmployeeNumberTmp" TYPE="hidden" VALUE="','">')
    cardid=extract(htmlparse,'cardCardNumber" type="hidden" value="','">')
    cardnumber= extract(htmlparse,'ID="txtCardNum">','</TD>')
    expdate= extract(htmlparse,'ID="txtCardExprDate">','</TD>')

    post_data ={"XFunction":"CardEditInput",
    "cardEmployeeNumberTmp":empid,
    "cardEmployeeNumber":empid,
    "cardId":cardid,
    "cardCardNumber":cardid,
    }
    resp6 = session.post(POST_CARD_PAGE,post_data,headers = headers)

    soup = BeautifulSoup(resp6.text)
    hidden_tags = soup.find_all("input", type="hidden")
    post_dict_cvv = {}
    for tag in hidden_tags:
        if tag.value==None:
            tag.value=""
        post_dict_cvv[tag['name']]=tag['value']
    post_dict_cvv['XFunction']= 'CardEditCVC2'
    resp6 = session.post(POST_CARD_PAGE,post_dict_cvv,headers = headers)
    cvv_html = extract(resp6.text,'CVC2:</TD>','</TR>')
    cvv = extract(cvv_html,'<TD class="data">',"</TD>")
    cc_dict = {}
    cc_dict['cvv'] = cvv
    cc_dict['cc'] = cardnumber
    cc_dict['expyear']="18"
    cc_dict['expmonth']='07'
    cc_dict['name'] = firstname + ' '+lastname
    cc_dict['street_addresss'] = street_address
    cc_dict['city'] = city
    cc_dict['state'] = state
    cc_dict['country'] = country
    return cc_dict




name = raw_input("First Name : ")
lname = raw_input("Last Name : ")
stadd = raw_input("Street Address : ")
cityy = raw_input("City Name : ")
STATE = raw_input("State : ")
zipcode = raw_input("Zipcode : ")
#
card = gen_card(firstname=name,lastname=lname,street_address=stadd,city=cityy,state=STATE,zipcode=zipcode)
print card['cc'] +' '+ card['expmonth']+ ' '+ card['expyear']+ ' '+card['cvv']
print card['name']
print card['street_addresss']
print card['city'] + " , " +card['state']+ " , " + card['country']


cityy = raw_input("\n")




