import BaseHTTPServer, SimpleHTTPServer
import ssl
import getopt
import sys


def print_use():
    print "Python HTTPS server.     ./simple_ssl -p port"

def main(argv):

    port = ''

    opts, args = getopt.getopt(argv,"p:",["port="])

    for opt, arg in opts:
        if opt == '-p' :
            port = arg

    if port == '':
        print_use()
        sys.exit()



    httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', int(port)),
            SimpleHTTPServer.SimpleHTTPRequestHandler)

    httpd.socket = ssl.wrap_socket (httpd.socket,
            keyfile="/tmp/key.pem",
            certfile='/tmp/cert.pem', server_side=True)

    print "Server is running on port %s" % (port)

    httpd.serve_forever()
if __name__ == "__main__":
    main(sys.argv[1:])

