# 1 Qts alunos/status (quem)
SELECT situacao, COUNT(*) as qtd_alunos
FROM historico
GROUP BY situacao;
# 2 Disciplinas que mais reprovam por nota/falta/situação
SELECT id_disciplina, COUNT(*) as qtd_reprovacoes FROM historico WHERE situacao = 'Reprovado' GROUP BY id_disciplina;
# 3 Dado um aluno: Qts/Quais disciplinas ele falta cursar
# 4 Dada uma disciplinas, qtos alunos estão aptos a cursá-lá (aluno nunca cursou/reprovado)
# 5 Listar alunos regularmente matriculados no curso/disciplina
# 6 Média de alunos por disciplina
SELECT d.nome_disciplina, h.semestre, AVG(qtd_alunos) as media_alunos
FROM (
    SELECT id_disciplina, id_aluno, COUNT(*) as qtd_alunos
    FROM historico
    GROUP BY id_disciplina, id_aluno
) as disciplina_count
JOIN historico h ON disciplina_count.id_disciplina = h.id_disciplina AND disciplina_count.id_aluno = h.id_aluno
JOIN disciplina d ON h.id_disciplina = d.id_disciplina
GROUP BY d.nome_disciplina, h.semestre;
# 7 Alunos formados no tempo certo
# 8 Listar alunos com desistência / alunos reprovados por falta
SELECT nome_aluno, situacao FROM aluno JOIN historico ON aluno.id_aluno = historico.id_aluno WHERE situacao = 'Desistência' OR situacao = 'Reprovado por Falta';
# 9 Listar alunos trancados
SELECT DISTINCT a.nome_aluno
FROM aluno a
JOIN historico h ON a.id_aluno = h.id_aluno
WHERE h.id_disciplina = 402;
# 10 Listar alunos que serão jubilados
SELECT a.nome_aluno, COUNT(DISTINCT h.semestre) as qtd_semestres
FROM aluno a
JOIN historico h ON a.id_aluno = h.id_aluno
GROUP BY a.id_aluno, a.nome_aluno
HAVING qtd_semestres > 12;
# 11 nº de disciplinas x professor x ano/sem quais
SELECT nome_professor, semestre, COUNT(DISTINCT id_disciplina) as qtd_disciplinas FROM historico JOIN professor ON historico.id_professor = professor.id_professor GROUP BY nome_professor, semestre;