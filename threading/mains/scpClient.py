import os
import paramiko

class ScpClient() :
  def __init__(self):
    self.ssh = paramiko.SSHClient()

  def connect(self):
    privatekeyfile = os.path.expanduser('~/.ssh/id_rsa')
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    self.ssh.connect('192.168.27.187', username='lestertay', pkey=mykey)

  def send(self):
    with closing(Write(self.ssh.get_transport(), '.')) as scp:
      scp.send_file('file.txt', True)
      scp.send_file('../../test.log', remote_filename='baz.log')

      s = StringIO('this is a test')
      scp.send(s, 'test', '0601', len(s.getvalue()))
  
for root, dirs, files in os.walk("/home/pi/images/"):
    for filename in files:
        print(filename)