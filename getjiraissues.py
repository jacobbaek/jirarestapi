#!/usr/bin/python
"""
jira get all issues
"""

import sys, optparse
import requests
import json

def help():
    print ("")
    print ("")
    print ("  you should run with 3 arguments")
    print ("  1. url with '-u' option")
    print ("  2. userID with '-i' option")
    print ("  3. password with '-p' option")
    print ("")

# "test_project_mgmt" 
def get_issues(url, auth, projectname):
    idslst = {}
    # return requests.get(URL + "/rest/api/latest/issue/TESTMGMT-1", auth=auth)
    # return requests.get(URL + "/rest/api/latest/project", auth=auth)
    res = requests.get(url + "/rest/api/2/search?jql=project=" + projectname + "&fields=id,key", auth=auth)
    jsondict = json.loads(res.text)

    for idnum in jsondict['issues']:
        idslst[idnum['id']] = idnum['key']
    return idslst

def get_projects(url, auth):
    prjlst = []
    res = requests.get(url + "/rest/api/2/project", auth=auth)
    jsondict = json.loads(res.text)

    for project in jsondict:
        prjlst.append(project['name'])
    return prjlst

def main():
    g_url = ""

    parser = optparse.OptionParser()
    parser.add_option('-i', '--id', action='store', dest='id', help="enter user id")
    parser.add_option('-p', '--password', action='store', dest='password', help="enter password")
    parser.add_option('-d', '--dest', action='store', dest='dest', help="enter url")
    (options, args) = parser.parse_args(sys.argv)

    if options.dest != None:
        g_url = "http://" + options.dest

    if (options.dest == None or options.id == None or options.password == None):
        help()
        return

    auth = requests.auth.HTTPBasicAuth(options.id, options.password)
    prjlst = get_projects(g_url, auth) 
    for prjname in prjlst:
        print("[PROJECT_NAME] " + prjname)
        issues = get_issues(g_url, auth, prjname)
        for k, v in issues.items():
            print("  ID %s / KEY %s" % (k,v))

if __name__ == '__main__':
    main()
