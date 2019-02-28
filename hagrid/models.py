import mongoengine as mgo


class AssetBase(mgo.Document):
    """An AssetBase document. Abstract base document."""

    symbol = mgo.StringField(max_length=10, required=True)
    name = mgo.StringField(required=True)
    exchange = mgo.StringField()
    meta = {'abstract': True}


class Asset(AssetBase):
    """An asset document."""

    meta = {
        'collection': 'assets',
    }
