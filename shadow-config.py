import requests
import json
import sys
import io
import sys, getopt
from pprint import pprint

#disable Certificat warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


def save_config ( archive,path ):
    archivename = path+archive['deviceName']+"_"+archive['createdAt']

    for conf2 in archive ['files']['file']:
        try:
#            print('archive=',archivename,'  config=',conf2)
            fileState=conf2['fileState']
            filename = archivename+"_"+fileState+".cfg"


            if fileState in ('STARTUPCONFIG', 'RUNNINGCONFIG'):
                print(".......saving ",fileState," of device", archive['deviceName']," in ",filename)
                fichier = open(filename,"w")
                fichier.write(conf2['data'])
                fichier.close()
        except:
            pass

    return();


def main(argv):
   server=""
   username=""
   password=""
   try:
      opts, args = getopt.getopt(argv,"hs:u:p:",)
   except getopt.GetoptError:
      print ('shadow-config.py -s server_address  -u username -p password')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('shadow-config.py -s server_address  -u username -p password')
         sys.exit()
      elif opt == "-s" :
         server = arg
      elif opt == "-u" :
         username = arg
      elif opt == "-p" :
         password = arg

   if server == "":
      server = input(  " Enter PI server IP Address : ")
   if username == "":
      username = input(" Enter API user username    : ")
   if password == "":
      password = input(" Enter API user password    :")


   PATH=""


   myheaders = {'Content-type': 'application/json'}
   status = requests.get('https://%s:%s@%s/webacs/api/v1/data/BulkSanitizedConfigArchives.json' %(username,password, server), verify=False, headers= myheaders)
   if  status.status_code != 200 :
        print("Problem with API BulSanitizedConfig , code ", status.status_code)
        exit(-1)
   status.encoding
   jresp = status.json()

   for entity in jresp['queryResponse']['entityId']:
        url = str(entity['@url'])+".json"

        status=requests.get(url,verify=False,auth=(username,password))
        if  status.status_code != 200 :
            print("Problem getting device config throug API , code ", status.status_code)
            exit(-1)
        else:
            status.encoding
            jresp = status.json()
            for entity2 in jresp['queryResponse']['entity']:
                save_config ( entity2['bulkSanitizedConfigArchivesDTO'],PATH)

   exit(0)




if __name__ == "__main__":
    main(sys.argv[1:])



