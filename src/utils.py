from pymongo import MongoClient
import config
import balance

cluster = MongoClient(config.cluster)
db = cluster['astra-balance']


def create_user_db(chat_id):

    collection = db["users"]

    if collection.find_one({"chat_id": chat_id}) == None:
        user = {
            'chat_id': chat_id,
            'notifications': 300,
        }

        collection.insert_one(user)
    else:
        raise ValueError('This user is already created')


def add_card_db(chat_id, card_number, card_name):
    collection = db['users']

    user = collection.find_one({'chat_id': chat_id})

    card_exist = False

    try:
        for dicts in user['cards']:
            for key, val in dicts.items():
                if key == 'card_number' and val == card_number:
                    card_exist = True
    except:
        pass

    if not card_exist:
        collection.update_one(user, {"$push": {"cards":
                                               {
                                                   'card_number': card_number,
                                                   'card_name': card_name.strip(),
                                                   'balance': balance.getBalance(card_number),
                                                   'notified': False,
                                               }}
                                     }, True)
    else:
        raise ValueError('This card is already added')


def update_balance(chat_id):

    collection = db['users']
    user = collection.find_one({"chat_id": chat_id})

    for dicts in user['cards']:

        current_balance = balance.getBalance(dicts['card_number'])

        collection.update({'cards.card_number': dicts['card_number']}, {'$set': {
            'cards.$.balance': current_balance,
        }})

    return user['cards']


if __name__ == "__main__":
    # collection = db["users"]
    # collection.delete_many({})

    pass
