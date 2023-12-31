"""add foreign key to posts table

Revision ID: 589776aafe1a
Revises: fd6b80ec07cb
Create Date: 2023-07-07 21:55:44.113233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '589776aafe1a'
down_revision = 'fd6b80ec07cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
