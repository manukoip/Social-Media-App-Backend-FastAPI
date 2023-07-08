"""add_content_column_to_posts_table

Revision ID: 88dfba04bddb
Revises: 3dc422e94813
Create Date: 2023-07-07 21:41:20.434415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88dfba04bddb'
down_revision = '3dc422e94813'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
