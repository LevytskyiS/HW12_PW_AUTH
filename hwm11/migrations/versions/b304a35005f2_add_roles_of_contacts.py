"""Add roles of contacts

Revision ID: b304a35005f2
Revises: 19e2e3da5b11
Create Date: 2023-03-03 18:41:15.495276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b304a35005f2'
down_revision = '19e2e3da5b11'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('role', sa.Enum('admin', 'moderator', 'user', name='roles'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contacts', 'role')
    # ### end Alembic commands ###
