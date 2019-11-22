##
## Splunk Streaming command (SCPv2) that will change an integer
## into an IPv4 address. 
##


import os,sys
import socket, struct

splunkhome = os.environ['SPLUNK_HOME']
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators



@Configuration()
class int2ipCommand(StreamingCommand):
    """ Converts integer to IPv4 address

    ##Syntax

    .. code-block::
        int2ip fields="<integer_field>[,<integer_field>]*" [destfield=<new_field>]

    ##Parameters:
    fields = Comma seperated list of fields containing integers

    destfield = *optional* If provided then the result of the command
                will be stored in this new *destfield*.
                Only 1 destination field can be provided so if the fields
                parameter contains a list then the destfield will be a
                overwritten with the last result!
 
                If destfield is not provided then a new field will be
                created as <field_ip>

    ##Description

    Splunk Streaming command (SCPv2) that will change an integer
    into an IPv4 address. Very often IP addresses are stored in
    integer format in databases.

    ##Example

    Convert a single field containing an integer into an IPv4 address. The result
    will be stored in a new field called ipint_ip

    .. code-block::
        | makeresults
        | eval ipint="3232235786" 
        | int2ip fields=ipint

    Convert a single field containing an IPv4 address into an integer. The result
    will be stored in a new field called ip_as_int

    .. code-block::
        | makeresults
        | eval ipint="3232235786" 
        | int2ip fields=ipint destfield=int_as_ip

    """

    destfield = Option(
        doc='''
        **Syntax:** **destfield=***<fieldname>*
        **Description:** Name of the field that will be created''',
        require=False, validate=validators.Fieldname())

    @Option()
    def fields(self):
        """ **Syntax:** logging_configuration=<path>
        **Description:** Loads an alternative logging configuration file for a command invocation. The logging
        configuration file must be in Python ConfigParser-format. The *<path>* name and all path names specified in
        configuration are relative to the app root directory.
        """
        return self._fields.split(",")

    @fields.setter
    def fields(self, value):
        if value is not None:
            self._fields = value

    def __init__(self, *args, **kwargs):
        super(StreamingCommand, self).__init__(*args, **kwargs)
        self._fields = None


    def stream(self, records):
        self.logger.debug('int2ipCommand: %s', self)  # logs command line

        for record in records:
            for fld in self.fields:
                if fld in record:
                    destfield = self.destfield if self.destfield else "{}_ip".format(fld)
                    try:
                        record[destfield] = self.int2ip(record[fld])
                    except:
                        self.logger.error("unable to convert '{}' to an IP address".format(record[fld]))
                        record[destfield] = "conversion error"
                else:
                    self.logger.warning("field '{}' is not found".format(fld))

            yield record


    def int2ip(self, addr):
        return socket.inet_ntoa(struct.pack("!I", int(addr)))

dispatch(int2ipCommand, sys.argv, sys.stdin, sys.stdout, __name__)

