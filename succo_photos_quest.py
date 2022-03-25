# https://github.com/ido-ran/google-photos-api-python-quickstart/blob/master/quickstart.py
# https://stackoverflow.com/questions/53328101/python-google-photos-api-list-items-in-album

# required imports
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from math import ceil
import time
import os 
import pickle

######################
# starting chronometer
tStart = time.time()
print("quest started!")

# settings
stepAlbumSize = 50  # nr. of albums per step in the loop on albums (<= 50)
stepMediaSize = 100  # nr. of media per step in the loop on media per album & global (<= 100)
#-# stepAddSize = 50  # nr. of no-album media that are uploaded to the temporary album at a time (<=50) [UNUSED]

filename1 = "output/photos_outAlbumList.txt"  # output filename -- list of albums
filename2 = "output/photos_outMediaNoAlbumList.txt"  # output filename -- list of media with no album

# setup the API w/ the authorisation & build service
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
creds = None
if(os.path.exists("tokens/photos/token.pickle")):
    with open("tokens/photos/token.pickle", "rb") as tokenFile:
        creds = pickle.load(tokenFile)
if not creds or not creds.valid:
    if (creds and creds.expired and creds.refresh_token):
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('keys/client_secret.json', SCOPES)
        creds = flow.run_local_server(port = 0)
    with open("tokens/photos/token.pickle", "wb") as tokenFile:
        pickle.dump(creds, tokenFile)
service = build('photoslibrary', 'v1', credentials = creds, static_discovery=False)

###########################################
## PART 1) get album-related information ##
###########################################
print("\nPART 1) get album-related information")

# these objects will contain all the album-related info
idsAlbum = []  # list of album ids 
titles = {}  # album titles as function of album id
nMedia = {}  # nr. of media per album as function of album id
albumUrls = {}  # album URLs as function of album id
mediaList = {}  # list of media ids per album as function of album id
mediaUrls = {}  # media URLs as function of media id per album as function of album id

