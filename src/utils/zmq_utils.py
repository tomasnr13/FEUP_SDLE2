import zmq
import sys
timeout = 1000
nr_tries = 1


def send_msg(context, socket , receiver_ip, receiver_port, request_msg):
    retries_left = nr_tries
    request = str(request_msg).encode('utf-8')
    print("...")

    try:
        socket.send(request)

        while retries_left != 0:
            if (socket.poll(timeout) & zmq.POLLIN) != 0:
                reply = socket.recv()
                return reply.decode('utf-8')

            retries_left -= 1
            # print("No response from user")
            # Socket is confused. Close and remove it.
            socket.setsockopt(zmq.LINGER, 0)
            socket.close()
            if retries_left == 0:
                # print("User seems to be offline, abandoning")
                return -1

            print("Retrying to contact the user…")
            # Create new connection
            socket = context.socket(zmq.REQ)
            socket.connect(f'tcp://{receiver_ip}:{int(receiver_port)}')
            print("Resending (%s)", request)
            socket.send(request)
    except zmq.ZMQError:
        print('ZMQ error! Aborting...')
        sys.exit()
