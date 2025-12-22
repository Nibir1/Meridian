/*
 * MIGRATION: 20250101_init_schema.sql
 * PURPOSE: Initialize Meridian Database Schema
 * FEATURES: pgvector extension, User Profiles, Document Store (Vectors), Chat History
 */

-- 1. Enable the pgvector extension to work with embeddings
-- This allows us to store 1536-dimensional vectors (OpenAI standard)
create extension if not exists vector;

-- 2. Create the User Profiles table (The "Context")
-- This stores the "Who" - used by ContextLoader to customize answers.
create table public.profiles (
  id uuid primary key default gen_random_uuid(),
  full_name text not null,
  role text not null,          -- e.g., 'CTO', 'CEO', 'Marketing Manager'
  industry text not null,      -- e.g., 'Fintech', 'Healthcare'
  bio text,                    -- A summary of their responsibilities/interests
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 3. Create the Documents table (The "Knowledge")
-- This stores the "What" - technical docs and market reports.
-- We use a jsonb column for flexible metadata (e.g., source, author).
create table public.documents (
  id bigserial primary key,
  content text,                        -- The raw text chunk
  metadata jsonb,                      -- metadata like {"page": 1, "source": "pdf"}
  doc_category text,                   -- CRITICAL: Used for Intent Routing (e.g., 'technical', 'business')
  embedding vector(1536),              -- OpenAI text-embedding-3-small output
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 4. Create Chat History (The "Session Memory")
-- Stores the conversation flow.
create table public.chat_history (
  id bigserial primary key,
  session_id text not null,            -- Group chats by session
  user_id uuid references public.profiles(id), -- Link to specific user persona
  user_message text not null,
  ai_response text not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 5. Create a function to search documents (Hybrid Search helper)
-- This function allows LangFlow to query embeddings with a similarity threshold and metadata filter.
create or replace function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int,
  filter_category text
)
returns table (
  id bigint,
  content text,
  metadata jsonb,
  doc_category text,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    documents.id,
    documents.content,
    documents.metadata,
    documents.doc_category,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where 1 - (documents.embedding <=> query_embedding) > match_threshold
  and documents.doc_category = filter_category -- STRICT FILTERING logic here
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;