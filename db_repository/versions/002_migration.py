from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
movie = Table('movie', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=120)),
    Column('description', Text),
)

movies = Table('movies', post_meta,
    Column('movie_id', Integer),
    Column('location_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['movie'].create()
    post_meta.tables['movies'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['movie'].drop()
    post_meta.tables['movies'].drop()
