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
  --verbose          Mostra saída detalhada de cada comando
  --stop-on-error    Para no primeiro erro encontrado
  --skip-destructive Pula comandos destrutivos (padrão)
  --module <num>     Executa apenas módulo específico
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

1. Execute apenas o módulo específico com `--verbose`:
   ```bash
   ./test-commands.sh --module XX --verbose
   ```

2. Verifique o log detalhado para ver o comando exato que falhou

3. Execute o comando manualmente para debug:
   ```bash
   oc <comando-que-falhou>
   ```

### Projeto de teste não é criado

Verifique se você tem permissões para criar projetos:
```bash
oc auth can-i create projects
```

### Variáveis não são compartilhadas entre módulos

A biblioteca `common.sh` usa um arquivo de estado temporário (`/tmp/oc-test-state-$$`) para compartilhar contadores entre módulos. Se houver problemas, verifique se o arquivo existe durante a execução.

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
