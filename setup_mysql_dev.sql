CREATE DATABASE IF NOT EXISTS h_tats_int;
CREATE USER IF NOT EXISTS 'onyx' @'localhost' IDENTIFIED BY 'TATS_123_pwd';
GRANT USAGE ON *.* TO 'onyx' @'localhost';
GRANT SELECT ON `performance_schema`.* TO 'onyx' @'localhost';
GRANT ALL PRIVILEGES ON `h_tats_int`.* TO 'onyx' @'localhost';
FLUSH PRIVILEGES;