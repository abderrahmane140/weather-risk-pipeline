CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    UNIQUE(name, latitude, longitude)
);


CREATE TABLE weather_forecasts (
    id SERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities(id) ON DELETE CASCADE,

    forecast_date DATE NOT NULL,

    temperature_max DECIMAL(5, 2),
    temperature_min DECIMAL(5, 2),

    precipitation DECIMAL(6, 2),
    precipitation_probability INTEGER,

    wind_speed_max DECIMAL(6, 2),
    wind_gust_max DECIMAL(6, 2),

    weather_code INTEGER,

    temperature_category VARCHAR(30),
    rain_category VARCHAR(30),
    wind_category VARCHAR(30),

    temperature_risk INTEGER,
    rain_risk INTEGER,
    wind_risk INTEGER,

    risk_score DECIMAL(5, 2),
    risk_level VARCHAR(30),

    UNIQUE(city_id, forecast_date)
);