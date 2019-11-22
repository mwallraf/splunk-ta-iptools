# splunk-ta-iptools
Splunk add-on which includes various IP manipulation tools

## Description
This is a Splunk add-on that exposes some commands to transform IP addresses:

### ip2int
Convert IPv4 addresses to integer

### int2ip
Convert integer into IPv4 addresses

## Installation
You can install directly from GIT or download the archive and install via Splunk

### Install source via GIT
To install from GIT do the following:

```
  cd $SPLUNK_HOME/etc/apps
  git clone https://github.com/mwallraf/splunk-ta-iptools TA-iptools
  restart splunk
```

### Install via Splunk
Download as archive and install as a standard Splunk app
