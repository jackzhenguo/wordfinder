'''
  ref: https://dev.to/zduey/how-to-set-up-an-ssh-server-on-a-home-computer
'''

sudo apt-get upgrade || update

sudo apt-get install openssh-client
sudo apt-get install openssh-server

ps -A | grep sshd

% output
% [number] ?  00:00:00 sshd

ssh localhost

'''
  Determine IP address of host machine
'''

ifconfig
ifconfig | grep "inet addr"

'''
  use returned IP address from command on line 22
  in place of X.X.X.X
'''
ssh username@X.X.X.X
