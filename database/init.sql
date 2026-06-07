CREATE TABLE IF NOT EXISTS operation_records (
  id SERIAL PRIMARY KEY,
  module_name VARCHAR(120) NOT NULL,
  owner_name VARCHAR(80) NOT NULL,
  status VARCHAR(40) NOT NULL,
  metric VARCHAR(40) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO operation_records (module_name, owner_name, status, metric)
VALUES ('场地与场次管理', '运营组', 'ready', '100%');

CREATE TABLE IF NOT EXISTS fields (
  id SERIAL PRIMARY KEY,
  name VARCHAR(80) NOT NULL,
  description VARCHAR(255),
  max_players INTEGER NOT NULL DEFAULT 20,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO fields (name, description, max_players) VALUES
('丛林战场', '模拟热带雨林地形，适合伏击战术', 24),
('废墟战场', '城市废墟风格，适合巷战攻防', 20),
('CQB室内场', '近距离作战场地，适合快速反应', 16);

CREATE TABLE IF NOT EXISTS time_slots (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO time_slots (name, start_time, end_time) VALUES
('上午场', '09:00:00', '12:00:00'),
('下午场', '14:00:00', '17:00:00'),
('夜场', '19:00:00', '22:00:00');

CREATE TABLE IF NOT EXISTS booking_records (
  id SERIAL PRIMARY KEY,
  player_name VARCHAR(80) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  booking_date DATE NOT NULL,
  field_id INTEGER NOT NULL REFERENCES fields(id),
  slot_id INTEGER NOT NULL REFERENCES time_slots(id),
  player_count INTEGER NOT NULL DEFAULT 1,
  status VARCHAR(20) DEFAULT 'pending',
  remark VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_booking_date ON booking_records(booking_date);
CREATE INDEX idx_booking_status ON booking_records(status);
