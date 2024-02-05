import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Configurações de conexão
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'banco_ais_faculdade'
}

# Grafico para questão 1
def grafico_barra(text_1):

    # texto do select
    sql_query = text_1

    # Ler dados usando Pandas
    df = pd.read_sql(sql_query, conn)

    # Criar gráfico de barras agrupadas com paleta de cores automática
    fig, ax = plt.subplots()
    width = 0.2  # Largura das barras
    colors = plt.cm.get_cmap('tab10', len(df['situacao']))  # Escolhe uma paleta de cores
    df['qtd_alunos'].plot(kind='bar', color=colors(df['situacao'].index), width=width, position=1, ax=ax,
                          label='Quantidade de Alunos')

    # Adicionar rótulos e título
    plt.xlabel('Situação')
    plt.ylabel('Quantidade de Alunos')
    plt.title('Quantidade de Alunos por Situação')

    # Ajustar rótulos do eixo x
    ax.set_xticks(range(len(df['situacao'])))
    ax.set_xticklabels(df['situacao'])

    # Ajustar o bottom para 0.52
    ax.set_position([0.125, 0.52, 0.775, 0.35])  # [left, bottom, width, height]

    # Salvar o gráfico num arquivo PNG
    plt.savefig('Q1_grafico_barra.png')

# Grafico para questão 2
def grafico_pizza(text_2):

    # texto do select
    sql_query = text_2

    # Ler dados usando Pandas
    df = pd.read_sql(sql_query, conn)

    # Criar gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(df['qtd_reprovacoes'], labels=df['nome_disciplina'], autopct='%1.1f%%', startangle=90,
            colors=plt.cm.Paired.colors)
    plt.title('Tops Disciplinas com Maior Quantidade de Reprovações')

    # Salvar o gráfico num arquivo PNG
    plt.savefig('Q2_grafico_pizza.png')

# ----------------------------Usar funções---------------------------------

# Conectar ao MySQL
conn = mysql.connector.connect(**config)

# Consulta SQL para a questão 1
pesquisa_1 = ("SELECT situacao, COUNT(DISTINCT id_aluno) as qtd_alunos FROM historico "
              "WHERE situacao IS NOT NULL AND situacao != 'NÃO INFORMADO' GROUP BY situacao;")

# Importar grafico
grafico_barra(pesquisa_1)

# Consulta SQL para a questão 2
pesquisa_2 = ("SELECT d.nome_disciplina, COUNT(*) as qtd_reprovacoes FROM historico h JOIN disciplina d "
              "ON h.id_disciplina = d.id_disciplina WHERE h.situacao = 'Reprovado' "
              "OR h.situacao = 'Reprovado por falta' GROUP BY h.id_disciplina ORDER BY qtd_reprovacoes DESC LIMIT 5;")

# Importar grafico
grafico_pizza(pesquisa_2)

# Fechar a conexão
conn.close()