print("entering loop on albums...")
iAlbumExit = False  # when this becomes True, the loop on groups of albums stops
iAlbumIter = 0
#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#
while not iAlbumExit:  # loop on groups of albums (with size stepAlbumSize)

    iAlbumIter += 1
    print("iteration over (<=%d) albums nr. %d" % (stepAlbumSize, iAlbumIter))
    resAlbumOuter = service.albums().list(  # album list query
        pageSize = stepAlbumSize,
        pageToken = None if iAlbumIter==1 else resAlbumOuter.get("nextPageToken"),
        fields = "nextPageToken,albums(id,title,mediaItemsCount,productUrl)"
    ).execute()
    
    titles0 = []
    idsAlbum0 = []
    nMedia0 = []
    albumUrls0 = []
    mediaList1 = {}
    mediaUrls1 = {}

    #1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#
    if (str(type(resAlbumOuter.get("albums")))!="<class 'NoneType'>"):
    
        for j in range(len(resAlbumOuter.get("albums"))):  # loop on albums within each iteration
        
            resAlbumOuter0 = resAlbumOuter.get("albums")[j]  # album list single entry
            
            if not (resAlbumOuter0["id"] in idsAlbum):
                print("album %d in iteration) %s (%d media)" % (
                    j+1, 
                    resAlbumOuter0["title"], 
                    int(resAlbumOuter0["mediaItemsCount"] if ("mediaItemsCount" in resAlbumOuter0.keys()) else 0
                )))

                idsAlbum0.append(resAlbumOuter0["id"])
                titles0.append(resAlbumOuter0["title"])
                albumUrls0.append(resAlbumOuter0["productUrl"])
                if ("mediaItemsCount" in resAlbumOuter0.keys()):
                    nMedia0.append(int(resAlbumOuter0["mediaItemsCount"]))

                    iMediaExit = False  # when this becomes True, the loop on groups of media per album stops
                    iMediaIter = 0
                    
                    #2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2
                    while not iMediaExit:  # loop on groups of media per album (with size stepMediaSize)
                    
                        iMediaIter += 1
                        searchBody = {
                            "albumId": resAlbumOuter0["id"],
                            "pageSize": stepMediaSize,
                            "pageToken": None if iMediaIter==1 else resAlbumInner.get("nextPageToken"),
                        }
                        resAlbumInner = service.mediaItems().search(  # media per album list query (params in searchBody)
                            body = searchBody,
                            fields="nextPageToken,mediaItems(id,productUrl)"
                        ).execute()

                        mediaList0 = []
                        mediaUrls0 = {}

                        #3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3
                        for k in range(len(resAlbumInner.get("mediaItems"))):  # loop on media within each iteration
                        
                            resAlbumInner0 = resAlbumInner.get("mediaItems")[k]  # media list single entry
                            
                            if not (resAlbumOuter0["id"] in mediaList1.keys()):
                                mediaList1.update({resAlbumOuter0["id"]: []})
                                mediaUrls1.update({resAlbumOuter0["id"]: {}})
                            
                            if not (resAlbumInner0["id"] in mediaList1[resAlbumOuter0["id"]]):
                                if k%stepMediaSize==0:
                                    print("  doing media %d/%d" % ((iMediaIter-1)*stepMediaSize+(k+1), int(resAlbumOuter0["mediaItemsCount"])))
                                mediaList0.append(resAlbumInner0["id"])
                                mediaUrls0.update({resAlbumInner0["id"]: resAlbumInner0["productUrl"]})
                                
                            else:
                                if not iMediaExit:
                                    iMediaExit = True
                        #3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3#3
                    
                        # intermediate step: fill these @ the end of every group of media
                        mediaList1[resAlbumOuter0["id"]] += mediaList0
                        mediaUrls1[resAlbumOuter0["id"]].update(mediaUrls0)
                    #2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2#2

                else:
                    nMedia0.append(0)
                    mediaList1.update({resAlbumOuter0["id"]: []})
                    mediaUrls1.update({resAlbumOuter0["id"]: {}})
                    
            else:
                if not iAlbumExit:
                    print("exiting loop on albums...")
                    iAlbumExit = True
                    
    else:
        if not iAlbumExit:
            print("exiting loop on albums...")
            iAlbumExit = True
    #1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#1#
    
    print ("filling all album-related objects for the iteration nr. %d..." % iAlbumIter)
    idsAlbum += idsAlbum0
    titles.update(dict(zip(idsAlbum0, titles0)))
    nMedia.update(dict(zip(idsAlbum0, nMedia0)))
    albumUrls.update(dict(zip(idsAlbum0, albumUrls0)))
    mediaList.update(mediaList1)
    mediaUrls.update(mediaUrls1)
#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#0#

# save a list of the main album info (title, nr. of media, url) in a file
file1 = open(filename1, "w")
for i, iId in enumerate(idsAlbum):
    print(i, titles[iId], nMedia[iId], albumUrls[iId], file=file1)
file1.close()

##############################################
## PART 2) get list of all media in library ##
##############################################
print("\nPART 2) get list of all media in library")

mediaGlobList = []  # list of ids of media in the whole library
mediaNoAlbums = []  # list of ids of zero-album media
mediaNoAlbumsTimes = {}  # creation dates of zero-album media as function of media ids-- human-readable
mediaNoAlbumsUrls = {}  # URLs of zero-album media as function of media ids

