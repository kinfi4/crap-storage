SELECT
    *
FROM pg_stats
WHERE tablename = 'users';


BEGIN;

EXPLAIN ANALYZE
DELETE
FROM users
WHERE username = 'alex';

ROLLBACK;
