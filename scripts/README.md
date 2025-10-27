# Scripts de Validação e Testes

Este diretório contém os scripts principais para validação e gerenciamento dos testes de comandos sugeridos nesse repositório.

Scripts são destinados exclusivamente ao desenvolvimento deste projeto — não os execute em ambientes de produção nem em clusters que não sejam de desenvolvimento desse projeto.

---

## Arquivos Principais

### `test-commands.sh`
Script principal de validação que executa todos os módulos de teste.

**Uso:**
```bash
./scripts/test-commands.sh [OPÇÕES]
```

**Opções disponíveis:**

| Opção | Descrição |
|-------|-----------|
| `--verbose` | Mostra saída detalhada de cada comando |
| `--stop-on-error` | Para execução no primeiro erro |
| `--cleanup` | Executa limpeza após os testes |
| `--module <num>` | Executa apenas o módulo especificado |
| `--start-module <num>` | Inicia a partir do módulo especificado |
| `--end-module <num>` | Termina no módulo especificado |
| `--help` | Exibe ajuda completa |

---

## Exemplos de Uso

### Executar todos os módulos (01-31)
```bash
./scripts/test-commands.sh
```

### Executar apenas um módulo específico
```bash
./scripts/test-commands.sh --module 05
./scripts/test-commands.sh --module 10
./scripts/test-commands.sh --module 23
```

### Executar a partir de um módulo até o final
```bash
# Executa módulos 10, 11, 12, ... até 30
./scripts/test-commands.sh --start-module 10
```

### Executar até um módulo específico
```bash
# Executa módulos 01, 02, 03, 04, 05
./scripts/test-commands.sh --end-module 05
```

### Executar um RANGE de módulos
```bash
# Executa módulos 01 a 05
./scripts/test-commands.sh --start-module 01 --end-module 05

# Executa módulos 06 a 08
./scripts/test-commands.sh --start-module 06 --end-module 08

# Executa módulos 08 a 30
./scripts/test-commands.sh --start-module 08 --end-module 30
```

### Combinar opções
```bash
# Range com verbose
./scripts/test-commands.sh --start-module 10 --end-module 15 --verbose

# Range com stop-on-error
./scripts/test-commands.sh --start-module 01 --end-module 05 --stop-on-error

# A partir de um módulo com cleanup
./scripts/test-commands.sh --start-module 20 --cleanup
```

---

## Estratégias de Teste por Blocos Temáticos

### Bloco 1 - Essenciais (01-03)
Autenticação, projetos, aplicações
```bash
./scripts/test-commands.sh --start-module 01 --end-module 03
```

### Bloco 2 - Recursos & Workloads (04-06)
Pods, deployments, services, routes
```bash
./scripts/test-commands.sh --start-module 04 --end-module 06
```

### Bloco 3 - Configuração (07-08)
ConfigMaps, Secrets, Storage
```bash
./scripts/test-commands.sh --start-module 07 --end-module 08
```

### Bloco 4 - Build & CI/CD (09-10)
BuildConfigs, ImageStreams, Registry
```bash
./scripts/test-commands.sh --start-module 09 --end-module 10
```

### Bloco 5 - Observabilidade (11-12)
Monitoring, logs, must-gather
```bash
./scripts/test-commands.sh --start-module 11 --end-module 12
```

### Bloco 6 - Troubleshooting (13-15)
Pods, networking, storage issues
```bash
./scripts/test-commands.sh --start-module 13 --end-module 15
```

### Bloco 7 - Segurança & RBAC (16-18)
Permissions, groups, SCC
```bash
./scripts/test-commands.sh --start-module 16 --end-module 18
```

### Bloco 8 - Admin Avançado (19-22)
Cluster operators, nodes, certificates, networking
```bash
./scripts/test-commands.sh --start-module 19 --end-module 22
```

### Bloco 9 - Utilitários (23-26)
Custom commands, field selectors, formatting, templates
```bash
./scripts/test-commands.sh --start-module 23 --end-module 26
```

### Bloco 10 - Operações (27-31)
Backup/restore, patching, jobs, operators
```bash
./scripts/test-commands.sh --start-module 27 --end-module 30
```

---

## Execução Rápida em 3 Etapas

### 1. Testar os essenciais primeiro
```bash
./scripts/test-commands.sh --start-module 01 --end-module 05
```

### 2. Depois, recursos avançados
```bash
./scripts/test-commands.sh --start-module 06 --end-module 15
```

### 3. Por fim, administração
```bash
./scripts/test-commands.sh --start-module 16 --end-module 30
```

---

## Outros Scripts

### `cleanup-test-project.sh`
Remove projetos de teste criados durante a validação.

```bash
./scripts/cleanup-test-project.sh
```

### `generate-all-tests.py`
Gera automaticamente módulos de teste a partir da documentação markdown.

```bash
python3 scripts/generate-all-tests.py [--verbose]
```

**Opções:**
- `--verbose` ou `-v`: Mostra informações detalhadas durante a geração

### `improve-comments.py`
Melhora automaticamente os comentários dos comandos bash nos arquivos markdown.

```bash
python3 scripts/improve-comments.py
```

**O que faz:**
- Analisa todos os arquivos `.md` (exceto README, ESTRUTURA, INICIO-RAPIDO)
- Melhora comentários genéricos para serem mais descritivos e claros
- Mantém comentários já bem escritos
- Preserva comentários com placeholders (`<>`) e instruções importantes
- Cria backup automático antes de modificar
- Evita duplicatas consecutivas

**Exemplos de melhorias:**

