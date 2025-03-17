"""create_profiles_table

Revision ID: 8828051e3297
Revises: 5b6d23ea72e9
Create Date: 2025-02-12 13:21:22.692368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8828051e3297'
down_revision: Union[str, None] = '5b6d23ea72e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if we're using PostgreSQL
    is_postgresql = op.get_context().dialect.name == 'postgresql'
    
    # Create the profiles table
    if is_postgresql:
        op.create_table(
            'profiles',
            sa.Column('id', sa.UUID(), nullable=False),
            sa.Column('username', sa.String(), nullable=False),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('username')
        )
        
        # Create RLS policies for PostgreSQL
        op.execute("""
            ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
            
            CREATE POLICY "Public profiles are viewable by everyone."
                ON profiles FOR SELECT
                USING ( true );

            CREATE POLICY "Users can insert their own profile."
                ON profiles FOR INSERT
                WITH CHECK ( auth.uid() = id );

            CREATE POLICY "Users can update their own profile."
                ON profiles FOR UPDATE
                USING ( auth.uid() = id );
        """)
    else:
        # SQLite version
        op.create_table(
            'profiles',
            sa.Column('id', sa.String(36), nullable=False),  # UUID as string for SQLite
            sa.Column('username', sa.String(), nullable=False),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('username')
        )


def downgrade() -> None:
    # Check if we're using PostgreSQL
    is_postgresql = op.get_context().dialect.name == 'postgresql'
    
    if is_postgresql:
        # Drop RLS policies for PostgreSQL
        op.execute("""
            DROP POLICY IF EXISTS "Public profiles are viewable by everyone." ON profiles;
            DROP POLICY IF EXISTS "Users can insert their own profile." ON profiles;
            DROP POLICY IF EXISTS "Users can update their own profile." ON profiles;
        """)
    
    op.drop_table('profiles')
