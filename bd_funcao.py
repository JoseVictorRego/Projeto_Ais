import mysql.connector

# ---------------------------------Funções conectar e desconectar do banco de dados---------------------------

# Função conectar no banco
def conectar():
    """Conectar ao banco de dados."""
    try:
        config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'banco_ais_faculdade'
        }

        # Conectar ao MySQL
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        return conn, cursor

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None, None

# Função desconectar no banco
def desconectar(conn, cursor):
    """Desconectar do banco de dados."""
    # Fechar a conexão
    if conn and conn.is_connected():
        cursor.close()
        conn.close()
        print("Conexão fechada.")

# ------------------Funções para obter Id_ das tabelas do banco de dados----------------------------------

# Função consutar id_aluno no banco
def consultar_id_aluno(conn, cursor, nome, sexo, forma_ingresso, periodo_ingresso):

    # Tentar inserir aluno no banco, caso ele não esteja cadastrado
    inserir_dados_aluno(conn, cursor, nome, sexo, forma_ingresso, periodo_ingresso)

    # Obter o id_aluno
    query = ("SELECT id_aluno FROM aluno "
             "WHERE nome_aluno = %s AND sexo = %s AND forma_ingresso = %s AND periodo_ingresso = %s")
    cursor.execute(query, (nome, sexo, forma_ingresso,  periodo_ingresso))
    result = cursor.fetchone()

    # Retorna o id_aluno
    return result[0]

# Função consutar id_disciplina no banco
def consultar_id_disciplina(conn, cursor, codigo_disciplina, nome_disciplina, carga_horaria, creditos):

    # Tentar inserir dados de disciplina
    inserir_dados_disciplina(conn, cursor, codigo_disciplina, nome_disciplina, carga_horaria, creditos)

    # Obter o id_disciplina
    query = "SELECT id_disciplina FROM disciplina WHERE nome_disciplina = %s"
    cursor.execute(query, (nome_disciplina, ))
    result = cursor.fetchone()

    # Retorna o id_disciplina
    return result[0]

# Função consutar id_professor no banco
def consultar_id_professor(conn, cursor, nome_professor):

    # Tentar inserir professor no banco caso ele não esteja cadastrado
    inserir_dados_professor(conn, cursor, 'professor', 'nome_professor', nome_professor)

    # Obter o id_professor
    query = "SELECT id_professor FROM professor WHERE nome_professor = %s"
    cursor.execute(query, (nome_professor,))
    result = cursor.fetchone()

    # Retorna o id_professor
    return result[0]

# Função consutar id_historico no banco
def consultar_id_historico(conn, cursor, semestre, id_aluno, id_disciplina, id_professor, nota_final, situacao):

    # Tentar inserir professor no banco caso ele não esteja cadastrado
    inserir_dados_historico(conn, cursor, semestre, id_aluno, id_disciplina, id_professor, nota_final, situacao)

    # Obter o id_historico
    query = "SELECT id_historico FROM historico WHERE semestre = %s AND id_aluno = %s  AND id_disciplina = %s"
    cursor.execute(query, (semestre, id_aluno, id_disciplina))
    result = cursor.fetchone()

    # Retorna o id_historico se encontrado
    return result[0]

# -------------------Funções para adicionar Aluno---------------------------------------------------------------------

# Função para verificar se o aluno já consta no banco de dados
def verificar_duplicacao_aluno(cursor, nome, sexo, forma_ingresso, periodo_ingresso):

    # Verificar se a linha já existe
    check_duplicate_query = """
    SELECT * FROM aluno
    WHERE nome_aluno = %s AND sexo = %s AND forma_ingresso = %s AND periodo_ingresso = %s
    """

    params = (nome, sexo, forma_ingresso, periodo_ingresso)
    cursor.execute(check_duplicate_query, params)
    result = cursor.fetchall()

    return len(result) > 0

# Função de inserir o aluno no banco de dados
def inserir_dados_aluno(conn, cursor, nome, sexo, forma_ingresso, periodo_ingresso):

    # if para adicionar apenas o aluno que não estão cadastrados ainda no banco de dados.
    if not verificar_duplicacao_aluno(cursor, nome, sexo, forma_ingresso, periodo_ingresso):

        # Inserção de dados
        insert_data_query = """
        INSERT INTO aluno (nome_aluno, sexo, forma_ingresso, periodo_ingresso)
        VALUES (%s, %s, %s, %s)
        """

        aluno_data = (nome, sexo, forma_ingresso, periodo_ingresso)
        cursor.execute(insert_data_query, aluno_data)
        conn.commit()
        print(f"\nAluno {nome} inseridos com sucesso!\n")

# -------------------Funções para adicionar Professor------------------------------------------------------------------

# Função para verificar se o professor já consta no banco de dados
def verificar_duplicacao_professor(cursor, tabela, nome_coluna, valor):

    # Verificar se a linha já existe
    check_duplicate_query = f"""
    SELECT * FROM {tabela}
    WHERE {nome_coluna} = %s
    """

    params = (valor,)
    cursor.execute(check_duplicate_query, params)
    result = cursor.fetchall()

    return len(result) > 0