| Antes | Depois |
|-------|--------|
| `# Verificar usuário atual` | `# Exibir o nome do usuário autenticado atualmente` |
| `# Listar pods` | `# Listar todos os pods de todos os namespaces do cluster` (quando usado com `-A`) |
| `# Deletar pod` | `# Deletar recurso forçadamente (sem período de espera)` (quando usado com `--force`) |
| `# Ver logs` | `# Acompanhar logs em tempo real do pod` (quando usado com `-f`) |

**Padrões reconhecidos:**
- Comandos `oc get` com diferentes flags (-A, -o wide, --show-labels, --sort-by, --field-selector)
- Comandos `oc describe`, `oc delete`, `oc create`
- Comandos de logs (`oc logs` com -f, --previous, --tail, --since)
- Comandos de execução (`oc exec`, `oc rsh`, `oc debug`)
- Comandos de deployment (`oc scale`, `oc rollout restart/undo/status/history`)
- Comandos de diagnóstico (`oc adm must-gather`, `oc adm inspect`)
- Comandos de RBAC e permissões (`oc auth can-i`, `oc adm policy`)
- Comandos de routes (`oc expose`, `oc create route`)
- E mais de 50+ outros padrões...

**Comentários preservados:**
- Comentários longos (>50 caracteres) com palavras-chave como "importante", "cuidado", "atenção", "note", "obs", "analise"
- Comentários com placeholders (`<nome-do-pod>`, `<namespace>`, etc.)
- Comentários que começam com "Exemplo"
- Comentários técnicos descritivos

**Execução:**
```bash
# Melhorar todos os arquivos markdown
python3 scripts/improve-comments.py

# Ver mudanças
git diff

# Reverter se necessário
git checkout -- *.md
```

**Saída:**
```
🔧 Melhorando comentários dos comandos bash...

Processando: 01-autenticacao-configuracao.md... ✅ Atualizado
Processando: 02-projetos.md... ✅ Atualizado
Processando: 03-aplicacoes.md... ✅ Atualizado
...

📊 Resumo:
   Total de arquivos processados: 31
   Arquivos modificados: 31
   Arquivos sem mudanças: 0

✨ Comentários melhorados com sucesso!
💡 Revise as mudanças com: git diff
```

### `fix-indexes.py`
Corrige automaticamente os índices (##  Índice) em todos os arquivos markdown.
Gera índice apenas com seções principais (##), ignorando subseções (###).

```bash
python3 scripts/fix-indexes.py [--verbose]
```

**Opções:**
- `--verbose` ou `-v`: Mostra as seções detectadas em cada arquivo

**Características:**
-  Detecta apenas seções de nível 2 (##)
-  Ignora subseções (###)
-  Remove acentos nas âncoras
-  Gera links funcionais automaticamente

### `add-docs-section.py`
Adiciona ou atualiza a seção de Documentação Oficial do OpenShift 4.19 em todos os arquivos markdown.

```bash
python3 scripts/add-docs-section.py [--force]
```

**Opções:**
- `--force` ou `-f`: Sobrescreve seção existente

**Características:**
-  Links contextualizados por tema (2-3 links relevantes por módulo)
-  Documentação oficial da Red Hat OpenShift 4.19
-  Inserção automática antes da navegação
-  Links abrem em nova aba (`target="_blank"`)
-  Links específicos para cada componente (CLI, Nodes, Networking, Storage, Operators, etc.)

### `find-duplicates.py`
Analisa e identifica comandos duplicados entre os arquivos markdown.

```bash
python3 scripts/find-duplicates.py
```

Gera um relatório CSV (`duplicates-report.csv`) com todos os comandos duplicados.

### `analyze-duplicates.py`
Analisa o relatório de duplicados e sugere ações (manter, remover, consolidar).

```bash
python3 scripts/analyze-duplicates.py
```

---

## Regras Importantes

### Não permitido
- Combinar `--module` com `--start-module` ou `--end-module`
- Executar sem autenticação no cluster (`oc login` primeiro)

### Recomendado
- Use `--verbose` para debugar falhas específicas
- Use `--stop-on-error` em ambientes críticos
- Use `--cleanup` para limpar recursos após os testes
- Execute `--start-module 01 --end-module 05` para validação rápida
- Teste módulos individualmente antes de executar suite completa

---

## Relatórios

Após a execução, o script gera:

1. **Relatório de Validação**: Estatísticas de testes (passou/falhou)
2. **Tempo de Execução**: Tempo por módulo e tempo total
3. **Log Completo**: Arquivo em `/tmp/test-commands-YYYYMMDD-HHMMSS.log`

---

## Verificação de Pré-requisitos

Antes de executar, o script verifica:
-  OpenShift CLI (`oc`) instalado
-  Autenticação ativa no cluster
-  Permissões básicas (criar pods)

---

## Exemplos de Output

### Sucesso
```

╔════════════════════════════════════════════════════════════════╗
║                    RELATORIO DE VALIDACAO                      ║
╚════════════════════════════════════════════════════════════════╝

[INFO] Finalizado em Sun Oct 26 10:42:44 PM -03 2025

Total de testes: 830
Passou: 830
Falhou: 0

Taxa de sucesso: 100.00%

```

### Com Range
```
[INFO] Iniciando validação em Thu Oct 23 10:30:00 -03 2025
[INFO] Módulos a serem executados: 5
[INFO] Range: início=01 fim=05
```

---

## Ajuda

Para ver todas as opções disponíveis:
```bash
./scripts/test-commands.sh --help
```

---

**Última atualização**: 23 de outubro de 2025  
**Versão**: 2.0.0 (com suporte a ranges)
