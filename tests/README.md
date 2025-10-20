# Scripts de Teste Modulares

Este diretório contém os scripts de teste automatizados para validar todos os comandos OpenShift documentados.

## 📁 Estrutura

```
tests/
├── lib/
│   └── common.sh              # Biblioteca compartilhada de funções
├── 01-autenticacao-configuracao/
│   └── test.sh                # Testes de autenticação
├── 02-projetos/
│   └── test.sh                # Testes de projetos
├── 03-aplicacoes/
│   └── test.sh                # Testes de aplicações
...
└── 30-operators-operandos/
    └── test.sh                # Testes de operators
```

## 🚀 Uso

### Executar todos os testes

```bash
./test-commands.sh
```

### Executar módulo específico

```bash
./test-commands.sh --module 01    # Apenas autenticação
./test-commands.sh --module 15    # Apenas troubleshooting storage
```

### Opções disponíveis

```bash
./test-commands.sh --help

Opções:
  --verbose          Mostra saída detalhada de cada comando com [DEBUG]
  --stop-on-error    Para no primeiro erro encontrado
  --skip-destructive Pula comandos destrutivos (padrão)
  --skip-cleanup     Mantém projeto de teste após execução
  --module <num>     Executa apenas módulo específico
```

## 🔄 Persistência de Projeto de Teste

### Como funciona

O sistema **persiste o projeto de teste** entre execuções usando um arquivo de estado em `/tmp/oc-test-project-state`.

**Benefícios:**
- ✅ Execute módulos individuais sem recriar o projeto
- ✅ Reutilize recursos criados em testes anteriores
- ✅ Economize tempo em execuções sequenciais
- ✅ Debug mais fácil com projeto persistente

### Fluxo de trabalho recomendado

#### 1️⃣ Primeira execução (criar projeto)
```bash
# Executar com --skip-cleanup para manter o projeto
./test-commands.sh --module 01 --skip-cleanup
```

#### 2️⃣ Execuções subsequentes (reutilizar projeto)
```bash
# Os próximos módulos reutilizarão o projeto automaticamente
./test-commands.sh --module 02 --skip-cleanup
./test-commands.sh --module 03 --skip-cleanup
./test-commands.sh --module 04 --skip-cleanup
```

#### 3️⃣ Verificar status do projeto
```bash
# Ver informações sobre o projeto de teste ativo
./tests/show-test-project.sh
```

Saída esperada:
```
╔════════════════════════════════════════════════════════════════╗
║     Status do Projeto de Teste OpenShift                      ║
╚════════════════════════════════════════════════════════════════╝

[✓] Projeto de teste ativo: test-validation-1729458123

[INFO] Detalhes do projeto:
NAME                         DISPLAY NAME   STATUS
test-validation-1729458123                  Active

[INFO] Recursos no projeto:
NAME                     READY   STATUS    RESTARTS   AGE
pod/test-app-1-abc123    1/1     Running   0          5m

NAME               TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)
service/test-app   ClusterIP   172.30.1.123   <none>        8080/TCP

[INFO] Estatísticas:
  - Deployments: 1
  - Services: 1
  - Routes: 1
  - ConfigMaps: 2
  - Secrets: 3
  - PVCs: 0
```

#### 4️⃣ Limpar quando terminar
```bash
# Remover projeto de teste e limpar estado
./tests/cleanup-test-project.sh
```

### Scripts utilitários

#### `tests/show-test-project.sh`
Mostra status detalhado do projeto de teste ativo:
- Nome do projeto
- Recursos criados
- Estatísticas de objetos
- Localização do arquivo de estado

```bash
./tests/show-test-project.sh
```

#### `tests/cleanup-test-project.sh`
Remove o projeto de teste e limpa arquivos de estado:
- Deleta o projeto do cluster
- Remove arquivo de estado `/tmp/oc-test-project-state`
- Limpa arquivos temporários

```bash
./tests/cleanup-test-project.sh
```

### Comportamento automático

| Cenário | Comportamento |
|---------|---------------|
| **Primeira execução** | Cria novo projeto `test-validation-TIMESTAMP` |
| **Projeto existe em estado** | Reutiliza projeto existente |
| **Projeto foi deletado** | Cria novo projeto automaticamente |
| **Execução sem `--skip-cleanup`** | Remove projeto e limpa estado ao final |
| **Execução com `--skip-cleanup`** | Mantém projeto e estado para próxima execução |

### Arquivo de estado

Localização: `/tmp/oc-test-project-state`

Conteúdo:
```bash
TEST_PROJECT=test-validation-1729458123
```

Este arquivo é automaticamente:
- ✅ Criado quando um projeto é criado/detectado
- ✅ Lido por todos os módulos de teste
- ✅ Validado (verifica se projeto ainda existe)
- ✅ Removido na limpeza completa

### Modo Verbose (Debug)

