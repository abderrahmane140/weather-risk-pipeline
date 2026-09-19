-- 1. Hottest forecast days
SELECT
    c.name AS city,
    w.forecast_date,
    w.temperature_max
FROM weather_forecasts w
JOIN cities c ON c.id = w.city_id
ORDER BY w.temperature_max DESC;


-- 2. Days with the strongest precipitation
SELECT
    c.name AS city,
    w.forecast_date,
    w.precipitation
FROM weather_forecasts w
JOIN cities c ON c.id = w.city_id
ORDER BY w.precipitation DESC;


-- 3. Average risk score by city
SELECT
    c.name AS city,
    ROUND(AVG(w.risk_score), 2) AS average_risk
FROM weather_forecasts w
JOIN cities c ON c.id = w.city_id
GROUP BY c.name
ORDER BY average_risk DESC;


-- 4. Highest-risk forecast days
SELECT
    c.name AS city,
    w.forecast_date,
    w.risk_score,
    w.risk_level
FROM weather_forecasts w
JOIN cities c ON c.id = w.city_id
ORDER BY w.risk_score DESC;


-- 5. Maximum risk for each city
SELECT
    c.name AS city,
    MAX(w.risk_score) AS maximum_risk
FROM weather_forecasts w
JOIN cities c ON c.id = w.city_id
GROUP BY c.name
ORDER BY maximum_risk DESC;


-- 6. Number of forecasts by risk level
SELECT
    risk_level,
    COUNT(*) AS total_days
FROM weather_forecasts
GROUP BY risk_level
ORDER BY total_days DESC;