#!/usr/bin/python2 -O
#  -*- coding:utf-8 -*-

"""
    Set of scripts to open a website in multiple browser and retrieve data

    IDEA/TODO
       - multiple browser support
       - extract network artifact
       - search VT + Google Safe Browsing
       - extract JS and run JSBeautifuler
       - browse list of websites
       - do diff between sessions
       - ...

    Version: 0.1 - Beta Version

    Copyright: Autopsit (N-Labs sprl) 2017
"""
# Import configuration
import configuration

# Packages required
import os
import re
import base64
import requests
import argparse
import datetime
import subprocess
from threading import Thread


"""
    VMWare Workstation driving
"""
class VMWare:
  vmrun = ""
  vmpath = ""
  vmuser = None
  vmpass = None
  scpath = "C:\Scripts"
  payload = "payload-rest.py"
  wrapper = "payload.bat"
  debug = False

  def __init__( self, vmrun, vmpath):
      self.vmrun  = vmrun
      self.vmpath = vmpath


  def start_vm(self):
      """
        Start the virtual machine
      """
      self.__call_vmrun__("start")
      return


  def stop_vm(self):
      self.__call_vmrun__("stop")
      return


  def take_snapshot(self, snapshot="webshoot"):
      self.__call_vmrun__("snapshot", snapshot)
      return


  def revert_snapshot(self, snapshot="webshoot"):
      self.__call_vmrun__("revertToSnapshot", snapshot)
      return


  def delete_snapshot(self):
      self.__call_vmrun__("deleteSnapshot", "webshot snapshot")
      return

  def upload_prerequities(self):
      # Check if script directory exists
      output = self.__call_vmrun__("directoryExistsInGuest", "C:\\Scripts\\")
      if "does not exist" in output:
        self.__call_vmrun__("createDirectoryInGuest", self.scpath)

      # Check if files exists in guest and upload if not
      files = [ self.payload, self.wrapper ]
      for f in files:
        output = self.__call_vmrun__("fileExistsInGuest", "%s\\%s" % (self.scpath, f))
        if "does not exist" in output:
          if self.debug:
            print "File: %s does not exist, uploading to %s." % (f, self.scpath)
          self.__call_vmrun__("copyFileFromHostToGuest", f, "%s\\%s" % (self.scpath, f))
      return


  def run_payload(self):
    self.__call_vmrun__("runProgramInGuest", "-noWait", "-activeWindow", "%s\\%s" % (self.scpath, self.wrapper))
    return


  def retrieve_results(self, workdir="./"):
    self.__call_vmrun__("copyFileFromGuestToHost", "%s\\%s" % (self.scpath, "results.zip"), "%s/%s" % (workdir, "results.zip"))
    return

  def enableDebug():
    """
      Turn on debugging
    """
    self.debug = True
    return


  def __call_vmrun__(self, cmd, *options):
    """
      Execute vmrun command with options
      and retrieve stdout output
    """
    output = None
    fullcmd = []
    try:
      fullcmd.append(self.vmrun)

      # handle guest host auth
      if(configuration.GUEST_USER is not None and configuration.GUEST_USER != ""):
        fullcmd.append("-gu")
        fullcmd.append(configuration.GUEST_USER)
        fullcmd.append("-gp")
        fullcmd.append(configuration.GUEST_PASS)

      # add action on vm
      fullcmd.append(cmd)

      # add path to vm
      fullcmd.append(self.vmpath)

      # handle options
      fullcmd = fullcmd + list(options)      

      # call process and retrieve output
      process = subprocess.Popen(fullcmd, stdout=subprocess.PIPE)
      output = process.stdout.read()
      process.wait() # wait process to complete
      if self.debug:
        print("VMRUN command: %s" % fullcmd)
        print("VMRUN Result: %s" % output)
    except Exception as e:
      print("FATAL ERROR, VM command: %s" % fullcmd)
      print(e)
    return output


# --------------------------------------------------------------------------- #
def recordPCAP(workdir="./"):
  """
     Launch tcpdump to regard traffic passing through VM interface
  """
  tcpdump = None
  try:
    tcpdump = subprocess.Popen([configuration.TCPDUMP, "-i", configuration.REC_IF, "-w", "%s/capture.pcap" % workdir])
  except:
    print("ERROR: no tcpdump capture for this run")
  return tcpdump


def startMitmProxy(workdir="./", proxylog=None):
  """
    Launch MITMProxy to record all the requests done by the website
  """
  proxy = None
  try:
    proxycmd = [configuration.PROXYCMD, "-b", configuration.PROXYHOST, "-p", configuration.PROXYPORT, "-w", "%s/%s" % (workdir, "proxy_traffic.txt"), "--anticache", "--anticomp", "--insecure"]
    if configuration.PROXYFWD is not None:
      proxycmd.append("-U")
      proxycmd.append(configuration.PROXYFWD)
    proxy = subprocess.Popen(proxycmd, stdout=proxylog)
  except Exception as e:
    print("ERROR: no proxy for this run")
    print(e)
  return proxy


def queryBrowsing(url, vmurl="http://localhost:8080/browse/%s"):
  """
    Query the python script running on guest to browse url
  """
  urlb64 = base64.b64encode(url)
  response = requests.get(vmurl % urlb64)
  return

def createDirectories(url):
  """
    Create a working directory to store snapshots, PCAP and proxy logs
  """
  try:
    # strip of http or https and keep the fqdn
    m = re.search("(http://|https://)?([\w+\.]+)/?(.*)", url)
    url = m.group(2)
    date = datetime.datetime.today().strftime('%Y%m%d%H%M%S')

    # create directory
    dirname = "./cases/%s/%s" % (url, date)
    try:
      os.makedirs(dirname)
    except Exception as e:
      print("ERROR, failed to create directories: %s" % dirname)
      print(e)
    return dirname
  except:
    print("FATAL ERROR: impossible to create case directory for %s" % url)    
  return None
# --------------------------------------------------------------------------- #


"""
    Main function
"""
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', action='store', dest='url', help='URL to browse', required=True)
    results = parser.parse_args()

    # Kick-off the analysis
    myvm =  VMWare(configuration.VMRUN, configuration.VMPATH)
    myvm.revert_snapshot(configuration.REFSNAPHSOT) # start from clean state
    myvm.start_vm() # in case VM is paused

    workdir=createDirectories(results.url)

    # Recording Thread - w/ tcpdump
    tcpdump = recordPCAP(workdir)
    
    # Start proxy and record traffic
    proxylog = open("%s/%s" % (workdir, "proxy.log"), "w")
    proxy = startMitmProxy(workdir, proxylog)

    # Browse website in VM
    queryBrowsing(results.url, configuration.VMURL)

    # Stop recording
    if tcpdump is not None:
      tcpdump.terminate()
    if proxy is not None:
      proxy.terminate()
      proxylog.flush()
      proxylog.close()

    # Restore state of VM and cleanup
    myvm.retrieve_results(workdir)
    myvm.revert_snapshot(configuration.REFSNAPHSOT) # restore clean state

    # All done :)
    return

"""
   Call main function
"""
if __name__ == "__main__":
    
    # Create an instance of the Analysis class (called "base") and run main 
    main()

# That's all folks ;)