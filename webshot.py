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
import configuration
import argparse
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
      output = process.stdout.read()
      print("== DEBUG : %s ==" % output)
    except Exception as e:
      print("FATAL ERROR, VM command: =%s=" % fullcmd)
      print(e)
    return output

# --------------------------------------------------------------------------- #
tcpdump = None # pointer to tcpdump process
proxy = None   # pointer to proxy process

def recordPCAP():
  """
     Launch tcpdump to regard traffic passing through VM interface
  """
  global tcpdump
  tcpdump = subprocess.Popen([configuration.TCPDUMP, "-i", configuration.REC_IF, "-w", "capture.pcap"])
  return


# --------------------------------------------------------------------------- #
"""
    Main function
"""
def main():
    global tcpdump
    global proxy

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', action='store', dest='url', help='URL to browse', required=True)
    results = parser.parse_args()


    # Kick-off the analysis
    myvm =  VMWare(configuration.VMRUN, configuration.VMPATH)
    myvm.take_snapshot()
    myvm.start_vm()
    myvm.upload_prerequities()

    # Recording Thread - w/ tcpdump
    pcapThread = Thread(target=recordPCAP, args = [])
    pcapThread.start()

    # Start proxy and record traffic
    # -- TODO --

    # Browse website in VM
    # -- TODO --

    # Stop recording
    tcpdump.terminate()

    # Restore state of VM and cleanup
    #myvm.stop_vm()
    #myvm.revert_snapshot()
    return

"""
   Call main function
"""
if __name__ == "__main__":
    
    # Create an instance of the Analysis class (called "base") and run main 
    main()

# That's all folks ;)