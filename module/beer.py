class Beer:
    def __init__(self, args):
        self.date = args.get('date', None)
        self.brewery = args.get('brewery', None)
        self.name = args.get('name', None)
        self.description = args.get('description', None)
        self.aroma = args.get('aroma', None)
        self.taste = args.get('taste', None)
        self.finish = args.get('finish', None)
        self.rating = args.get('rating', None)

    def to_dict(self):
        return {
            'date': self.date,
            'brewery': self.brewery,
            'name': self.name,
            'description': self.description,
            'aroma': self.aroma,
            'taste': self.taste,
            'finish': self.finish,
            'rating': self.rating,
        }

class BeerCollection:
    def __init__(self, beers={}):
        self.beers = beers

    @staticmethod
    def from_firebase_doc(doc):
        beer_collection = BeerCollection()

        for beer in doc:
            beer_collection.add_beer(beer.id, Beer(beer.to_dict()))

        return beer_collection

    def add_beer(self, id, content):
        if id in self.beers:
            return

        self.beers[id] = content

    def get_basic_details(self):
        return [ { 'id': beer.id, 'name': beer.name, 'brewery': beer.brewery, 'rating': beer.rating } for beer in self.beers ]

    def get_full_details(self, beer_id):
        if not self.beers[beer_id]:
            return self.beers[beer_id].to_dict()

        return None
