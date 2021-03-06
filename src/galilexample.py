import socket
import sys
from struct import *
import cmd

HOST = '10.30.1.2'
PORT = 9874

class GalilTools(cmd.Cmd):
    intro = 'Welcome to GalilTools. Type help or ? to list commands.\n'
    prompt = '(galiltools) '

    def preloop(self):
        self.host = HOST
        self.port = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)

    def do_connect(self, arg):
        'Connect to galilserver'
        try:
            self.sock.connect((self.host, self.port))
            self.receive()
        except Exception as err:
            print('Error! {}'.format(err))

    def do_show_all_lvdt_values(self, arg):
        'Return all LVDT values'
        try:
            self.sock.send('SHOWALLLVDTVALS\r\n'.encode())
            self.receive()
        except Exception as err:
            print('Error! {}'.format(err))

    def do_disconnect(self, arg):
        'Disconnects and closes open socket with galilserver'
        try:
            self.sock.send('CLIENTDONE\r\n'.encode())
            self.receive()
        except Exception as err:
            print('Error! {}'.format(err))

    def receive(self, size=1024):
        'Receive response from galilserver'
        message = self.sock.recv(size).decode()
        print(message)

    def do_exit(self, arg):
        'Closes socket, stops GalilTools, and exits.'
        print('Closing socket.')
        self.sock.close()
        print('Exiting GalilTools. Goodbye.')
        return True


def test():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((self.host, self.port))
    # returns "OK: Connected to galilserver. Client 1"
    message = sock.recv(1024).decode()
    prints(message)

    # request all LVDT values
    # returns "OK: 0.600 0.727 0.507" in order of LVDT A, B, then C
    sock.send('SHOWALLLVDTVALS\r\n'.encode())
    message = sock.recv(1024).decode()
    prints(message)

    # request actuator encoder values
    # requires sending a STATUS command
    sock.send('STATUS\r\n'.encode())
    message = sock.recv(1024)
    sock.close()

    # must remove the "OK: " of response
    message_slice = message[4:len(message)]
    # each actuator encoder value is at different byte locations
    # actuator A = 52
    # actuator B = 80
    # actuator C = 108
    # getting actuator A
    raw_actuator_encoder_a = message_slice[52:54]
    # must unpack the response
    # 'h' is for signed short integer
    # https://docs.python.org/3.8/library/struct.html
    actuator_encoder_a = unpack('h',
                                raw_actuator_encoder_a)[0]  # returns tuple
    prints('Actuator Encoder A'.format(actuator_encoder_a))
    return None


if __name__ == '__main__':
    GalilTools().cmdloop()
