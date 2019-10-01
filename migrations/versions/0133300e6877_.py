"""empty message

Revision ID: 0133300e6877
Revises: 8a70b93b495d
Create Date: 2019-09-26 00:35:34.725596

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0133300e6877'
down_revision = '8a70b93b495d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scrape_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scrape_start', sa.DateTime(), nullable=True),
    sa.Column('scrape_end', sa.DateTime(), nullable=True),
    sa.Column('char_count', sa.Integer(), nullable=True),
    sa.Column('min_ilvl', sa.Float(), nullable=True),
    sa.Column('pages_scraped', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('characters', 'char_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('characters', 'last_update',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('characters', 'last_update',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('characters', 'char_name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.drop_table('scrape_log')
    # ### end Alembic commands ###
