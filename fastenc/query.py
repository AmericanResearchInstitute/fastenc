"""
Helper methods for constructing valid encoding.com queries

"""
from xml.etree.ElementTree import Element, SubElement

def create_query(userid, userkey, action, mediaid=None, source=None,
                            notify=None, format_list=None):
    '''
    This pretty abstract, and should let you make any kind of request
    supported by encoding.com's api, but it doesn't do any enforcement
    for you. Plan ahead or be ready for encoding.com error responses.
    '''

    e_query = Element("query")

    SubElement(e_query, "userid").text = str(userid)
    SubElement(e_query, "userkey").text = userkey
    SubElement(e_query, "action").text = action

    if mediaid:
        SubElement(e_query, "mediaid").text = mediaid

    if source:
        SubElement(e_query, "source").text = source

    if notify:
        SubElement(e_query, "notify").text = notify

    # Output format specification required for AddMedia and UpdateMedia actions
    if format_list:
        for entry in format_list:
            e_query.append(entry)

    return e_query

# The list of of possible arguments is HUGE, but only "output" is required
def create_format_element(output, logo=None, **kwargs):
    e_format = Element("format")

    if logo:
        e_format.append(logo)

    SubElement(e_format, "output").text = output

    for key, value in kwargs.iteritems():
        SubElement(e_format, key).text = value

    return e_format

def create_logo_element(url, x, y, mode, threshold):
    e_logo = Element("logo")

    SubElement(e_logo, "logo_source").text = url
    SubElement(e_logo, "logo_x").text = x
    SubElement(e_logo, "logo_y").text = y
    SubElement(e_logo, "logo_mode").text = mode
    SubElement(e_logo, "logo_threshold").text = threshold

    return e_logo
