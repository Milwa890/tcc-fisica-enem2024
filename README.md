# tcc-fisica-enem2024

Código do Trabalho de Conclusão de Curso **"Análise de erros nas questões de Física do ENEM 2024: um estudo a partir dos microdados do INEP"**, Licenciatura em Física, Instituto Federal de Brasília (IFB).

**Autoria:** Gabriela Barbosa (pipeline original de processamento dos microdados e fluxogramas da metodologia) e Melissa Assunção (adaptação, análise de distratores e parâmetros da TRI).

## O que o notebook faz

| Etapa | Descrição |
|---|---|
| 0 | Configuração de pastas e parâmetros |
| 1 | Conversão de `RESULTADOS_2024.csv` para Parquet, só com as colunas necessárias e em blocos (cabe na RAM do Colab) |
| 2 | Itens, gabaritos, parâmetros da TRI e mapeamento das questões para o caderno azul |
| 3 | Respostas na ordem do caderno azul (presentes nas quatro provas, cadernos regulares 1419–1422) |
| 4 | Taxa de acerto e frequência de cada alternativa |
| 5 | Curvas de escolha das alternativas em três réguas de desempenho |
| 6 | Parâmetros a, b, c da TRI e acerto previsto × observado |
| 7 | Exportação da planilha final |

## Dados

Os microdados **não estão incluídos** neste repositório por causa do tamanho. Baixe os Microdados do Enem 2024 no portal do INEP:
https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem

Coloque `RESULTADOS_2024.csv` e `ITENS_PROVA_2024.csv` na pasta `raw/` dentro de `PASTA_PROJETO` (definida na Etapa 0).

## Como executar

1. Abra o notebook no Google Colab.
2. Ajuste `PASTA_PROJETO` na Etapa 0.
3. Execute as células em ordem. Os resultados (planilhas `.xlsx` e figuras) são gravados em `processed/`.

Dependências: `pandas`, `numpy`, `pyarrow`, `matplotlib`, `scipy`, `openpyxl` (já presentes no Colab).

## Figuras do TCC

O script `gerar_figuras_tcc.py` refaz as figuras de resultados do TCC (Figuras 2 a 5, 8, 14, 15 e 16) a partir das três planilhas que o notebook grava em `processed/`. Ele não lê os microdados, então roda em poucos segundos.

No Colab, depois de executar o notebook:

```
!python gerar_figuras_tcc.py "/content/drive/MyDrive/TCC Melissa/enem-fisica/processed"
```

As figuras são salvas em `processed/figuras_tcc/`. A Figura 1 (fluxograma de Gabriela Barbosa) e as imagens das questões (recortadas do caderno azul do Inep) não são geradas por este script.

## Observações

- A questão 129 foi anulada e não entra nas análises.
- Os arquivos de resultados do INEP não têm a variável `IN_TREINEIRO`, então os treineiros não puderam ser excluídos.
- Modelo da TRI (INEP, 2021): P = c + (1 − c) / (1 + exp[−a(θ − b)]), com θ = (nota − 500)/100.

## Como citar

BARBOSA, Gabriela; ASSUNÇÃO, Melissa. **tcc-fisica-enem2024**: processamento dos microdados do Enem 2024 para análise das questões de Física. [S. l.]: GitHub, 2026. Disponível em: https://github.com/Milwa890/tcc-fisica-enem2024.
