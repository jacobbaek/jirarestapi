#!/usr/bin/python
"""
jira get all issues
"""

import sys, optparse
import requests
import json

def help():
    print ("")
    print ("  you should run with 3 arguments")
    print ("  1. url with '-d' option")
    print ("  2. userID with '-i' option")
    print ("  3. password with '-p' option")
    print ("")

# "test_project_mgmt" 
def get_issues(url, auth, projectname):
    idslst = {}
    # return requests.get(URL + "/rest/api/latest/issue/TESTMGMT-1", auth=auth)
    # return requests.get(URL + "/rest/api/latest/project", auth=auth)
    res = requests.get(url + "/rest/api/2/search?jql=project=" + projectname + "&fields=id,key,summary", auth=auth)

    jsondict = json.loads(res.text)

    for idnum in jsondict['issues']:
        idslst[idnum['id']] = idnum['key']
        # idslst[idnum['key']] = idnum['fields']['summary']
    return idslst

def get_projects(url, auth):
    prjlst = []
    try:
        res = requests.get(url + "/rest/api/latest/project", auth=auth)
    except requests.exceptions.ConnectionError:
        print("connection refused")
        help()
        return None
    except requests.URLRequired:
        print("invalid url...")
        help()
        return None
    print(res.status_code)

    jsondict = json.loads(res.text)

    for project in jsondict:
        prjlst.append(project['name'])
    return prjlst

def main():
    url = "http://"

    parser = optparse.OptionParser()
    parser.add_option('-i', '--id', action='store', dest='id', help="enter user id")
    parser.add_option('-p', '--password', action='store', dest='password', help="enter password")
    parser.add_option('-d', '--dest', action='store', dest='dest', help="enter url")
    (options, args) = parser.parse_args(sys.argv)

    if (options.dest == None or options.id == None or options.password == None):
        help()
        return False

    if (options.dest).find("http://") != 0:
        url = url + options.dest + "/jira"

    auth = requests.auth.HTTPBasicAuth(options.id, options.password)
    prjlst = get_projects(url, auth) 
    if prjlst == None:
        return False

    for prjname in prjlst:
        print("[PROJECT_NAME] " + prjname)
        issues = get_issues(url, auth, prjname)
        for k, v in issues.items():
            print("  ID: %s / KEY: %s" % (k,v))
            # print("  KEY: %s / SUMMARY: %s" % (k,v))

    return True

if __name__ == '__main__':
    main()