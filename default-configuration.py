# ! COPY THIS FILE AS configuration.py !
# --------------------------------------------------------------------------- #
# Configuration for WebShoot script
# --------------------------------------------------------------------------- #
#
# Path to vmrun binary
# By default: 
# - on Mac OS X: /Applications/VMware\ Fusion.app/Contents/Library/vmrun
# - on Linux: /usr/bin/vmrun
VMRUN="/usr/bin/vmrun"
# Configuration specific to ESXi
ESXI_HOST=None # format 'https://<hostName or IPaddr>/sdk'
ESXI_USER=None
ESXI_PASS=None
ESXI_TYPE="esx" # set to 'esx' for direct host or 'vc' for vSphere

# Path to virtual machine to use (give path to .vmx file)
VMPATH="/media/vmware/Victim Windows 10/Victim Windows 10.vmx"

# User  and password on VM (MANDATORY)
GUEST_USER="user"
GUEST_PASS="password"

# Interface used by the VM to communicate.
# tcpdump and mitmdump will be bound to this interface to intercept 
# communication
REC_IF="vmnet8"

# Path to tcpdump
TCPDUMP="/usr/sbin/tcpdump"

# Path to mitmdump
PROXYCMD="./tools/proxy/mitmproxy/mitmdump"

# Port and IP on which mitmdump will listen
# (typically the IP assigned to interface defnined in REC_IF)
PROXYHOST = "192.168.148.1"
PROXYPORT = "8080"

# Internal proxy to use.  If Internet access require to pass
# through a proxy, configuration will be defined here with the format
# http://[<proxy user>]:[<proxy port]@[proxy host]:[proxy port]
# ! proxy autentication IS NOT TESTED !
PROXYFWD = "http://192.168.148.1:8888"

# URL inside the vm to push url to browse.
# Default settings and parameters are
# http://<vm ip>:8080/browse/%s
VMURL="http://192.168.148.141:8080/browse/%s"

# VM snaphost to restore.  This snaphsot should be such that
# - vm is running
# - payload script is running and listening on VMURL
REFSNAPHSOT="webshoot"

# Path to tcpflow binary
TCPFLOW="/usr/bin/tcpflow"

# Google Safe Browsing API (required to validate url agaist GSB)
# if (not recommended), a different proxy is required for upstream
# connections to secure website like Google Safe Browsing, set
# GSPROXY to a proxy address with format:
# http://[<proxy user>]:[<proxy port]@[proxy host]:[proxy port]
# 
# To disable Google Safe Browsing, set GSBAPI to None
GSBAPI = None
SSLPROXY = None # ! not recommended !

# VirusTotal API key (required to validate url against VT)
# to disable VirusTotal set VTAPI to None
# SSLPROXY variable will be used to communicate to outside if 
# defined
VTAPI = None
