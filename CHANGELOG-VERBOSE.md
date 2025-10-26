# Changelog - Modo Verbose e Melhorias de Formatação

## Data: 20/10/2025

### Objetivo
Adicionar funcionalidade de debug detalhado e melhorar a legibilidade dos testes.

### Mudanças Implementadas

#### 1. **Modo Verbose com [DEBUG]**
- Adicionada captura e exibição da saída completa dos comandos quando `--verbose` está ativo
- Marcador `[DEBUG]` em azul para identificar facilmente a saída dos comandos
- Saída indentada (2 espaços) para melhor visualização
- Funciona tanto para comandos com sucesso quanto para falhas

**Antes:**
```bash
[INFO] Executando: oc whoami
[] Verificar usuário atual (whoami)
```

**Depois (com --verbose):**
```bash
[INFO] Executando: oc whoami
[] Verificar usuário atual (whoami)
[DEBUG] Saída do comando:
  admin
```

#### 2. **Espaçamento Automático entre Testes**
- Todos os 30 módulos agora incluem linha em branco após cada `run_test`
- Melhora significativa na legibilidade da saída
- Facilita identificação visual de início/fim de cada teste

**Exemplo:**
```bash
run_test "Verificar usuário atual (whoami)" \
    "oc whoami"
run_test "Verificar token de acesso" \
    "oc whoami -t"
run_test "Verificar contexto atual" \
    "oc whoami --show-context"
```

#### 3. **Atualização da Biblioteca Comum (`tests/lib/common.sh`)**

**Melhorias na função `run_test`:**
- Captura inteligente da saída dos comandos em modo verbose
- Exibição condicional com formatação [DEBUG]
- Mantém compatibilidade com modo normal (sem verbose)
- Adiciona linha em branco ao final de cada teste (sucesso ou falha)

**Código-chave adicionado:**
```bash
if [ "$VERBOSE" -eq 1 ]; then
    # Captura e exibe saída
    output=$(eval "$command" 2>&1)
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log_success "$description"
        if [ -n "$output" ]; then
            echo -e "${BLUE}[DEBUG]${NC} Saída do comando:" | tee -a "$LOG_FILE"
            echo "$output" | sed 's/^/  /' | tee -a "$LOG_FILE"
        fi
    fi
    echo ""  # Linha em branco
fi
```

### Arquivos Modificados

1. **`/lib/common.sh`**
   - Função `run_test` expandida para suportar modo verbose
   - Adicionada lógica de captura e formatação de saída
   - Implementado espaçamento automático

2. **Todos os 30 módulos de teste** (`tests/01-*/test.sh` até `tests/30-*/test.sh`)
   - Adicionadas linhas em branco entre cada `run_test`
   - Formatação consistente em todos os módulos

3. **`tests/README.md`**
   - Documentação da nova funcionalidade verbose
   - Exemplos de uso com [DEBUG]
   - Atualização das boas práticas

### Validação

Testado com sucesso:
```bash
# Modo normal (sem mudanças visíveis de comportamento)
./scripts/test-commands.sh --module 01

# Modo verbose (nova funcionalidade)
./scripts/test-commands.sh --module 01 --verbose

# Todos os módulos com verbose
./scripts/test-commands.sh --verbose
```

### Benefícios

1. **Debug Facilitado:** Agora é possível ver exatamente o que cada comando retorna
2. **Legibilidade:** Espaçamento consistente torna a saída mais fácil de ler
3. **Troubleshooting:** [DEBUG] marca claramente onde procurar informações
4. **Compatibilidade:** Modo normal continua funcionando exatamente como antes
5. **Performance:** Modo verbose só captura saída quando necessário (não impacta modo normal)

### Uso Recomendado

**Para desenvolvimento e debug:**
```bash
./scripts/test-commands.sh --module XX --verbose
```

**Para CI/CD e validação rápida:**
```bash
./scripts/test-commands.sh
```

**Para análise detalhada de problemas:**
```bash
./scripts/test-commands.sh --verbose --stop-on-error --module XX
```

### Detalhes Técnicos

- **Cores mantidas:** Verde (sucesso), Vermelho (erro), Amarelo (skip), Azul (debug)
- **Log file:** Toda saída verbose também é registrada no log
- **Exit codes:** Mantidos inalterados
- **Compatibilidade:** Backward compatible - scripts antigos funcionam sem modificação

### Referências

- Commit: (será adicionado após commit)
- Issue: Melhorias de usabilidade do sistema de testes
- Documentação: `tests/README.md` atualizado com novos exemplos

---

**Nota:** Script temporário `fix-test-spacing.py` foi usado para automatizar o ajuste dos 30 módulos e foi removido após o uso.
