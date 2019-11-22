##
## Splunk Streaming command (SCPv2) that will change an IPv4 address
## into an integer value. 
##


import os,sys
import socket, struct

splunkhome = os.environ['SPLUNK_HOME']
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators



@Configuration()
class ip2intCommand(StreamingCommand):
    """ Converts IPv4 to integer

    ##Syntax

    .. code-block::
        ip2int fields="<ipv4_field>[,<ipv4_field>]*" [destfield=<new_field>]

    ##Parameters:
    fields = Comma seperated list of fields containing IPv4 addresses

    destfield = *optional* If provided then the result of the command
                will be stored in this new *destfield*.
                Only 1 destination field can be provided so if the fields
                parameter contains a list then the destfield will be a
                overwritten with the last result!
 
                If destfield is not provided then a new field will be
                created as <field_int>

    ##Description

    Splunk Streaming command (SCPv2) that will change an IPv4 address
    into an integer value. Very often IP addresses are stored in
    integer format in databases.

    ##Example

    Convert a single field containing an IPv4 address into an integer. The result
    will be stored in a new field called ipv4_int

    .. code-block::
        | makeresults
        | eval ipv4="192.168.1.10" 
        | ip2int fields=ipv4

    Convert a single field containing an IPv4 address into an integer. The result
    will be stored in a new field called ip_as_int

    .. code-block::
        | makeresults
        | eval ipv4="192.168.1.10" 
        | ip2int fields=ipv4 destfield=ip_as_int


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
        self.logger.debug('ip2intCommand: %s', self)

        for record in records:
            for fld in self.fields:
                if fld in record:
                    destfield = self.destfield if self.destfield else "{}_int".format(fld)
                    try:
                        record[destfield] = int(self.ip2int(record[fld]))
                    except:
                        self.logger.error("unable to convert IP '{}' to an integer".format(record[fld]))
                        record[destfield] = "conversion error"
                else:
                    self.logger.warning("field '{}' is not found".format(fld))

            yield record


    def ip2int(self, addr):
        return struct.unpack("!I", socket.inet_aton(str(addr)))[0]

dispatch(ip2intCommand, sys.argv, sys.stdin, sys.stdout, __name__)

