#!/usr/bin/python

"""

"""

from subprocess import Popen, PIPE
import requests
import os, sys
import optparse

def add_comment(user, passwd, url, issuenum, _data):
    auth = requests.auth.HTTPBasicAuth(user, passwd)
    data = """
    {
        "body": "%s",
        "visibility": {
            "type": "role",
            "value": "Administrators"
        }
    }
    """ % repr(_data)

    header = {"Content-Type":"application/json"}
    try:
        res = requests.post(url + "/rest/api/latest/issue/" + issuenum + "/comment", data=data, auth=auth, headers=header)
    except requests.exceptions.ConnectionError:
        res.status_code = "Connection refused"
        print("connection refused")
        help()
        sys.exit(0)
    except requests.URLRequired:
        print("invalid url...")
        help()
        sys.exit(0)

    if res.status_code == 200:
        return True

    return False

def run_command(user, passwd, url):
    commandline = "python ./getjiraissues.py -d %s -i %s -p %s" % (url, user, passwd)
    p = Popen(commandline, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    return stdout

def help():
    print ("")
    print ("  you should run with 4 arguments")
    print ("  1. url with '-d' option")
    print ("  2. userID with '-i' option")
    print ("  3. password with '-p' option")
    print ("  4. issue number with '-n' option")
    print ("")

def main():
    url = "http://"
    parser = optparse.OptionParser()
    parser.add_option('-i', '--id', action='store', dest='id', help="enter user id")
    parser.add_option('-p', '--password', action='store', dest='password', help="enter password")
    parser.add_option('-d', '--dest', action='store', dest='dest', help="enter url")
    parser.add_option('-n', '--num', action='store', dest='num', help="enter issue number")
    (options, args) = parser.parse_args(sys.argv)

    if (options.dest == None or options.id == None or options.password == None or options.num == None):
        help()
        sys.exit(0)

    if (options.dest).find("http://") != 0:
        url = url + options.dest + "/jira"

    issues = run_command(options.id, options.password, options.dest)
    add_comment(options.id, options.password, url, options.num, issues)

    return True

if __name__ == '__main__':
    main()