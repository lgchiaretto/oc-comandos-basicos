# Guia Rápido de Início - OpenShift

Este é um guia rápido para você começar a usar os comandos do OpenShift imediatamente!

---

## Top 20 Comandos Mais Usados

### 1. Login e Contexto
```bash
# Login no cluster
oc login <url> -u <usuario> -p <senha>

# Ver usuário atual
oc whoami

# Ver projeto atual
oc project
```

### 2. Listar Recursos
```bash
# Listar pods
oc get pods

# Listar tudo
oc get all

# Listar pods com problemas
oc get pods -A | grep -E -v "Running|Completed"
```

### 3. Debug de Pods
```bash
# Ver logs
oc logs <pod-name>

# Logs em tempo real
oc logs -f <pod-name>

# Logs de pod crasheado
oc logs <pod-name> --previous

# Acessar shell do pod
oc rsh <pod-name>
```

### 4. Descrever Recursos
```bash
# Descrever pod
oc describe pod <pod-name>

# Ver eventos
oc get events --sort-by='.lastTimestamp' | tail -20
```

### 5. Cluster Operators
```bash
# Ver status dos operators
oc get co

# Operators com problemas
oc get co | grep -v "True.*False.*False"
```

### 6. Nodes
```bash
# Listar nodes
oc get nodes

# Ver uso de recursos dos nodes
oc adm top nodes
```

### 7. CSR (Certificate Signing Requests)
```bash
# Listar CSRs
oc get csr

# Aprovar todos os CSRs pendentes
oc get csr -o name | xargs oc adm certificate approve
```

### 8. Scaling
```bash
# Escalar deployment
oc scale deployment test-app --replicas=3

# Ver status do rollout
oc rollout status deployment/test-app
```

### 9. Criar Aplicação
```bash
# Criar app a partir de imagem
oc new-app <imagem>

# Criar app a partir de git
oc new-app <url-git>

# Expor service
oc expose service test-app
```

### 10. ConfigMaps e Secrets
```bash
# Criar configmap
oc create configmap test-app --from-literal=key=value

# Criar secret
oc create secret generic test-app --from-literal=key=value
```

---

## Comandos de Emergência

### Troubleshooting Rápido
```bash
# Health check completo do cluster
echo "=== Pods com Problemas ===" && \
(oc get pods -A | grep -E -v "Running|Completed" || echo "Nenhum pod com problema") && \
echo "" && \
echo "=== Cluster Operators ===" && \
(oc get co | grep -v "True.*False.*False" || echo "Todos os operators estão saudáveis") && \
echo "" && \
echo "=== CSRs Pendentes ===" && \
(oc get csr | grep Pending || echo "Nenhum CSR pendente") && \
echo "" && \
echo "=== Nodes ===" && \
oc get nodes

# Must-gather para suporte
oc adm must-gather --dest-dir=/tmp/must-gather-$(date +%Y%m%d-%H%M%S)
```

### Resolver CSRs Pendentes
```bash
# Aprovar todos de uma vez
oc get csr -o name | xargs oc adm certificate approve
```

### Cordon e Drain de Node
```bash
# Tornar node não agendável
oc adm cordon <node-name>

# Drenar pods do node
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Voltar a agendar no node
oc adm uncordon <node-name>
```

---

## Onde Encontrar Cada Tipo de Comando

### Para Iniciantes
1. **[README.md](README.md)** - Comece aqui! Índice completo
2. Autenticação e Login (ainda não criado)
3. Projetos e Aplicações (ainda não criado)

### Para Troubleshooting
1. **[23-comandos-customizados.md](23-comandos-customizados.md)** - Scripts e automação
2. **[24-field-selectors.md](24-field-selectors.md)** - Filtros avançados
3. Troubleshooting de Pods (ainda não criado)

