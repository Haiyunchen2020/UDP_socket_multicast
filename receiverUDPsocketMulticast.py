#put print(...) to check that part of code,
#if it print out,it's good. if didn't print out,that part of code has problem.
#run receiver before sender.

import sys
import socket
import struct

bufsize=1024

def help_and_exit(prog):
    print('Usage: ' + prog + ' from_nic_by_host_ip mcast_group_ip mcast_port')
    sys.exit(1)

#There are 2 arguments here, when you use it, you need put 2 arguments too!
#write means to write content of the file.
#write a file=open a file with the filename, as f,f.write(buf)
def write_file(filename, buf):
    with open(filename, 'wb') as f:
        f.write(buf)

def mc_recv_file(fromnicip, mcgrpip, mcport):

    # 1. Creates a UDP socket
    receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, \
            proto=socket.IPPROTO_UDP, fileno=None)

    # 2. Defines a multicast end point
    bindaddr = (mcgrpip, mcport)
    receiver.bind (bindaddr)

    # 3. Joins the socket to the intended multicast group. 
    if fromnicip == '0.0.0.0':
        mreq = struct.pack("=4sl", socket.inet_aton(mcgrpip), socket.INADDR_ANY)
    else:
        mreq = struct.pack("=4s4s", \
            socket.inet_aton(mcgrpip), socket.inet_aton(fromnicip))
    receiver.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # receiver regards the datagram received first time as filename.
    # 4. Receive the filename
    buf,senderaddr = receiver.recvfrom(1024)
    filename=buf.decode()

    # receiver regards the datagram received second time as file content.
    # 5. Receive file content of the file and write it to file
    buf,senderaddr = receiver.recvfrom(1024)
    data = buf
    print ("got it",data)
#There are 2 arguments for write_file here, cannot only have 1 argument.
    write_file (filename,data)

    # 6. Release resources
    receiver.close()
    print('Completed')

def mc_recv_msg(fromnicip, mcgrpip, mcport):
    bufsize = 1024

    # This creates a UDP socket
    receiver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, \
            proto=socket.IPPROTO_UDP, fileno=None)

    # This configure the socket to receive datagrams sent to this multicast
    # end point, i.e., the pair of 
    #   (multicast group ip address, mulcast port number)
    # that must match that of the sender
    bindaddr = (mcgrpip, mcport)
    receiver.bind(bindaddr)

    # This joins the socket to the intended multicast group. The implications
    # are two. It specifies the intended multicast group identified by the
    # multicast IP address.  This also specifies from which network interface
    # (NIC) the socket receives the datagrams for the intended multicast group.
    # It is important to note that socket.INADDR_ANY means the default network
    # interface in the system (ifindex = 1 if loopback interface present). To
    # receive multicast datagrams from multiple NICs, we ought to create a
    # socket for each NIC. Also note that we identify a NIC by its assigned IP
    # address. 
    if fromnicip == '0.0.0.0':
        mreq = struct.pack("=4sl", socket.inet_aton(mcgrpip), socket.INADDR_ANY)
    else:
        mreq = struct.pack("=4s4s", \
            socket.inet_aton(mcgrpip), socket.inet_aton(fromnicip))
    receiver.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Receive the mssage
    buf, senderaddr = receiver.recvfrom(1024)
    msg = buf.decode()

    return msg

def main(argv):
    if len(argv) < 4:
        help_and_exit(argv[0])

    fromnicip = argv[1] 
    mcgrpip = argv[2]
    mcport = int(argv[3])


    mc_recv_file(fromnicip, mcgrpip, mcport)
    
if __name__=='__main__':
    main(sys.argv)
