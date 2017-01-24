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


Note for Proxy users, to use PIP, set proxy with the following command
<pre>
	set HTTP_PROXY=http://<username>:<password>@<proxy address>:<port>
</pre>

