# Critérios e Testes de Aceitação

## AC-01 — Importação de CSV

### Critérios
- O arquivo CSV deve ser carregado corretamente
- As colunas obrigatórias devem existir
- Dados inválidos devem ser rejeitados

### Teste de Aceitação
Entrada:
CSV válido contendo OHLCV

Resultado esperado:
Importação realizada sem erro.

---

## AC-02 — Validação de Dados

### Critérios
- Datas duplicadas devem ser rejeitadas
- Datas fora de ordem devem ser rejeitadas
- Capital inválido deve gerar erro

### Teste de Aceitação
Entrada:
CSV inválido

Resultado esperado:
Sistema exibe erro controlado.

---

## AC-03 — Estratégias de Investimento

### Critérios
- Estratégias devem executar corretamente
- Estratégias inválidas devem ser bloqueadas

### Teste de Aceitação
Entrada:
Parâmetros válidos e inválidos

Resultado esperado:
Execução correta ou erro tratado.

---

## AC-04 — Métricas

### Critérios
- Sistema deve calcular retorno
- Sistema deve calcular drawdown
- Sistema deve calcular win rate

### Teste de Aceitação
Entrada:
Resultado da simulação

Resultado esperado:
Métricas calculadas corretamente.

---

## AC-05 — Integração e Pipeline

### Critérios
- Testes automatizados devem executar
- Pipeline CI/CD deve finalizar com sucesso

### Teste de Aceitação
Entrada:
Push no repositório

Resultado esperado:
GitHub Actions finaliza sem erros.