# Função de inserir o professor no banco de dados
def inserir_dados_professor(conn, cursor, tabela, nome_coluna, valor):

    # if para adicionar apenas o professor que não estão cadastrados ainda no banco de dados.
    if not verificar_duplicacao_professor(cursor, tabela, nome_coluna, valor):

        # Inserção de dados
        insert_data_query = f"""
        INSERT INTO {tabela} ({nome_coluna})
        VALUES (%s)
        """

        data = (valor,)
        cursor.execute(insert_data_query, data)
        conn.commit()
        print(f"\nProfessor {valor} inseridos com sucesso!\n")

# -------------------Funções para adicionar Disciplina----------------------------------------------------------------

# Função para verificar se a disciplina já consta no banco de dados
def verificar_duplicacao_disciplina(cursor, nome_disciplina):

    # Verificar se a linha já existe
    check_duplicate_query = """
    SELECT * FROM disciplina
    WHERE nome_disciplina = %s
    """

    params = (nome_disciplina, )
    cursor.execute(check_duplicate_query, params)
    result = cursor.fetchall()

    return len(result) > 0

# Função de inserir a disciplina no banco de dados
def inserir_dados_disciplina(conn, cursor, codigo_disciplina, nome_disciplina, carga_horaria, creditos):

    # if para adicionar apenas a disciplina que não estão cadastrados ainda no banco de dados.
    if not verificar_duplicacao_disciplina(cursor, nome_disciplina):

        # Inserção de dados
        insert_data_query = """
        INSERT INTO disciplina (codigo_disciplina, nome_disciplina, carga_horaria, creditos)
        VALUES (%s, %s, %s, %s)
        """

        disciplina_data = (codigo_disciplina, nome_disciplina, carga_horaria, creditos)
        cursor.execute(insert_data_query, disciplina_data)
        conn.commit()
        print(f"\nDisiciplina {nome_disciplina} inserida com sucesso!\n")

# -------------------Funções para adicionar Historico----------------------------------------------------------------

# Função para verificar se o historico já consta no banco de dados
def verificar_duplicacao_historico(cursor, semestre, id_aluno, id_disciplina):
    # Verificar se a linha já existe
    check_duplicate_query = """
    SELECT * FROM historico
    WHERE semestre = %s AND id_aluno = %s AND id_disciplina = %s
    """

    params = (semestre, id_aluno, id_disciplina)
    cursor.execute(check_duplicate_query, params)
    result = cursor.fetchall()

    return len(result) > 0

# Função de inserir o historico no banco de dados
def inserir_dados_historico(conn, cursor, semestre, id_aluno, id_disciplina, id_professor, nota_final, situacao):

    # if para adicionar apenas o historico que não estão cadastrados ainda no banco de dados.
    if not verificar_duplicacao_historico(cursor, semestre, id_aluno, id_disciplina):

        # Inserção de dados
        insert_data_query = """
        INSERT INTO historico (semestre, id_aluno, id_disciplina, id_professor, nota_final, situacao)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        historico_data = (semestre, id_aluno, id_disciplina, id_professor, nota_final, situacao)
        cursor.execute(insert_data_query, historico_data)
        conn.commit()
        print(f"Historico: {semestre}, {id_aluno}, {id_disciplina}, {id_professor},"
              f" {situacao}, inserida com sucesso!\n")

    else:
        print("Dados Historico já inserido no banco de dados")

# -----------------------------------Funções diversas-------------------------------------------------------------

# Consutar todos os dados da tabela informada
def consultar_dados(cursor, tabela):
    # Exemplo de consulta de dados
    select_data_query = f"SELECT * FROM {tabela}"
    cursor.execute(select_data_query)
    result = cursor.fetchall()

    print(f"\nRegistros na tabela '{tabela}':")
    for row in result:
        print(row)

def consultar_dado_especifico_da_tabela(cursor, tabela, coluna, id_especifico):
    # Exemplo de consulta de dados por ID
    select_data_query = f"SELECT * FROM {tabela} WHERE {coluna} = {id_especifico}"
    cursor.execute(select_data_query)
    result = cursor.fetchall()

    print(f"\nRegistro do ID {id} na tabela '{tabela}':")
    for row in result:
        print(row)


"""
# Uso das funções
conn, cursor = conectar()
if conn and cursor:
    try:
        with cursor:

            inserir_dados_aluno(conn, cursor, 'Maria Santos', 'F', 'Vestibular', 2002.2)
            consultar_dados(cursor, 'aluno')

            inserir_dados_professor(conn, cursor, 'professor', 'nome_professor', 'Jose Joao')
            consultar_dados(cursor, 'professor')

            inserir_dados_disciplina(conn, cursor, 'OAEVG825', 'informatica produto', 40, 2)
            consultar_dados(cursor, 'disciplina')

            inserir_dados_historico(conn, cursor, 2005.2, 2, 1, None, 9.8, 'APROVADO')
            consultar_dados(cursor, 'historico')

    finally:
        desconectar(conn, cursor)"""