### Para Administradores
1. Cluster Operators (ainda não criado)
2. Nodes e Machines (ainda não criado)
3. **[21-csr.md](README.md#21-certificate-signing-requests)** - CSRs

### Referência Completa
- **[comandos-openshift-ORIGINAL-COMPLETO.md](comandos-openshift-ORIGINAL-COMPLETO.md)** - Todos os comandos em um arquivo

---

## Fluxos de Trabalho Comuns

### Deploy de Nova Aplicação
```bash
# 1. Criar projeto
oc new-project development

# 2. Criar aplicação
oc new-app <imagem-ou-git>

# 3. Expor service
oc expose service test-app

# 4. Ver status
oc status

# 5. Ver logs
oc logs -f deployment/test-app
```

### Debug de Pod com Problema
```bash
# 1. Identificar o problema
oc get pods | grep -v Running

# 2. Descrever o pod
oc describe pod <pod-name>

# 3. Ver logs
oc logs <pod-name>

# 4. Se crasheado, ver logs anteriores
oc logs <pod-name> --previous

# 5. Ver eventos
oc get events --field-selector involvedObject.name=<pod-name>

# 6. Se necessário, debug interativo
oc debug pod/<pod-name>
```

### Manutenção de Node
```bash
# 1. Cordon (não agendar novos pods)
oc adm cordon <node-name>

# 2. Drain (remover pods existentes)
oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data

# 3. Realizar manutenção...

# 4. Uncordon (voltar a agendar)
oc adm uncordon <node-name>

# 5. Verificar
oc get nodes
```

---

## Ferramentas Complementares

### JQ - Processar JSON
```bash
# Instalar
sudo dnf install jq  # RHEL/Fedora

# Exemplo de uso
oc get pods -o json | jq '.items[].metadata.name'
```

### Watch - Monitorar mudanças
```bash
# Ver pods em tempo real
watch -n 2 oc get pods

# Ver nodes em tempo real
watch -n 5 oc get nodes
```

### Bash Completion
```bash
# Habilitar completion
oc completion bash > oc && sudo mv oc /etc/bash_completion.d/oc

# Recarregar shell
source ~/.bashrc
```

---

## Próximos Passos

1. **Explore o [README.md](README.md)** - Índice completo com 30 categorias
2. **Leia [ESTRUTURA.md](ESTRUTURA.md)** - Entenda a organização do guia
3. **Pratique os comandos** - Use em ambiente de desenvolvimento
4. **Consulte quando necessário** - Guia de referência rápida

---

## Dicas Importantes

### Segurança
-  Nunca execute comandos `delete` ou `drain` em produção sem ter certeza
-  Sempre teste em ambiente de desenvolvimento primeiro
-  Faça backup antes de mudanças críticas

### Boas Práticas
-  Use `oc describe` antes de deletar recursos
-  Sempre verifique o namespace correto com `oc project`
-  Use `--dry-run=client -o yaml` para ver o que será criado
-  Mantenha aliases organizados e documentados

### Performance
-  Use `--field-selector` para filtrar no servidor
-  Use `-o name` quando só precisar dos nomes
-  Use `--no-headers` em scripts
-  Combine com `grep` e `awk` para processamento local

---

## Ajuda Rápida

### Comando não funciona?
```bash
# Ver ajuda do comando
oc <comando> --help

# Ver exemplos
oc <comando> --help | grep -A 5 "Examples:"

# Explicar recurso da API
oc explain <recurso>
```

### Erro de permissão?
```bash
# Verificar suas permissões
oc auth can-i <verbo> <recurso>

# Ver todas as permissões
oc auth can-i --list
```

### Não encontra o pod?
```bash
# Listar em todos os namespaces
oc get pods -A

# Buscar por nome parcial
oc get pods -A | grep <parte-do-nome>
```

---

## Links Úteis

- **Documentação Oficial**: https://docs.redhat.com/en/documentation/openshift_container_platform/
- **Índice Principal**: [README.md](README.md)
- **Comandos Customizados**: [23-comandos-customizados.md](23-comandos-customizados.md)
- **Field Selectors**: [24-field-selectors.md](24-field-selectors.md)

---

**Última atualização**: Outubro 2025  
**Dica**: Imprima ou salve este guia para consulta rápida!
