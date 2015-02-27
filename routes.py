############ START CHANGE FROM LOCAL DEVELOPMENT TO HOSTED SITE ##############
SERVER_URL_BASE = "http://snapdev.cs.vt.edu/snapdev"
# LOCAL_URL_BASE = "http://127.0.0.1:5000"


SITE_URL_BASE = SERVER_URL_BASE
# SITE_URL_BASE = LOCAL_URL_BASE

############ END CHANGE FROM LOCAL DEVELOPMENT TO HOSTED SITE ##############



from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request


from datetime import datetime


import sys
HEADER = {'User-Agent': 'CORGIS Weather library for educational purposes'}
PYTHON_3 = sys.version_info >= (3, 0)

if PYTHON_3:
    # from urllib.error import HTTPError
    import urllib.request as request
    # from urllib.parse import quote_plus
else:
    # from urllib2 import HTTPError
    import urllib2
    # from urllib import quote_plus



app = Flask(__name__)






# For caching.
@app.after_request
def add_header(response):
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response








def _get(urlString):
    """
    Internal method to convert a URL into it's response (a *str*).

    :param str urlString: the url to request a response from
    :returns: the *str* response
    """
    if PYTHON_3:
        req = request.Request(urlString, headers=HEADER)
        response = request.urlopen(req)
        return response.read().decode('utf-8')
    else:
        req = urllib2.Request(urlString, headers=HEADER)
        response = urllib2.urlopen(req)
        return response.read()




#(End) helper methods.






@app.route('/')
def index():
    return render_template('hello.html', SITE_URL_BASE=SITE_URL_BASE)

@app.route('/hello')
def learn():
    return render_template('hello2.html', SITE_URL_BASE=SITE_URL_BASE)



@app.route('/urlRequestForClient')
def urlRequestForClient():
    #Get the request parameters.
    urlString = str(request.args.get('urlString'))
    app.logger.debug(urlString)

    #newURLString = "https://" + urlString
    newURLString = "http://" + urlString

    rawResponseValue = _get(newURLString)

    responseValue = removeUnwantedCharacters(rawResponseValue)

    #Form the response.
    urlReport = {'responseValue': responseValue}

    #Return the results.
    return jsonify(urlReport=urlReport)


# Helper Methods
def removeUnwantedCharacters(rawResponseValue):
    responseValue = ""
    firstCurly = rawResponseValue.find("{")
    firstBracket = rawResponseValue.find("[")

    if (firstCurly < firstBracket):
        responseValue = rawResponseValue[firstCurly:]
    else:
        responseValue = rawResponseValue[firstBracket:]
    return responseValue




if __name__ == '__main__':
    app.debug = True
    app.run()
