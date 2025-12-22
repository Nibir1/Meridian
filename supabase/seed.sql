/*
 * SEED DATA: User Personas
 * PURPOSE: Populate the profiles table with distinct user types for testing Context Injection.
 */

-- 1. Clean existing data (Optional, for development reset)
truncate table public.profiles cascade;

-- 2. Insert Persona A: The Technical CTO
-- Expected AI Behavior: Detailed, code-heavy, security-conscious responses.
insert into public.profiles (id, full_name, role, industry, bio)
values (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', -- Hardcoded UUID for easy reference in app
    'Sarah Jenkins',
    'CTO',
    'Fintech',
    'Responsible for backend architecture, API security, and Python microservices. Prefers technical documentation and architectural diagrams over sales pitch.'
);

-- 3. Insert Persona B: The Strategic CEO
-- Expected AI Behavior: High-level, ROI-focused, market-trend oriented responses.
insert into public.profiles (id, full_name, role, industry, bio)
values (
    'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22', -- Hardcoded UUID for easy reference in app
    'Marcus Thorne',
    'CEO',
    'Retail',
    'Focused on quarterly revenue, market expansion, and competitor analysis. Needs executive summaries and pricing strategies, not code.'
);