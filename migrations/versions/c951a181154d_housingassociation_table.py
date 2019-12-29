"""HousingAssociation table

Revision ID: c951a181154d
Revises: 
Create Date: 2019-12-29 12:10:32.725996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c951a181154d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('housing_association',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('business_id', sa.String(length=10), nullable=True),
    sa.Column('street', sa.String(length=100), nullable=True),
    sa.Column('street_number', sa.Integer(), nullable=True),
    sa.Column('postal_code', sa.String(length=15), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('housing_association')
    # ### end Alembic commands ###
