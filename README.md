# WebShoot
Framework for analysis of suspicious website

! UNDER DEVELOPMENT !

## Features

* Launch a VM and open a website with multiple browsers.
* For each browser, do a screenshot of the loaded webpage.
* Take a PCAP of the full browsing session
* Pass all requests through a proxy (currently Burp)
* Automate the full process

## Installation

### Host preparation
1. Install mitmproxy: <tt>$ sudo apt-get install mitmproxy</tt>
2. Check that <tt>tcpdump</tt> is installed

### VM preparation

1. Install operating system of choice (dev/test on Windows 10)
1. Install Python 2.7
1. <tt>pip install selenium</tt>
1. Install Firefox
1. Install Selenium drivers for Internet Explorer and Firefox
1. Set a password for user (required to run remotely script)
1. Enable auto-logon of user
1. Copy <tt>payload-rest.py</tt> to <tt>C:\Scripts\</tt> and run the script
1. While the script is still RUNNING, take a snapshot named<tt>webshot</tt>

## Usage

<pre>
sudo python ./webshot.py -u "http://www.autopsit.org"
</pre>

## Output

In ./cases, you fill have the following structure:
* A sub-directory with the FQDN
 * A sub directory per run of the script
  * A capture of all the traffic passing through proxy: <tt>proxy_traffic.txt</tt>
   * A logfile of the proxy output (MITMPROXY format): <tt>proxy.log</tt>
   * A full tcpdump capture: <tt>capture.pcap</tt>
   * A zip file with screenshots of the website for each browser selected in <tt>payload-rest.py</tt>


## Others (cheat sheet)

Note for Proxy users, to use PIP, set proxy with the following command
<pre>
	set HTTP_PROXY=http://[username]:[password]@[proxy address]:[port]
</pre>