print("entering loop on whole library...")
iGlobExit = False  # when this becomes True, the loop on groups of whole library media stops
iGlobIter = 0
while not iGlobExit:  # loop on groups of the whole library (with size stepMediaSize)

    iGlobIter += 1
    print("iteration over media nr. %d" % iGlobIter)
    searchBody = {
        "pageSize": stepMediaSize,
        "pageToken": None if iGlobIter==1 else resLib.get("nextPageToken"),
        "filters": {"includeArchivedMedia": True}
    }
    resLib = service.mediaItems().search(  # whole library media list query (params in searchBody)
        body = searchBody,
        fields = "nextPageToken,mediaItems(id,productUrl,mediaMetadata(creationTime))"
    ).execute()
    
    # counter for loop exit: latter happens when no new media are detected in the last iteration
    iTempExit = 0
    
    for i in range(0 if (resLib.get("mediaItems") is None) else len(resLib.get("mediaItems"))):  # loop on the elements of each groups
    
        resLib0 = resLib.get("mediaItems")[i]  # library single entry
        
        if not (resLib0["id"] in mediaGlobList):
            mediaGlobList.append(resLib0["id"])
            
            nAlbums = 0
            for iId in idsAlbum:  # check presence of the single element in every album
                if resLib0["id"] in mediaList[iId]:
                    nAlbums += 1
                
            if nAlbums == 0:  # if element is absent from all the albums...
                # creation date is given in a human-readable format
                timeObj = time.strptime(resLib0["mediaMetadata"]["creationTime"], '%Y-%m-%dT%H:%M:%SZ')
                mediaNoAlbums.append(resLib0["id"])
                mediaNoAlbumsTimes.update({resLib0["id"]: "%.4d-%.2d-%.2d" % (timeObj.tm_year, timeObj.tm_mon, timeObj.tm_mday)})
                mediaNoAlbumsUrls.update({resLib0["id"]: resLib0["productUrl"]})
                
        else:
            iTempExit += 1
            if (not iGlobExit) & (iTempExit >= len(resLib.get("mediaItems"))):
                print("exiting loop on whole library...")
                iGlobExit = True
            
# count the no-album media per year (also, list of keys is a suitable list of years)
nNoAlbumYears = {}
for iDate in mediaNoAlbumsTimes.values():
    timeObj = time.strptime(iDate, '%Y-%m-%d')
    if not (timeObj.tm_year in nNoAlbumYears.keys()):
        nNoAlbumYears.update({timeObj.tm_year: 0})
    nNoAlbumYears[timeObj.tm_year] += 1
            
# save a list of the no-album media info in a file
file2 = open(filename2, "w")
for i, iId in enumerate(mediaNoAlbums):
    print(i, mediaNoAlbumsTimes[iId], mediaNoAlbumsUrls[iId], file=file2)
file2.close()

#-# [UNUSED]
#-# # also, put all no-album media in a temp album
#-# if len(mediaNoAlbums) > 0:
#-#     createName = "noalbum_quest_temp"  # temporary album name
#-#     createBody = {"album": {"title": createName}}
#-#     newAlbumTemp = service.albums().create(body = createBody).execute()  # temporary album creation query
#-# 
#-#     for i in range(ceil(len(mediaNoAlbums)/stepAddSize)):
#-#         mediaNoAlbumsTemp = mediaNoAlbums[stepAddSize*i:stepAddSize*(i+1)]
#-#         addBody = {"mediaItemIds": mediaNoAlbumsTemp}
#-#         service.albums().batchAddMediaItems(  # temporary album filling query (stepAddSize media at a time)
#-#             albumId = newAlbumTemp["id"],
#-#             body = addBody
#-#         ).execute()

###############################################
# stopping chronometer & printing final results
tStop = time.time()
print("quest completed! in %f s" % (tStop-tStart))

print("total media in the whole library (approx.): %d" % len(mediaGlobList))
print("total media with no album: %d" % sum(nNoAlbumYears.values()))
for iDate in nNoAlbumYears:
    print("no-album media from %d: %d" % (iDate, nNoAlbumYears[iDate]))
#-# print("all these media have been moved to the (temporary) album "+createName)
print("a detailed list can be found in "+filename2)
print("also, an accessible album list can be found in "+filename1)





    
    
    
    
        
    
