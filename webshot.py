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


"""
    VMWare Workstation driving
"""
class VMWare:
  vmrun = ""
  vmpath = ""

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

  def __call_vmrun__(self, cmd, *options):
    try:
      subprocess.call([self.vmrun, cmd, self.vmpath] + list(options))
    except Exception as e:
      print("FATAL ERROR, VM command %s failed" % cmd)
      print(e)
    return

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
    # -- DO THINKS --
    #        xxx
    # -- EVERYTHING IS DONE --
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