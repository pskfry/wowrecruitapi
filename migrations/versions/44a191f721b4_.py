"""empty message

Revision ID: 44a191f721b4
Revises: 0e8fcc6ffde4
Create Date: 2019-09-27 17:19:34.439618

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Table, MetaData
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '44a191f721b4'
down_revision = '0e8fcc6ffde4'
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind())
    meta.reflect(only=('users',))

    users_tbl = Table('users', meta)

    op.bulk_insert(users_tbl,
        [
            {'user_name':'scraper','password':sha256.hash('thescraperneedsaccesstothisshit'),'date_added':datetime.now(),'last_login':None,'permissions':1}
        ]
    )


def downgrade():
    pass
