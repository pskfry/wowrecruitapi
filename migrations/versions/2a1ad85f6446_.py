"""empty message

Revision ID: 2a1ad85f6446
Revises: 44a191f721b4
Create Date: 2019-09-27 18:10:02.123610

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Table, MetaData
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '2a1ad85f6446'
down_revision = '44a191f721b4'
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind())
    meta.reflect(only=('users',))

    users_tbl = Table('users', meta)

    op.bulk_insert(users_tbl,
        [
            {'user_name':'ogwebapp','password':sha256.hash('thewebappneedssomeaccesstoobiznatch'),'date_added':datetime.now(),'last_login':None,'permissions':1}
        ]
    )


def downgrade():
    pass
