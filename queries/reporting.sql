-- 1.
SELECT 
    title, 
    TRIM(REPLACE(author, 'By ', '')) AS clean_author 
FROM 
    wired_articles;

-- 2.
SELECT 
    TRIM(REPLACE(author, 'By ', '')) AS clean_author, 
    COUNT(*) as article_count 
FROM 
    wired_articles 
GROUP BY 
    clean_author 
ORDER BY 
    article_count DESC 
LIMIT 3;

-- 3. 
SELECT 
    * FROM 
    wired_articles 
WHERE 
    title ILIKE '%AI%' OR title ILIKE '%Climate%' OR title ILIKE '%Security%'
    OR description ILIKE '%AI%' OR description ILIKE '%Climate%' OR description ILIKE '%Security%';