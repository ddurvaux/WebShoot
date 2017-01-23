#!/usr/bin/python2 -O
#  -*- coding:utf-8 -*-

"""
    Set of scripts to open a website in multiple browser and retrieve data

    IDEA/TODO
       - multiple browser support
       - start/stop network capture
       - start/stop OS monitoring (process, registry changes...)

    Version: 0.0 - dev / poc Version

    Copyright: Autopsit (N-Labs sprl) 2017
"""
# Import configuration
import configuration

# Packages required
import os
import re
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


  def __init__( self, vmrun, vmpath ):
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


  def take_snapshot(self):
      self.__call_vmrun__("snapshot", "webshot snapshot")
      return


  def revert_snapshot(self):
      self.__call_vmrun__("revertToSnapshot", "webshot snapshot")
      return


  def delete_snapshot(self):
      self.__call_vmrun__("deleteSnapshot", "webshot snapshot")
      return


  def upload_prerequities(self):
      self.__call_vmrun__("directoryExistsInGuest", "C:\\Scripts\\")
      return


  def __call_vmrun__(self, cmd, *options):
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
      process = subprocess.Popen(fullcmd)
      # !! FIX THIS !!
      #output = process.stdout.read()
      #print("== DEBUG : %s ==" % output)
    except Exception as e:
      print("FATAL ERROR, VM command: %s" % fullcmd)
      print(e)
    return output


# --------------------------------------------------------------------------- #
def recordPCAP(workdir="./"):
  """
     Launch tcpdump to regard traffic passing through VM interface
  """
  tcpdump = subprocess.Popen([configuration.TCPDUMP, "-i", configuration.REC_IF, "-w", "%s/capture.pcap" % workdir])
  return tcpdump


def startMitmProxy(workdir="./"):
  """
    Launch MITMProxy to record all the requests done by the website
  """
  proxy = subprocess.Popen([configuration.PROXY])
  return proxy


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
    myvm.take_snapshot()     
    myvm.start_vm()
    myvm.upload_prerequities()

    workdir=createDirectories(results.url)
    # Recording Thread - w/ tcpdump
    tcpdump = recordPCAP(workdir)
    
    # Start proxy and record traffic
    #proxy = startMitmProxy(workdir)

    # Browse website in VM
    # -- TODO --

    # Stop recording
    tcpdump.terminate()
    #proxy.terminate()

    # Restore state of VM and cleanup
    myvm.stop_vm()
    myvm.revert_snapshot()
    return


"""
   Call main function
"""
if __name__ == "__main__":
    
    # Create an instance of the Analysis class (called "base") and run main 
    main()

# That's all folks ;)