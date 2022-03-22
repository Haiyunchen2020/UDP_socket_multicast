# UDP_socket_multicast

 This code is to use the multicast Python programs to send a small file to a selected few hosts.
 For these two programs to work properly, i.e., to send and receive a file, these two programs must 
 adhere to a protocol. The programs at present implements the following simple protocol:

1. The sender and receivers agree that the file must fit in a single UDP datagram (so, small files only).
2. The receivers begin to wait for incoming datagrams
3. The sender first sends the name of the file in a datagram
4. The sender then sends the content of the file in another datagram
5. The receivers treat the datagram received the first as the filename
6. The receivers treat the datagram received the second as the file content
7. The receivers write the content to the file named after the received filename
