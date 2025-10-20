# Script de Reorganização de Testes

## Descrição

O script `reorganize-tests.py` reorganiza automaticamente todos os scripts de teste (`tests/*/test.sh`) para que a ordem de execução dos testes corresponda à ordem em que os comandos aparecem nos arquivos markdown correspondentes.

## Por que isso é importante?

- **Consistência**: Os testes seguem a mesma sequência lógica da documentação
- **Manutenibilidade**: Facilita encontrar e atualizar testes específicos
- **Didática**: A ordem de execução reflete o fluxo de aprendizado da documentação

## Como funciona

1. **Extrai comandos do Markdown**: Lê cada arquivo `.md` e identifica todos os comandos `oc` na ordem em que aparecem nos blocos de código bash
2. **Extrai testes do script**: Lê o `test.sh` correspondente e captura todos os blocos `run_test` preservando sua formatação original
3. **Calcula ordem**: Para cada teste, determina sua posição correta baseada na primeira ocorrência do comando no markdown
4. **Reorganiza**: Reconstrói o script com os testes reordenados, mantendo o cabeçalho intacto

## Uso

### Reorganizar todos os módulos

```bash
python3 reorganize-tests.py
```

### Backup automático

O script cria automaticamente backups antes de modificar:
- `test.sh.bak2` - Backup da versão original antes da reorganização

## Algoritmo de Ordenação

Para cada teste, o script:

1. Extrai a palavra-chave principal do comando (ex: `whoami`, `get`, `create`)
2. Procura essa palavra-chave nos comandos extraídos do markdown
3. Atribui um "score" baseado na posição da primeira ocorrência
4. Ordena todos os testes por esse score (menor = aparece antes)
5. Em caso de empate, mantém a ordem original

## Exemplo

### Markdown (01-autenticacao-configuracao.md)
```markdown
### Verificar Autenticação
```bash
oc whoami
oc whoami -t
oc whoami --show-context
```

### Versão do Cliente
```bash
oc version
oc cluster-info
```
```

### Teste ANTES da reorganização
```bash
run_test "Verificar versão" \
    "oc version"
run_test "Ver usuário" \
    "oc whoami"
run_test "Ver token" \
    "oc whoami -t"
```

### Teste DEPOIS da reorganização
```bash
run_test "Ver usuário" \
    "oc whoami"
run_test "Ver token" \
    "oc whoami -t"
run_test "Verificar versão" \
    "oc version"
```

## Preservação de Formato

O script **preserva exatamente** a formatação original dos blocos `run_test`, incluindo:
- Aspas (simples ou duplas)
- Quebras de linha com `\`
- Indentação
- Comentários internos aos comandos
- Escape de caracteres especiais

## Tratamento de Casos Especiais

### Comandos com pipes e redirecionamentos
O script extrai apenas a primeira parte do comando:
```bash
"oc get pods | grep Running"  # Extrai: "get"
"oc describe pod 2>/dev/null" # Extrai: "describe"
```

### Comandos não encontrados
Testes cujos comandos não aparecem no markdown são colocados no final, mantendo sua ordem relativa original.

### Múltiplas ocorrências
Quando um comando aparece várias vezes no markdown, todos os testes relacionados são agrupados pela primeira ocorrência.

## Validação

Após a reorganização, sempre execute:

```bash
# Validar sintaxe bash
for f in tests/*/test.sh; do bash -n "$f" && echo "✅ $f OK"; done

# Executar suite completa
./test-commands.sh
```

## Limitações

- Não reorganiza comandos **dentro** de um mesmo bloco `run_test` (apenas reordena os blocos completos)
- Assume que o formato é `run_test "descrição" \ "comando"`
- Requer que o markdown use blocos de código com ` ```bash `

## Troubleshooting

### "Syntax error in test.sh"
Restaure o backup e reporte o problema:
```bash
cp tests/XX-module/test.sh.bak2 tests/XX-module/test.sh
```

### "Comando not found in markdown"
O teste será colocado no final. Verifique se:
1. O comando existe no markdown
2. O formato do comando no teste está correto
3. Não há typos no nome do comando

## Manutenção

### Adicionar suporte para novo padrão de comando

Edite a função `extract_command_keyword()` em `reorganize-tests.py`:

```python
def extract_command_keyword(command: str) -> str:
    # Adicione lógica para extrair palavra-chave
    # do seu novo padrão de comando
    pass
```

### Melhorar matching de comandos

Edite a função `calculate_command_order_score()` para ajustar como os comandos são comparados.

## Changelog

### Versão 2.0 (Atual)
- Preservação completa da formatação original
- Melhor tratamento de aspas e strings complexas
- Backup automático com `.bak2`
- Suporte para comandos multi-linha

### Versão 1.0 (Depreciada)
- Primeira versão com problemas de parsing de strings
- Não preservava formatação original

---

**Última atualização**: Outubro 2025
**Autor**: Automation team
**Status**: Produção
