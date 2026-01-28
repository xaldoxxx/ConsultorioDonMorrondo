
INSERT INTO user (username, password, role) VALUES
('admin',  'pbkdf2:sha256:600000$admin$hash', 'admin'),
('user1',  'pbkdf2:sha256:600000$user1$hash', 'usuario1'),
('user2',  'pbkdf2:sha256:600000$user2$hash', 'usuario2'),
('user3',  'pbkdf2:sha256:600000$user3$hash', 'usuario3');
