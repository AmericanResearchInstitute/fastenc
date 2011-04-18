"""
Encoding.com actions in python class form.

See http://encoding.com/api for information regarding usage

"""

from xml.etree.ElementTree import tostring
from connection import Connection
import query

# Helper classes to ensure proper generation of encoding.com queries

class ActionAlreadySentError(Exception):
    '''Exception to be raised if an action is sent more than once.'''
    pass

# Base Class for Actions
class _ActionBase(object):
    '''Base class for all encoding.com actions

    This class should provide most functionality for all encoding.com actions,
    making liberal use of positional and keyword arguments. The order of those
    arguments is defined by the encoding.com docs themselves.

    Argument identifiers have been modified to abide by PEP-08 standards.

    See http://www.encoding.com/api for more information.
    '''
    def __init__(self, userid, userkey, *args, **kwargs):
        '''Base init method of encoding.com actions

        :param userid: Your encoding.com numeric userid
        :param userkey: Your encoding.com API key
        '''
        self.userid = str(userid)
        self.userkey = userkey
        self.action = self.__class__.__name__

        self.already_sent = False

        self._generate_query(*args, **kwargs)

    def _generate_query(self, *args, **kwargs):
        '''Private method to generate a query object based on given arguments'''
        self.query = query.create_query(self.userid, self.userkey, self.action, *args, **kwargs)

    def tostring(self):
        '''Returns the string representation of the encoding.com query

        :returns: str, raw XML of an encoding.com query
        '''
        return tostring(self.query)

    def send(self, secure=True):
        '''Sends the generated query off to encoding.com, returning the result

        :param secure: Use encoding.com's HTTPS service if true
        :type secure: bool
        :returns: xml.etree.ElementTree.Element, the XML result from encoding.com
        :raises: ActionAlrestSentError
        '''
        if self.already_sent:
            raise ActionAlreadySentError()
        else:
            c = Connection(secure)
            result = c.request(self.query)
            self.alredy_sent = True
            return result

#########################
# Media-related actions #
#########################
class AddMedia(_ActionBase):
    def __init__(self, userid, userkey, source, notify=None, format_list=None):
        '''add new media to user's media list, creates new items in a queue according to formats specified in XML

        :param source: URL that encoding.com will use to locate the media to be transcoded
        :param notify: URL that encoding.com will use as the destination of transcode notifications (optional)
        :param format_list: A list containing ElementTree elements create using
            the :func:`fastenc.query.create_format_element` method
        '''
        super(AddMedia, self).__init__(userid, userkey, source=source, notify=notify, format_list=format_list)

class AddMediaBenchmark(_ActionBase):
    def __init__(self, userid, userkey, source, notify=None, format_list=None):
        '''add new media to user's media list and set a flag for NOT processing it after downloading

        :param source: URL that encoding.com will use to locate the media to be transcoded
        :param notify: URL that encoding.com will use as the destination of transcode notifications (optional)
        :param format_list: A list containing ElementTree elements create using
            the :func:`fastenc.query.create_format_element` method (optional)
        '''
        super(AddMediaBenchmark, self).__init__(userid, userkey, source=source, notify=notify, format_list=format_list)

class UpdateMedia(_ActionBase):
    def __init__(self, userid, userkey, mediaid, format_list):
        '''replace information about existing media's formats

        :param mediaid: A unique identifier for the media being updated
        :param format_list: A list containing ElementTree elements create using
            the :func:`fastenc.query.create_format_element` method
        '''
        super(UpdateMedia, self).__init__(userid, userkey, mediaid, format_list=format_list)

class ProcessMedia(_ActionBase):
    def __init__(self, userid, userkey, mediaid):
        '''start encoding of previously downloaded media (one that added with AddMediaBenchmark action)

        :param mediaid: A unique identifier for the media to be processed
        '''
        super(ProcessMedia, self).__init__(userid, userkey, mediaid)

class CancelMedia(_ActionBase):
    def __init__(self, userid, userkey, mediaid):
        '''delete specified media and all its items in queue

        :param mediaid: A unique identifier for the media to be processed
        '''
        super(CancelMedia, self).__init__(userid, userkey, mediaid)

class GetMediaList(_ActionBase):
    def __init__(self, userid, userkey):
        '''return list of user's media'''
        super(GetMediaList, self).__init__(userid, userkey)

class GetStatus(_ActionBase):
    def __init__(self, userid, userkey, mediaid):
        '''return information about selected user's media and all its items in queue

        :param mediaid: A unique identifier (or list of unique identifiers) of media to query
        '''
        # Mediaid can be one ID string, or many separated by commas for the GetStatus action
        # To make it more 'pythonic', we take one id or some collection of them
        if isinstance(mediaid, basestring):
            super(GetStatus, self).__init__(userid, userkey, mediaid)
        else:
            # Gotta map everything to a string type in case they're all
            # ints or something, lest we get a TypeError from str.join()
            mediaid_csv = ','.join(map(unicode, mediaid))
            super(GetStatus, self).__init__(userid, userkey, mediaid_csv)

class GetMediaInfo(_ActionBase):
    def __init__(self, userid, userkey, mediaid):
        '''returns some video parameters of the specified media, if available

        :param mediaid: A unique identifier of media to query
        '''
        super(GetMediaInfo, self).__init__(userid, userkey, mediaid)

###########################
# SubUser-related actions #
###########################
class AddTrialUser(_ActionBase):
    '''Not yet implemented.'''
    def __init__(self, userid, userkey):
        raise NotImplementedError

class UpdateSubUser(_ActionBase):
    '''Not yet implemented.'''
    def __init__(self, userid, userkey):
        raise NotImplementedError

class DeleteSubUser(_ActionBase):
    '''Not yet implemented.'''
    def __init__(self, userid, userkey):
        raise NotImplementedError

class GetUserInfo(_ActionBase):
    '''Not yet implemented.'''
    def __init__(self, userid, userkey):
        raise NotImplementedError

class GetSubUsers(_ActionBase):
    '''Not yet implemented.'''
    def __init__(self, userid, userkey):
        raise NotImplementedError

class GetASM(_ActionBase):
    '''Not yet implemented.'''
    def __init__(self, userid, userkey):
        raise NotImplementedError

class GetStorageSpace(_ActionBase):
    '''Not yet implemented.'''
    def __init__(self, userid, userkey):
        raise NotImplementedError

class GetBandwidthStat(_ActionBase):
    '''Not yet implemented.'''
    def __init__(self, userid, userkey):
        raise NotImplementedError

class GetBandwidthStatGroupDate(_ActionBase):
    '''Not yet implemented.'''
    def __init__(self, userid, userkey):
        raise NotImplementedError
