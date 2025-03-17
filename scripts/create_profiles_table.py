import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# SQL to create profiles table with RLS
CREATE_PROFILES_TABLE = """
-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
    id UUID REFERENCES auth.users ON DELETE CASCADE,
    username TEXT UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    PRIMARY KEY (id)
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Public profiles are viewable by everyone."
    ON profiles FOR SELECT
    USING ( true );

CREATE POLICY "Users can insert their own profile."
    ON profiles FOR INSERT
    WITH CHECK ( auth.uid() = id );

CREATE POLICY "Users can update their own profile."
    ON profiles FOR UPDATE
    USING ( auth.uid() = id );
"""

def main():
    try:
        # Execute the SQL
        result = supabase.table('profiles').execute(CREATE_PROFILES_TABLE)
        print("Successfully created profiles table and policies")
    except Exception as e:
        print(f"Error creating profiles table: {e}")

if __name__ == "__main__":
    main()
