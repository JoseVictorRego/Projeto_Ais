import pandas as pd
import matplotlib.pyplot as plt
from bd_funcao import *

# Uso das funções
conn, cursor = conectar()
if conn and cursor:
    try:
        with cursor:
            # Consulta SQL
            sql_query = ("SELECT situacao, COUNT(DISTINCT id_aluno) as qtd_alunos FROM historico "
                         "WHERE situacao IS NOT NULL AND situacao != 'NÃO INFORMADO' GROUP BY situacao;")

            # Ler dados usando Pandas
            df = pd.read_sql(sql_query, conn)

            # Criar gráfico de barras agrupadas
            fig, ax = plt.subplots()
            width = 0.2  # Largura das barras
            df['qtd_alunos'].plot(kind='bar', color=['green', 'red', 'blue', 'yellow', 'pink', 'purple', 'brown',
                                                     'orange', 'black'], width=width, position=1, ax=ax,
                                  label='Quantidade de Alunos')

            # Adicionar rótulos e título
            plt.xlabel('Situação')
            plt.ylabel('Quantidade de Alunos')
            plt.title('Quantidade de Alunos por Situação')

            # Ajustar rótulos do eixo x
            ax.set_xticks(range(len(df['situacao'])))
            ax.set_xticklabels(df['situacao'])

            # Exibir o gráfico
            plt.legend()
            plt.show()

    finally:
        desconectar(conn, cursor)
