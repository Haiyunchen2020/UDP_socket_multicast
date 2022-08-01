#run receiver before sender

import socket
import sys

def help_and_exit(prog):
    print('Usage: ' + prog \
        + ' host_ip mcast_group_ip mcast_port_num file_to_send',
        file=sys.stderr)
    sys.exit(1)


#read the file.
def read_file(filename):
    buf = None
    with open(filename, 'rb') as f:
        buf = f.read()
    return buf

def mc_send_file(hostip, mcgrpip, mcport, filename):
    # creates a UDP socket
    sender = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, \
            proto=socket.IPPROTO_UDP, fileno=None)

    # Defines a multicast end point
    mcgrp = (mcgrpip, mcport)

    # Set up IP_MULTICAST_TTL
    sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    # Set up transmitting NIC for multicast datagrams
    sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, \
            socket.inet_aton(hostip))
    bindaddr=(mcgrpip,mcport)
    sender.bind (bindaddr)

#There are 2 arguments for sender.sendto,
#first one is the things you need to send out,
#second one is the destination of the things.
   # Transmit the filename in a datagram
    sender.sendto(filename.encode(),mcgrp)
    #sender.send(f"{filename}{file.size}".encode())
    
    # Read the file and transmit the file content in a datagram
    data=read_file (filename)
    sender.sendto (data,mcgrp)

    while True:
        if (sender.sendto(data,mcgrp)):
            print('sending')
        break

    sender.close()
    
    print('Completed')

def mc_send_msg(hostip, mcgrpip, mcport, msgbuf):
    # This creates a UDP socket
    sender = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, \
            proto=socket.IPPROTO_UDP, fileno=None)
    # This defines a multicast end point, that is a pair
    #   (multicast group ip address, send-to port nubmer)
    mcgrp = (mcgrpip, mcport)

    # This defines how many hops a multicast datagram can travel. 
    # The IP_MULTICAST_TTL's default value is 1 unless we set it otherwise. 
    sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    # This defines to which network interface (NIC) is responsible for
    # transmitting the multicast datagram; otherwise, the socket 
    # uses the default interface (ifindex = 1 if loopback is 0)
    # If we wish to transmit the datagram to multiple NICs, we
    # ought to create a socket for each NIC. 
    sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, \
           socket.inet_aton(hostip))

    # Transmit the datagram in the buffer
    sender.sendto(msgbuf, mcgrp)

    # release the socket resources
    sender.close()


def main(argv):
    if len(argv) < 5:
        help_and_exit(argv[0])

    hostipaddr = argv[1]
    mcgrpipaddr = argv[2]
    mcport = int(argv[3])
    filename = argv[4]

    mc_send_file(hostipaddr, mcgrpipaddr, mcport, filename)

if __name__=='__main__':
    main(sys.argv)
