# 🔍 Field Selectors e Filtros Avançados

Este documento contém comandos avançados usando field selectors, label selectors e filtros complexos para buscar e filtrar recursos no OpenShift.

---

## 📋 Índice

1. [🎯 Field Selectors Básicos](#field-selectors-basicos)
2. [🚀 Field Selectors Avançados](#field-selectors-avancados)
3. [🏷 ️ Label Selectors](#label-selectors)
4. [🔗 Combinação de Filtros](#combinacao-de-filtros)
5. [🔎 Filtros com GREP](#filtros-com-grep)
6. [📊 Ordenação e Paginação](#ordenacao-e-paginacao)
7. [💡 Padrões Úteis](#padroes-uteis)
8. [🛠 ️ Troubleshooting com Filtros](#troubleshooting-com-filtros)
9. [📚 Recursos Adicionais](#recursos-adicionais)
---

## 🎯 Field Selectors Básicos

### Filtrar Pods por Status
```bash
# Pods em execução
oc get pods --field-selector=status.phase=Running
```

```bash
# Pods pendentes
oc get pods --field-selector=status.phase=Pending
```

```bash
# Pods falhados
oc get pods --field-selector=status.phase=Failed
```

```bash
# Pods que NÃO estão rodando
oc get pods --field-selector=status.phase!=Running
```

```bash
# Pods com sucesso (Completed)
oc get pods --field-selector=status.phase=Succeeded
```

### Filtrar por Namespace
```bash
# Recursos em namespace específico
oc get pods --field-selector=metadata.namespace=default
```

```bash
# Pods em múltiplos namespaces (usando grep)
oc get pods -A --field-selector=metadata.namespace=default,metadata.namespace=kube-system
```

### Filtrar Eventos
```bash
# Eventos de warning
oc get events --field-selector type=Warning
```

```bash
# Eventos normais
oc get events --field-selector type=Normal
```

```bash ignore-test
# Eventos de um recurso específico
oc get events --field-selector involvedObject.name=<pod-name>
```

```bash ignore-test
# Eventos de um namespace
oc get events --field-selector involvedObject.namespace=<namespace>
```

### Filtrar Nodes
```bash
# Nodes não agendáveis
oc get nodes --field-selector spec.unschedulable=true
```

```bash
# Nodes agendáveis
oc get nodes --field-selector spec.unschedulable=false
```

---

## 🚀 Field Selectors Avançados

### CSR (Certificate Signing Requests)
```bash ignore-test
# CSRs pendentes
oc get csr | grep -i Pending
```

```bash
# CSRs aprovados
oc get csr
```

```bash ignore-test
# Listar todos os CSRs pendentes (alternativa)
oc get csr | grep Pending
```

### Builds
```bash
# Builds não completos
oc get builds --field-selector status!=Complete
```

```bash
# Builds completos
oc get builds --field-selector status=Complete
```

```bash
# Builds falhados
oc get builds --field-selector status=Failed
```

### Services
```bash
# Services do tipo LoadBalancer
oc get svc -o jsonpath="{range .items[?(@.spec.type=='LoadBalancer')]}{.metadata.name}{'\n'}{end}"
```

```bash
# Services do tipo NodePort
oc get svc -o jsonpath="{range .items[?(@.spec.type=='NodePort')]}{.metadata.name}{'\n'}{end}"
```

---

## 🏷️ Label Selectors

### Seleção por Label
```bash
# Pods com label específica
oc get pods -l app=nginx
```

```bash
# Pods com múltiplas labels (AND)
oc get pods -l app=nginx,tier=frontend
```

```bash
# Pods com label existente (qualquer valor)
oc get pods -l app
```

```bash
# Pods SEM uma label específica
oc get pods -l '!app'
```

```bash
# Pods com label em conjunto de valores
oc get pods -l 'env in (dev,qa)'
```

```bash
# Pods com label NÃO em conjunto
oc get pods -l 'env notin (prod)'
```

### Label Selectors Complexos
```bash
# Combinação de labels e operadores
oc get pods -l 'deployment=test-app,tier!=frontend'
```

```bash
# Labels com operadores de comparação
oc get pods -l 'deployment=test-app'
```

```bash
# Labels com regex (usando grep após)
oc get pods --show-labels | grep "deployment=test-app"
```

### Labels em Diferentes Recursos
```bash
# Deployments por label
oc get deployments -l app=test-app
```

```bash
# Services por label
oc get svc -l app=test-app
```

```bash
# Todos os recursos com label
oc get all -l app=test-app
```

```bash
# Pods de um deployment específico
oc get pods -l deployment=test-app
```

---

## 🔗 Combinação de Filtros

### Field Selector + Label Selector
```bash
# Pods Running com label específica
oc get pods -l app=nginx --field-selector=status.phase=Running
```

```bash
# Pods em namespace com label
oc get pods -l tier=frontend --field-selector=metadata.namespace=production
```

```bash
# Combinação complexa
oc get pods -l app=test-app,version=v2 --field-selector=status.phase=Running,metadata.namespace=default
```

### Múltiplos Field Selectors
```bash ignore-test
# Combinar múltiplas condições
oc get pods --field-selector=status.phase=Running,spec.nodeName=<node-name>
```

```bash ignore-test
# Pods rodando em node específico
oc get pods -A --field-selector=spec.nodeName=worker-1
```

```bash
# Eventos de warning em namespace específico
oc get events --field-selector=type=Warning,involvedObject.namespace=development
```

---

## 🔎 Filtros com GREP 

### Filtros Básicos com GREP
```bash
# Pods com problemas (não Running ou Completed)
oc get pods -A | grep -E -v "Running|Completed"
```

```bash
# Pods com estados de erro específicos
oc get pods -A | grep -E "Error|CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Pending"
```

```bash
# Nodes com problemas
oc get nodes | grep -v "Ready"
```

```bash
# Cluster operators com problemas
oc get co | grep -v "True.*False.*False"
```

### Filtros Complexos com grep
```bash
# Múltiplos padrões de erro
oc get pods -A | grep -E "Error|Failed|CrashLoop|ImagePull|Pending|Unknown"
```

```bash
# Pods em namespaces específicos
oc get pods -A | grep -E "kube-system|openshift-"
```

### Grep Inverso (excluir padrões)
```bash
# Excluir múltiplos padrões
oc get pods -A | grep -E -v "Running|Completed|Succeeded"
```

```bash
# Excluir namespaces do sistema
oc get pods -A | grep -E -v "kube-system|kube-public|openshift-"
```

```bash
# Ver apenas pods com problemas
oc get pods -A | grep -E -v "Running|Completed" | grep -E -v "NAME"
```

---

## 📊 Ordenação e Paginação

### Ordenar por Campos
```bash
# Ordenar eventos por timestamp
oc get events --sort-by='.lastTimestamp'
```

```bash
# Ordenar eventos mais recentes primeiro
oc get events --sort-by='.lastTimestamp' | tac
```

```bash
# Ordenar pods por criação
oc get pods --sort-by='.metadata.creationTimestamp'
```

```bash
# Ordenar nodes por nome
oc get nodes --sort-by='.metadata.name'
```

### Limitar Resultados
```bash
# Primeiros 10 eventos
oc get events --sort-by='.lastTimestamp' | head -10
```

```bash
# Últimos 10 eventos
oc get events --sort-by='.lastTimestamp' | tail -10
```

```bash
# Paginação customizada
oc get pods --chunk-size=50
```

### Ordenar com Sort Unix
```bash
# Ordenar pods por uso de CPU
oc adm top pods --no-headers | sort -k3 -nr
```

```bash
# Ordenar pods por uso de memória
oc adm top pods --no-headers | sort -k4 -hr
```

```bash
# Ordenar nodes por uso de CPU
oc adm top nodes --no-headers | sort -k3 -nr
```

---

## 💡 Padrões Úteis

### Health Checks Rápidos
```bash
# Verificar se há pods com problemas
if oc get pods -A | grep -E -v "Running|Completed" | grep -v NAME; then
  echo "⚠️  Pods com problemas encontrados!"
else
  echo "✅ Todos os pods estão OK"
fi
```

```bash ignore-test
# Verificar CSRs pendentes
if oc get csr | grep -q Pending; then
  echo "⚠️  CSRs pendentes encontrados!"
  oc get csr | grep Pending
else
  echo "✅ Nenhum CSR pendente"
fi
```

```bash
# Verificar cluster operators
if oc get co | grep -v "True.*False.*False" | grep -v NAME; then
  echo "⚠️  Cluster Operators com problemas!"
  oc get co | grep -v "True.*False.*False" | grep -v NAME
else
  echo "✅ Todos os Cluster Operators estão OK"
fi
```

### Contadores
```bash
# Contar pods por estado
oc get pods -A --no-headers | awk '{print $4}' | sort | uniq -c
```

```bash
# Contar pods por namespace
oc get pods -A --no-headers | awk '{print $1}' | sort | uniq -c
```

```bash
# Contar pods por node
oc get pods -A -o wide --no-headers | awk '{print $8}' | sort | uniq -c
```

```bash
# Contar eventos por tipo
oc get events --no-headers | awk '{print $3}' | sort | uniq -c
```

### Filtros Combinados Complexos
```bash ignore-test
# Pods não-Running em namespaces específicos
oc get pods -A | grep -E "my-app|my-service" | grep -E -v "Running|Completed"
```

```bash
# Nodes com alta utilização de CPU
oc adm top nodes --no-headers | awk 'int($3) > 80 {print $1, $3}'
```

```bash
# Pods usando mais de 80% da memória solicitada
oc adm top pods -A --no-headers | awk 'int($4) > 80 {print $1, $2, $4}'
```

---

## 🛠️ Troubleshooting com Filtros

### Encontrar Pods com Problemas Específicos
```bash
# Pods com restart alto
oc get pods -A -o wide | awk '$5 > 5 {print $0}'
```

```bash
# Pods em CrashLoopBackOff
oc get pods -A | grep CrashLoopBackOff
```

```bash ignore-tests
# Pods em ImagePullBackOff
oc get pods -A | grep ImagePullBackOff
```

```bash
# Pods Pending há muito tempo
oc get pods -A --field-selector=status.phase=Pending --sort-by='.metadata.creationTimestamp'
```

### Análise de Recursos
```bash
# PVCs não bound
oc get pvc -A | grep -v Bound
```

```bash ignore-test
# Services sem endpoints
for svc in $(oc get svc -o name); do
  if [ -z "$(oc get endpoints ${svc##*/} -o jsonpath='{.subsets[*].addresses[*].ip}')" ]; then
    echo "Service sem endpoints: $svc"
  fi
done
```

```bash ignore-test
# Routes sem host
oc get routes -A -o custom-columns=NAME:.metadata.name,HOST:.spec.host | grep -E "^[^ ]+ *$"
```

---

## 📚 Recursos Adicionais

- **Field Selectors**: https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/
- **Label Selectors**: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

---


---

## 📚 Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- [CLI Tools](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools)

---

## 📖 Navegação

- [← Voltar para Comandos Customizados](23-comandos-customizados.md)
- [→ Próximo: Formatação de Output](25-formatacao-output.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
