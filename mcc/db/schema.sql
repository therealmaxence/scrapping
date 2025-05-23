DROP TABLE IF EXISTS Degree;
DROP TABLE IF EXISTS Topic;
DROP TABLE IF EXISTS Certification;
DROP TABLE IF EXISTS Programme;
DROP TABLE IF EXISTS Semester;
DROP TABLE IF EXISTS Module;

CREATE TABLE Certification (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(150) NOT NULL
);
 
CREATE TABLE Topic (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(150) NOT NULL
);

CREATE TABLE Degree (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(150) NOT NULL,
  description TEXT,
  id_certification INTEGER,
  id_topic INTEGER,
  FOREIGN KEY (id_certification) REFERENCES Certification(id) ON DELETE CASCADE,
  FOREIGN KEY (id_topic) REFERENCES Topic(id) ON DELETE CASCADE
);

CREATE TABLE Programme (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(150) NOT NULL,
  id_degree INTEGER,
  FOREIGN KEY (id_degree) REFERENCES Degree(id) ON DELETE CASCADE
);

CREATE TABLE Semester (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(150) NOT NULL
);

CREATE TABLE Module (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(150) NOT NULL,
  credit INTEGER,
  id_programme INTEGER,
  id_semester INTEGER,
  FOREIGN KEY (id_programme) REFERENCES Programme(id) ON DELETE CASCADE,
  FOREIGN KEY (id_semester) REFERENCES Semester(id) ON DELETE CASCADE
);