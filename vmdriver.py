class CloudProvider():
  vmuser = None
  vmpass = None
  scpath = "C:\Scripts"
  payload = "payload-rest.py"
  wrapper = "payload.bat"
  debug = False

  def __init__(self):
    pass
     

  def start_vm(self):
    """
      Start the virtual machine
    """
    print("NOT IMPLEMENTED")
    return


  def stop_vm(self):
    print("NOT IMPLEMENTED")
    return


  def take_snapshot(self, snapshot="webshoot"):
    print("NOT IMPLEMENTED")
    return


  def revert_snapshot(self, snapshot="webshoot"):
    print("NOT IMPLEMENTED")
    return


  def delete_snapshot(self):
    print("NOT IMPLEMENTED")
    return


  def upload_prerequities(self):
    print("NOT IMPLEMENTED")
    return


  def run_payload(self):
    print("NOT IMPLEMENTED")
    return


  def retrieve_results(self, workdir="./"):
    print("NOT IMPLEMENTED")
    return


  def enableDebug():
    """
      Turn on debugging
    """
    self.debug = True
    return


class Azure(CloudProvider):

  def __init__(self):
    pass
     

  def start_vm(self):
    """
      Start the virtual machine
    """
    print("NOT IMPLEMENTED")
    return


  def stop_vm(self):
    print("NOT IMPLEMENTED")
    return


  def take_snapshot(self, snapshot="webshoot"):
    print("NOT IMPLEMENTED")
    return


  def revert_snapshot(self, snapshot="webshoot"):
    print("NOT IMPLEMENTED")
    return


  def delete_snapshot(self):
    print("NOT IMPLEMENTED")
    return


  def upload_prerequities(self):
    print("NOT IMPLEMENTED")
    return


  def run_payload(self):
    print("NOT IMPLEMENTED")
    return


  def retrieve_results(self, workdir="./"):
    print("NOT IMPLEMENTED")
    return


  def enableDebug():
    """
      Turn on debugging
    """
    self.debug = True
    return