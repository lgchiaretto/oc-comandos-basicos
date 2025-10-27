# Guia Rápido de Início - OpenShift

Este é um guia rápido para você começar a usar os comandos do OpenShift imediatamente!

---

## Top 20 Comandos Mais Usados

### 1. Login e Contexto
**Login no cluster**
**Ver usuário atual**
**Ver projeto atual**

```bash
oc login <url> -u <usuario> -p <senha>

oc whoami

oc project
```

### 2. Listar Recursos
**Listar pods**
**Listar tudo**
**Listar pods com problemas**

```bash
oc get pods

oc get all

oc get pods -A | grep -E -v "Running|Completed"
```

### 3. Debug de Pods
**Ver logs**
**Logs em tempo real**
**Logs de pod crasheado**
**Acessar shell do pod**

```bash
oc logs <pod-name>

oc logs -f <pod-name>

oc logs <pod-name> --previous

oc rsh <pod-name>
```

### 4. Descrever Recursos
**Descrever pod**
**Ver eventos**

```bash
oc describe pod <pod-name>

oc get events --sort-by='.lastTimestamp' | tail -20
```

### 5. Cluster Operators
**Ver status dos operators**
**Operators com problemas**

```bash
oc get co

oc get co | grep -v "True.*False.*False"
```

### 6. Upgrade do Cluster
**Ver versão atual e status do upgrade**
**Ver progresso do upgrade**
**Ver se há operadores bloqueando upgrade**

```bash
oc get clusterversion

oc adm upgrade

oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Upgradeable" and .status=="False")) | .metadata.name'
```

### 7. Nodes
**Listar nodes**
**Ver uso de recursos dos nodes**

```bash
oc get nodes

oc adm top nodes
```

### 8. CSR (Certificate Signing Requests)
**Listar CSRs**
**Aprovar todos os CSRs pendentes**

```bash
oc get csr

oc get csr -o name | xargs oc adm certificate approve
```

### 9. Scaling
**Escalar deployment**
**Ver status do rollout**

```bash
oc scale deployment test-app --replicas=3

oc rollout status deployment/test-app
```

### 10. Criar Aplicação
**Criar app a partir de imagem**
**Criar app a partir de git**
**Expor service**

```bash
oc new-app <imagem>

oc new-app <url-git>

oc expose service test-app
```

### 10. ConfigMaps e Secrets
**Criar configmap**
**Criar secret**

```bash
oc create configmap test-app --from-literal=key=value

oc create secret generic test-app --from-literal=key=value
```

---

## Comandos de Emergência

### Troubleshooting Rápido
**Health check completo do cluster**
**Must-gather para suporte**

```bash
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

oc adm must-gather --dest-dir=/tmp/must-gather-$(date +%Y%m%d-%H%M%S)
```

### Resolver CSRs Pendentes
**Aprovar todos de uma vez**

```bash
oc get csr -o name | xargs oc adm certificate approve
```

### Cordon e Drain de Node
**Tornar node não agendável**
**Drenar pods do node**
**Voltar a agendar no node**

```bash
oc adm cordon <node-name>

oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data

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

---

## Fluxos de Trabalho Comuns

### Deploy de Nova Aplicação
**1. Criar projeto**
**2. Criar aplicação**
**3. Expor service**
**4. Ver status**
**5. Ver logs**

```bash
oc new-project development

oc new-app <imagem-ou-git>

oc expose service test-app

oc status

oc logs -f deployment/test-app
```

### Debug de Pod com Problema
**1. Identificar o problema**
**2. Descrever o pod**
**3. Ver logs**
**4. Se crasheado, ver logs anteriores**
**5. Ver eventos**
**6. Se necessário, debug interativo**

```bash
oc get pods | grep -v Running

oc describe pod <pod-name>

oc logs <pod-name>

oc logs <pod-name> --previous

oc get events --field-selector involvedObject.name=<pod-name>

oc debug pod/<pod-name>
```

### Manutenção de Node
**1. Cordon (não agendar novos pods)**
**2. Drain (remover pods existentes)**
**3. Realizar manutenção...**
* 4. Uncordon (voltar a agendar)
**5. Verificar**

```bash
oc adm cordon <node-name>

oc adm drain <node-name> --ignore-daemonsets --delete-emptydir-data


oc adm uncordon <node-name>

oc get nodes
```

---

## Ferramentas Complementares

### JQ - Processar JSON
**Instalar**
**Exemplo de uso**

```bash
sudo dnf install jq  # RHEL/Fedora

oc get pods -o json | jq '.items[].metadata.name'
```

### Watch - Monitorar mudanças
**Ver pods em tempo real**
**Ver nodes em tempo real**

```bash
watch -n 2 oc get pods

watch -n 5 oc get nodes
```

### Bash Completion
**Habilitar completion**
**Recarregar shell**

```bash
oc completion bash > oc && sudo mv oc /etc/bash_completion.d/oc

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
**Ver ajuda do comando**
**Ver exemplos**
**Explicar recurso da API**

```bash
oc <comando> --help

oc <comando> --help | grep -A 5 "Examples:"

oc explain <recurso>
```

### Erro de permissão?
**Verificar suas permissões**
**Ver todas as permissões**

```bash
oc auth can-i <verbo> <recurso>

oc auth can-i --list
```

### Não encontra o pod?
**Listar em todos os namespaces**
**Buscar por nome parcial**

```bash
oc get pods -A

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
