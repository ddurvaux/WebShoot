VMRUN="/usr/bin/vmrun" # on Mac OS X: /Applications/VMware\ Fusion.app/Contents/Library/vmrun
VMPATH="/media/durvada/2e86542c-3270-4b22-919f-f1867a4615b6/vmware/Victim Windows 10/Victim Windows 10.vmx"
GUEST_USER="david"
GUEST_PASS="david"
REC_IF="vmnet8"
TCPDUMP="/usr/sbin/tcpdump"
PROXYCMD="./tools/proxy/mitmproxy/mitmdump"
PROXYHOST = "192.168.148.1"
PROXYPORT = "8080"
PROXYFWD = "http://192.168.148.1:8888"
VMURL="http://192.168.148.141:8080/browse/%s"