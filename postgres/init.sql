-- Extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- busca por texto

-- Índices extras para performance
-- (as tabelas são criadas pelo SQLAlchemy no startup)

-- View útil: resumo de execuções por pipeline
-- CREATE OR REPLACE VIEW pipeline_summary AS
-- SELECT
--     p.id,
--     p.name,
--     p.status,
--     COUNT(r.id) AS total_runs,
--     COUNT(CASE WHEN r.status = 'success' THEN 1 END) AS successful_runs,
--     COUNT(CASE WHEN r.status = 'failed'  THEN 1 END) AS failed_runs,
--     SUM(r.rows_processed) AS total_rows_processed,
--     MAX(r.created_at) AS last_run_at
-- FROM pipelines p
-- LEFT JOIN pipeline_runs r ON r.pipeline_id = p.id
-- GROUP BY p.id, p.name, p.status;
