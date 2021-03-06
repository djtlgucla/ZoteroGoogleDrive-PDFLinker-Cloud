#!/usr/bin/env python3

from sys import stderr as cerr

class ZoteroLibs:
    
    @staticmethod
    def progress(format_message, num1, num2, num3):
        """Displays progress for 3 items given a format template"""
        print(format_message % (num1,num2,num3), end='\r', file=cerr)


    @staticmethod
    def findCollectionID(zot, name = ""):
        """Finds the collectionID for a collection name"""

        res = {}
        for zz in zot.collections():
            if name == "" or (name != "" and (zz['data']['name'] == name)):

                title = zz['data']['name']
                value = zz['key']

                if title not in res:
                    res[title] = []
                res[title].append( value )


        if len(res) == 1:
            if len(res[name]) == 1:
                return res[name][0]       

        print("Multiple collections found:\n%s" % res, file=cerr)
        exit(-1)


        
    @staticmethod
    def iterateTopLevelItems(zot, collectionID, callback, progmessage):
        """Iterate through all items in the collection and perform callback upon each item"""
        # Can handle 100 at a time
        start_it = 0
        limit_vl = 100

        total_processed = 0
        total_v1        = 0
        total_v2        = 0


        while True:
            items = zot.collection_items_top(collectionID,
                                             start=start_it, limit = limit_vl)
            start_it += limit_vl
            len_items = len(items)

            if len_items == 0:
                break

            for item in items:
                val1, val2 = callback(item)
                total_processed += 1
                total_v1        += val1
                total_v2        += val2

               
                ZoteroLibs.progress(progmessage, total_processed, total_v1, total_v2)   # per item update
            ZoteroLibs.progress(progmessage, total_processed, total_v1, total_v2)       # per batch query update
        ZoteroLibs.progress(progmessage, total_processed, total_v1, total_v2)           # upon completion


    ####### DEBUG ######
    @staticmethod
    def getAllItems(self):
        """Prints out all items"""
        ZoteroLibs.iterateItemsInCollection(
            zot,
            collectionID,
            ZoteroItemFuncs.printItem,
            "total %d, attached %d, url %d"
        )
