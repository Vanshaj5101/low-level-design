-- Problem Statement:
-- 1. Calculate the average years of experience of employees for each project.
-- 2. From these averages, identify the project(s) that have the highest average years of experience.

-- PROBLEM 1

-- SELECT p.project_id, ROUND(AVG(e.experience_years)::NUMERIC, 2) AS average_years 
-- FROM project p
-- INNER JOIN employee e
--     ON p.employee_id = e.employee_id
-- GROUP BY p.project_id

-- PROBLEM 2
-- we want the project with the highest avg years of exp
WITH prj_exp AS (
    SELECT 
        p.project_id, 
        ROUND(AVG(e.experience_years)::NUMERIC, 2) AS average_years
    FROM project p
    INNER JOIN employee e
        ON p.employee_id = e.employee_id
    GROUP BY p.project_id
)
SELECT p.project_id, p.average_years
FROM (
    SELECT 
        p.project_id, 
        p.average_years,
        RANK() OVER (ORDER BY p.average_years DESC) AS rnk
    FROM prj_exp p
) p
WHERE rnk = 1


-- Now say we want, for each project, to show:
-- project_id, average experience (2 decimals), median experience (2 decimals), employee_count
-- …and only include projects with at least 3 employees.

SELECT 
    p.project_id, 
    ROUND(AVG(e.experience_years)::NUMERIC, 2) AS average_years,
    ROUND(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY e.experience_years)::NUMERIC, 2)
    COUNT(e.employee_id) AS employee_count
FROM project p
INNER JOIN employee e
    ON p.employee_id = e.employee_id
GROUP BY p.project_id
HAVING employee_count > 3
ORDER BY p.project_id