Quando `--verbose` está ativo, além dos status dos testes, você verá:
- O comando exato sendo executado
- A saída completa do comando marcada com **[DEBUG]**
- Maior espaçamento entre os testes para melhor legibilidade

Exemplo:
```bash
[INFO] Executando: oc whoami
[✓] Verificar usuário atual (whoami)
[DEBUG] Saída do comando:
  admin

[INFO] Executando: oc whoami -t
[✓] Verificar token de acesso
[DEBUG] Saída do comando:
  sha256~FPLu2dixF_cAeDzu73l0oDG3kI083_4DEh0JwC4VZYw
```

## 📝 Estrutura de um Módulo

Cada módulo de teste segue este padrão:

```bash
#!/bin/bash

# Source da biblioteca comum
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

section_header "01 - AUTENTICAÇÃO E CONFIGURAÇÃO"
run_test "Descrição do teste" \
    "comando-oc a executar"
run_test "Outro teste" \
    "outro comando" \
    1  # 1 = skip este teste (opcional)
```

**Nota:** Os testes são automaticamente espaçados com uma linha em branco entre cada `run_test` para melhor legibilidade.

## 🔧 Manutenção

### Adicionar novo teste a um módulo existente

1. Edite o arquivo `tests/XX-nome-modulo/test.sh`
2. Adicione o novo teste usando `run_test`
3. Execute o teste: `./test-commands.sh --module XX`

### Criar novo módulo de teste

1. Crie o diretório: `mkdir tests/31-novo-modulo`
2. Crie o script: `touch tests/31-novo-modulo/test.sh`
3. Use o template acima para estruturar o teste
4. Torne executável: `chmod +x tests/31-novo-modulo/test.sh`

### Regenerar todos os módulos do script antigo

Se você modificou o `test-commands-old.sh` e quer regerar todos os módulos:

```bash
python3 generate-test-modules.py
```

## 📊 Logs e Relatórios

Os logs são salvos em:
- `test-commands-YYYYMMDD-HHMMSS.log` - Log completo de cada execução

## 🐛 Troubleshooting

### Teste falhando

1. Execute apenas o módulo específico com `--verbose` para ver a saída completa dos comandos:
   ```bash
   ./test-commands.sh --module XX --verbose
   ```

2. Verifique o log detalhado com marcadores **[DEBUG]** para identificar o problema

3. Execute o comando manualmente para debug:
   ```bash
   oc <comando-que-falhou>
   ```

### Projeto de teste não é criado

Verifique se você tem permissões para criar projetos:
```bash
oc auth can-i create pods
```

### Módulos não reutilizam o mesmo projeto

**Sintoma:** Cada módulo cria um projeto novo mesmo com `--skip-cleanup`

**Solução:**
```bash
# Verificar se o arquivo de estado existe
ls -la /tmp/oc-test-project-state

# Se não existir, criar manualmente ou executar módulo 01
./test-commands.sh --module 01 --skip-cleanup

# Verificar status
./tests/show-test-project.sh
```

### Projeto órfão (estado existe mas projeto não)

**Sintoma:** `show-test-project.sh` mostra que projeto não existe

**Solução:**
```bash
# Limpar estado órfão
./tests/cleanup-test-project.sh

# Ou manualmente
rm /tmp/oc-test-project-state

# Criar novo projeto
./test-commands.sh --module 01 --skip-cleanup
```

### Múltiplos projetos de teste no cluster

**Sintoma:** Vários projetos `test-validation-*` existem

**Solução:**
```bash
# Listar todos os projetos de teste
oc get projects -l test-validation=true

# Deletar todos
oc delete projects -l test-validation=true

# Limpar estado local
rm /tmp/oc-test-project-state
```

### Variáveis não são compartilhadas entre módulos

A biblioteca `common.sh` usa dois arquivos de estado:
- `/tmp/oc-test-state-$$` - Contadores de testes (por execução)
- `/tmp/oc-test-project-state` - Projeto de teste (persistente)

Se houver problemas, verifique se os arquivos existem durante a execução.

## 💡 Boas Práticas

1. **Sempre teste localmente** antes de commitar mudanças
2. **Use comandos idempotentes** sempre que possível
3. **Adicione tratamento de erros** com `|| true` quando apropriado
4. **Documente testes complexos** com comentários inline
5. **Mantenha os testes rápidos** - evite sleeps longos desnecessários

## 🔄 Integração Contínua

Os scripts podem ser integrados em pipelines CI/CD:

```yaml
# Exemplo GitLab CI
test:
  script:
    - oc login $OPENSHIFT_URL --token=$OPENSHIFT_TOKEN
    - ./test-commands.sh
  artifacts:
    paths:
      - test-commands-*.log
    when: always
```

## 📚 Referências

- Documentação principal: `../README.md`
- Comandos individuais: `../01-autenticacao-configuracao.md` até `../30-operators-operandos.md`
- Copilot instructions: `../.github/copilot-instructions.md`
