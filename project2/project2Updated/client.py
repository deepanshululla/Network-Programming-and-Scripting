

import re
import socket
import string
import sys


class ClientError(Exception):
    def __str__(self):
        return repr(self.value)


class ServerError(Exception):
    def __str__(self):
        return repr(self.value)


class RedirectError(Exception):
    def __str__(self):
        return repr(self.value)


class UnKnowError(Exception):
    def __str__(self):
        return repr(self.value)


class Client():
    """
    The Client class.
    """

    def __init__(self, usr, pwd):
        """
        Initial the class
        """
        self.host = 'fring.ccs.neu.edu'  # host name
        self.urls = ['/fakebook/']  # store unvisited urls
        self.visited = []  # store visited urls
        self.flag = []  # store secret flags
        self.csrftoken = ''  # cookie's csrftoken
        self.sessionid = ''  # cookie's sessionid
        self.usr = usr  # user name
        self.pwd = pwd  # password
        # Connect to remote server
        self.sock = socket.create_connection((self.host, 80))

    def handle_request(self, request):
        """
        Send request to the server and receive response. Return the response
        """
        try:
            self.sock.sendall(request)
            print request
        except socket.error:
            # Send failed
            sys.exit('Send failed')
			
        reply = self.sock.recv(4096)
        if not reply:
            print("no data recieved")
        print reply
        return reply

    def login(self):
        """
        Login to the fakebook and get cookie.
        """
        print "in login mode"
        # initial request to access fakebook
        request = 'GET /accounts/login/?next=/fakebook/ HTTP/1.1\r\nHost: %s\r\n\r\n' % self.host

        reply = self.handle_request(request)
        #print '[DEBUG]Initial Request\'s reply\n%s' % reply

        # Use regular expression to get the cookie's value
        csrf_pattern = re.compile(r'csrftoken=([a-z0-9]+);')
        session_pattern = re.compile(r'sessionid=([a-z0-9]+);')
        # get cookie
        try:
            self.csrftoken = csrf_pattern.findall(reply)[0]
            self.sessionid = session_pattern.findall(reply)[0]
        except IndexError:
            # server's reponse is abnormal, cannot get the cookie value
            # print '[DEBUG]Cannot parse1:\n%s' % reply
            sys.exit('Cannot parse HTML due to receive incomplete message.')
        # print '[DEBUG]csrf: %s\tsession: %s' % (self.csrftoken, self.sessionid)

        # Post request to server, send username and password to login fakebook
        postdata = 'csrfmiddlewaretoken=%s&username=%s&password=%s&next=' % (self.csrftoken, self.usr, self.pwd)
        request = 'POST /accounts/login/ HTTP/1.1\r\nHost: %s\r\nConnection: keep-alive\r\nContent-Length: %d' \
                  '\r\nContent-Type: application/x-www-form-urlencoded\r\nCookie: csrftoken=%s; sessionid=%s' \
                  '\r\n\r\n%s' % (self.host, len(postdata), self.csrftoken, self.sessionid, postdata)
        #print'[DEBUG]Post Request:\n%s' % request

        reply = self.handle_request(request)
        #print '[DEBUG]POST Request\'s reply\n%s' % reply
        try:
            self.sessionid = session_pattern.findall(reply)[0]
        except IndexError:
            # print '[DEBUG]Cannot parse2:\n%s' % reply
            # print '[DEBUG]csrf:%s\tsession:%s' % (self.csrftoken, self.sessionid)
            sys.exit('Cannot parse HTML due to receive incomplete message.')


    def open_url(self, url):
        """
        Open the given url and return the reponse from the server
        """

        def get_status(page):
            """
            Parse the HTTP response header and get HTTP status code
            """
            index = string.find(page, ' ') + 1
            status = page[index: index + 3]
            # if status == '' or status == '500' or status == '301':
            #     print '[DEBUG]Abnormal Status Page:%s\n%s' % (status, page)
            return status

        request = 'GET %s HTTP/1.1\r\nHost: %s\r\nConnection: keep-alive\r\nCookie: csrftoken=%s; ' \
                  'sessionid=%s\r\n\r\n' % (url, self.host, self.csrftoken, self.sessionid)
        page = self.handle_request(request)
        self.visited.append(url)  # this url is visited
        status = get_status(page)
        if status == '403' or status == '404':
            raise ClientError('403 or 404 Error')
        elif status == '301':  # redirect to a new url
            raise RedirectError('301 Error')
        elif status == '500':  # Internal Server Error
            raise ServerError('500 Error')
        elif status == '':
            raise UnKnowError('Unknown Error')
        return page

    def find_url(self, page):
        """
        Use regular expression to find urls in html page
        """
        pattern = re.compile(r'<a href=\"(/fakebook/[a-z0-9/]+)\">')
        links = pattern.findall(page)
        # Find a new url(have not been visited or found), then add it to urls
        self.urls.extend(filter(lambda l: l not in self.urls and l not in self.visited, links))

    def find_secret_flag(self, page):
        """
        Use regular expression to find secret flag in html page
        """
        pattern = re.compile(r"<h2 class='secret_flag' style=")
        flag = pattern.findall(page)
        
            
        # print 'Page\n%s' % page
        if flag:
            self.flag.extend(flag)
			
    def findBtw(self,s,start_char,end_char):
        start = s.find(start_char)
        end= s.find(end_char, start)
        fl=s[start:end]
        return fl
		
    def get_new_url(self, page):
        """
        Parse the HTTP response header and get new url
        """
        pattern = re.compile(r'Location=http://cs5700\.ccs\.neu\.edu(/fakebook/[a-z0-9/]+)')
        new_url = pattern.findall(page)[0]
        return new_url

    def run(self):
        """
        Use breadth first search to crawl fakebook
        """
        print "Program in run mode"
        page = ''
        while self.urls and len(self.flag) < 5:
            # if there are unvisited urls or less than 5 flags, continue the loop
            link = self.urls.pop(0)
            #print '[DEBUG]Open link:%s' % link
            try:
                page = self.open_url(link)
                #print '[DEBUG]Page:\n%s' % page
                self.find_url(page)
                self.find_secret_flag(page)
            except ClientError:
                self.visited.append(link)  # abandon the URL
            except RedirectError:
                self.urls.insert(0, self.get_new_url(page))
            except ServerError:
                self.sock = socket.create_connection((self.host, 80))
                self.visited.pop()
                self.urls.insert(0, link)
            except UnKnowError:
                self.sock = socket.create_connection((self.host, 80))
                self.visited.pop()
                self.urls.insert(0, link)

        print '[DEBUG]Visited:%d' % len(self.visited)
        print self.visited
        print '[DEBUG]URLS:%d' % len(self.urls)
        print self.urls
        print '[DEBUG]secret_flag:'
        f=open('secret.txt','w')
        for flag in self.flag:
           print flag
           f.write(flag)
        f.close()
		# print self.flag
        self.sock.close()


def main():
    c = Client('001798574', 'CQA2F4BJ')
    # c = Client('001944902', 'AF50YTLA')
    # if (len(sys.argv) != 3):
        # sys.exit('Illegal Arguments.')
    #c = Client(sys.argv[1], sys.argv[2])
    c.login()
    c.run()


if __name__ == '__main__':
    main()
