-- FSPY-V3 course kit: 40 real Indian railway stations, for your first SELECT queries.
--
-- The codes, names, states and zones are real. The platform counts and opening years
-- come from each station's English Wikipedia page, read in November 2026. Stations
-- change over time, so treat the numbers as practice data, not as travel information.
--
-- README.md in this folder shows how to load this file into the cloud lab's PostgreSQL.
-- You can run the file more than once: it creates the table only if it does not exist,
-- and it skips rows that are already there.

CREATE TABLE IF NOT EXISTS stations (
    code        VARCHAR(5) PRIMARY KEY,  -- the Indian Railways station code, such as NDLS
    name        TEXT       NOT NULL,     -- the station's name
    state       TEXT       NOT NULL,     -- the state or union territory it is in
    zone        VARCHAR(5) NOT NULL,     -- the railway zone, such as NR for Northern Railway
    platforms   INTEGER    NOT NULL CHECK (platforms > 0),                     -- number of platforms
    opened_year INTEGER    NOT NULL CHECK (opened_year BETWEEN 1850 AND 2030)  -- the year it opened
);

INSERT INTO stations (code, name, state, zone, platforms, opened_year) VALUES
    ('NDLS', 'New Delhi', 'Delhi', 'NR', 16, 1926),
    ('DLI', 'Delhi Junction', 'Delhi', 'NR', 16, 1864),
    ('NZM', 'Hazrat Nizamuddin', 'Delhi', 'NR', 9, 1926),
    ('CDG', 'Chandigarh Junction', 'Chandigarh', 'NR', 6, 1954),
    ('LDH', 'Ludhiana Junction', 'Punjab', 'NR', 7, 1864),
    ('ASR', 'Amritsar Junction', 'Punjab', 'NR', 10, 1862),
    ('JAT', 'Jammu Tawi', 'Jammu and Kashmir', 'NR', 7, 1975),
    ('JP', 'Jaipur Junction', 'Rajasthan', 'NWR', 8, 1895),
    ('AGC', 'Agra Cantonment', 'Uttar Pradesh', 'NCR', 6, 1904),
    ('GWL', 'Gwalior Junction', 'Madhya Pradesh', 'NCR', 6, 1878),
    ('CNB', 'Kanpur Central', 'Uttar Pradesh', 'NCR', 10, 1930),
    ('LKO', 'Lucknow Charbagh', 'Uttar Pradesh', 'NR', 9, 1914),
    ('PRYJ', 'Prayagraj Junction', 'Uttar Pradesh', 'NCR', 10, 1859),
    ('BSB', 'Varanasi Junction', 'Uttar Pradesh', 'NR', 11, 1872),
    ('GKP', 'Gorakhpur Junction', 'Uttar Pradesh', 'NER', 10, 1930),
    ('DDU', 'Pt. Deen Dayal Upadhyaya Junction', 'Uttar Pradesh', 'ECR', 8, 1862),
    ('PNBE', 'Patna Junction', 'Bihar', 'ECR', 10, 1862),
    ('TATA', 'Tatanagar Junction', 'Jharkhand', 'SER', 6, 1910),
    ('HWH', 'Howrah Junction', 'West Bengal', 'ER', 24, 1854),
    ('KGP', 'Kharagpur Junction', 'West Bengal', 'SER', 12, 1899),
    ('NJP', 'New Jalpaiguri Junction', 'West Bengal', 'NFR', 10, 1960),
    ('GHY', 'Guwahati', 'Assam', 'NFR', 7, 1900),
    ('BBS', 'Bhubaneswar', 'Odisha', 'ECoR', 6, 1896),
    ('PURI', 'Puri', 'Odisha', 'ECoR', 8, 1897),
    ('CSMT', 'Mumbai Chhatrapati Shivaji Maharaj Terminus', 'Maharashtra', 'CR', 18, 1853),
    ('BCT', 'Mumbai Central', 'Maharashtra', 'WR', 9, 1930),
    ('PUNE', 'Pune Junction', 'Maharashtra', 'CR', 6, 1858),
    ('NGP', 'Nagpur Junction', 'Maharashtra', 'CR', 8, 1867),
    ('ADI', 'Ahmedabad Junction', 'Gujarat', 'WR', 13, 1863),
    ('BRC', 'Vadodara Junction', 'Gujarat', 'WR', 6, 1861),
    ('BPL', 'Bhopal Junction', 'Madhya Pradesh', 'WCR', 6, 1889),
    ('R', 'Raipur Junction', 'Chhattisgarh', 'SECR', 7, 1888),
    ('MAS', 'Chennai Central', 'Tamil Nadu', 'SR', 17, 1873),
    ('MDU', 'Madurai Junction', 'Tamil Nadu', 'SR', 7, 1875),
    ('TVC', 'Thiruvananthapuram Central', 'Kerala', 'SR', 5, 1931),
    ('ERS', 'Ernakulam Junction', 'Kerala', 'SR', 6, 1932),
    ('SBC', 'KSR Bengaluru City Junction', 'Karnataka', 'SWR', 10, 1968),
    ('MYS', 'Mysuru Junction', 'Karnataka', 'SWR', 6, 1870),
    ('SC', 'Secunderabad Junction', 'Telangana', 'SCR', 10, 1874),
    ('BZA', 'Vijayawada Junction', 'Andhra Pradesh', 'SCoR', 10, 1888)
ON CONFLICT (code) DO NOTHING;  -- a station that is already in the table stays as it is
