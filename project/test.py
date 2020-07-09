# store_info = list(db.food_store.find({'station': station_receive}, {'_id': 0}))
def storeInfoLists(standard) :
    a = str(standard) + "Info = list(db.food_store.find({'" + str(standard) + "': " + str(standard) + "_receive}, {'_id': 0}))"
    return print(a)

storeInfoLists('station')