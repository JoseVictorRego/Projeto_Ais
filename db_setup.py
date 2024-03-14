import mysql.connector

import os
from dotenv import load_dotenv

load_dotenv() 

def setup_database():
  
  config = {
            'host': os.getenv('HOST'),
            'user': os.getenv('USER'),
            'password': os.getenv('PASSWORD'),
        }
  
  conn = mysql.connector.connect(**config)
  cursor = conn.cursor()

  cursor.execute("CREATE DATABASE IF NOT EXISTS banco_ais_faculdade")

  cursor.execute("USE banco_ais_faculdade")

  cursor.execute("""
    CREATE TABLE IF NOT EXISTS aluno (
      id_aluno INT UNSIGNED AUTO_INCREMENT,
      nome_aluno VARCHAR(255) NOT NULL,
      sexo CHAR(1),
      forma_ingresso VARCHAR(50),
      periodo_ingresso DOUBLE,
      PRIMARY KEY (id_aluno)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  """)

  cursor.execute("""
    CREATE TABLE IF NOT EXISTS disciplina (
      id_disciplina INT UNSIGNED AUTO_INCREMENT,
      nome_disciplina VARCHAR(255),
      codigo_disciplina VARCHAR(255),
      carga_horaria INT,
      creditos INT,
      PRIMARY KEY (id_disciplina)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  """)

  cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico (
      id_historico INT UNSIGNED AUTO_INCREMENT,
      semestre DOUBLE,
      id_aluno INT UNSIGNED,
      id_disciplina INT UNSIGNED,
      id_professor INT UNSIGNED,
      nota_final DOUBLE,
      situacao VARCHAR(50),
      PRIMARY KEY (id_historico),
      KEY id_aluno (id_aluno),
      KEY id_professor (id_professor),
      KEY id_disciplina (id_disciplina)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  """)

  cursor.execute("""
    CREATE TABLE IF NOT EXISTS professor (
      id_professor INT UNSIGNED AUTO_INCREMENT,
      nome_professor VARCHAR(255),
      PRIMARY KEY (id_professor)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  """)

  # cursor.execute("""
  #   ALTER TABLE historico
  #   ADD CONSTRAINT historico_ibfk_1 FOREIGN KEY (id_aluno) REFERENCES aluno (id_aluno),
  #   ADD CONSTRAINT historico_ibfk_2 FOREIGN KEY (id_professor) REFERENCES professor (id_professor),
  #   ADD CONSTRAINT historico_ibfk_3 FOREIGN KEY (id_disciplina) REFERENCES disciplina (id_disciplina)
  # """)

  cursor.close()
  conn.close()