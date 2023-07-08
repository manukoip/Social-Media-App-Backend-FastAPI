"""add phone number revised

Revision ID: 479f3258e915
Revises: 77e019f38dd1
Create Date: 2023-07-07 22:31:54.674042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '479f3258e915'
down_revision = '77e019f38dd1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'phone_number')
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    op.add_column('posts', sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
