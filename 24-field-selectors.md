# 🔍 Field Selectors e Filtros Avançados

Este documento contém comandos avançados usando field selectors, label selectors e filtros complexos para buscar e filtrar recursos no OpenShift.

---

## 📋 Índice

1. [Field Selectors Básicos](#field-selectors-básicos)
2. [Field Selectors Avançados](#field-selectors-avançados)
3. [Label Selectors](#label-selectors)
4. [Combinação de Filtros](#combinação-de-filtros)
5. [Filtros com GREP e EGREP](#filtros-com-grep-e-egrep)
6. [Ordenação e Paginação](#ordenação-e-paginação)
7. [Storage e PVCs](#storage-e-pvcs)
8. [Permissões](#permissões)

---

## 🎯 Field Selectors Básicos

### Filtrar Pods por Status
```bash
# Pods em execução
oc get pods --field-selector=status.phase=Running

# Pods pendentes
oc get pods --field-selector=status.phase=Pending

# Pods falhados
oc get pods --field-selector=status.phase=Failed

# Pods que NÃO estão rodando
oc get pods --field-selector=status.phase!=Running

# Pods com sucesso (Completed)
oc get pods --field-selector=status.phase=Succeeded
```

### Filtrar por Namespace
```bash
# Recursos em namespace específico
oc get pods --field-selector=metadata.namespace=default

# Pods em múltiplos namespaces (usando grep)
oc get pods -A --field-selector=metadata.namespace=default,metadata.namespace=kube-system
```

### Filtrar Eventos
```bash
# Eventos de warning
oc get events --field-selector type=Warning

# Eventos normais
oc get events --field-selector type=Normal

# Eventos de um recurso específico
oc get events --field-selector involvedObject.name=<pod-name>

# Eventos de um namespace
oc get events --field-selector involvedObject.namespace=<namespace>
```

### Filtrar Nodes
```bash
# Nodes não agendáveis
oc get nodes --field-selector spec.unschedulable=true

# Nodes agendáveis
oc get nodes --field-selector spec.unschedulable=false
```

---

## 🚀 Field Selectors Avançados

### CSR (Certificate Signing Requests)
```bash
# CSRs pendentes
oc get csr --field-selector status.conditions.type=pending

# CSRs aprovados
oc get csr --field-selector status.conditions.type=Approved

# Listar todos os CSRs pendentes (alternativa)
oc get csr | grep Pending
```

### Builds
```bash
# Builds não completos
oc get builds --field-selector status!=Complete

# Builds completos
oc get builds --field-selector status=Complete

# Builds falhados
oc get builds --field-selector status=Failed
```

### Services
```bash
# Services com ClusterIP específico
oc get svc --field-selector spec.clusterIP=10.x.x.x

# Services do tipo LoadBalancer
oc get svc --field-selector spec.type=LoadBalancer

# Services do tipo NodePort
oc get svc --field-selector spec.type=NodePort
```

---

## 🏷️ Label Selectors

### Seleção por Label
```bash
# Pods com label específica
oc get pods -l app=nginx

# Pods com múltiplas labels (AND)
oc get pods -l app=nginx,tier=frontend

# Pods com label existente (qualquer valor)
oc get pods -l app

# Pods SEM uma label específica
oc get pods -l '!app'

# Pods com label em conjunto de valores
oc get pods -l 'env in (dev,qa)'

# Pods com label NÃO em conjunto
oc get pods -l 'env notin (prod)'
```

### Label Selectors Complexos
```bash
# Combinação de labels e operadores
oc get pods -l 'app=nginx,tier!=frontend'

# Labels com operadores de comparação
oc get pods -l 'version>=2.0'

# Labels com regex (usando grep após)
oc get pods --show-labels | grep "app=nginx"
```

### Labels em Diferentes Recursos
```bash
# Deployments por label
oc get deployments -l app=myapp

# Services por label
oc get svc -l app=myapp

# Todos os recursos com label
oc get all -l app=myapp

# Pods de um deployment específico
oc get pods -l deployment=<deployment-name>
```

---

## 🔗 Combinação de Filtros

### Field Selector + Label Selector
```bash
# Pods Running com label específica
oc get pods -l app=nginx --field-selector=status.phase=Running

# Pods em namespace com label
oc get pods -l tier=frontend --field-selector=metadata.namespace=production

# Combinação complexa
oc get pods -l app=myapp,version=v2 --field-selector=status.phase=Running,metadata.namespace=default
```

### Múltiplos Field Selectors
```bash
# Combinar múltiplas condições
oc get pods --field-selector=status.phase=Running,spec.nodeName=<node-name>

# Pods rodando em node específico
oc get pods -A --field-selector=spec.nodeName=worker-1

# Eventos de warning em namespace específico
oc get events --field-selector=type=Warning,involvedObject.namespace=default
```

---

## 🔎 Filtros com GREP e EGREP

### Filtros Básicos com GREP
```bash
# Pods com problemas (não Running ou Completed)
oc get pods -A | egrep -v "Running|Completed"

# Pods com estados de erro específicos
oc get pods -A | grep -E "Error|CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Pending"

# Nodes com problemas
oc get nodes | grep -v "Ready"

# Cluster operators com problemas
oc get co | grep -v "True.*False.*False"
```

### Filtros Complexos com EGREP
```bash
# Múltiplos padrões de erro
oc get pods -A | egrep "Error|Failed|CrashLoop|ImagePull|Pending|Unknown"

# Pods em namespaces específicos
oc get pods -A | egrep "kube-system|openshift-"

# Filtrar por múltiplos status
oc get pods -A | egrep "1/1|2/2|3/3" | egrep -v "Running"
```

### Grep Inverso (excluir padrões)
```bash
# Excluir múltiplos padrões
oc get pods -A | egrep -v "Running|Completed|Succeeded"

# Excluir namespaces do sistema
oc get pods -A | egrep -v "kube-system|kube-public|openshift-"

# Ver apenas pods com problemas
oc get pods -A | egrep -v "Running|Completed" | egrep -v "NAME"
```

---

## 📊 Ordenação e Paginação

### Ordenar por Campos
```bash
# Ordenar eventos por timestamp
oc get events --sort-by='.lastTimestamp'

# Ordenar eventos mais recentes primeiro
oc get events --sort-by='.lastTimestamp' | tac

# Ordenar pods por criação
oc get pods --sort-by='.metadata.creationTimestamp'

# Ordenar nodes por nome
oc get nodes --sort-by='.metadata.name'
```

### Limitar Resultados
```bash
# Primeiros 10 eventos
oc get events --sort-by='.lastTimestamp' | head -10

# Últimos 10 eventos
oc get events --sort-by='.lastTimestamp' | tail -10

# Paginação customizada
oc get pods --chunk-size=50
```

### Ordenar com Sort Unix
```bash
# Ordenar pods por uso de CPU
oc adm top pods --no-headers | sort -k3 -nr

# Ordenar pods por uso de memória
oc adm top pods --no-headers | sort -k4 -hr

# Ordenar nodes por uso de CPU
oc adm top nodes --no-headers | sort -k3 -nr
```

---

## 💡 Padrões Úteis

### Health Checks Rápidos
```bash
# Verificar se há pods com problemas
if oc get pods -A | egrep -v "Running|Completed" | grep -v NAME; then
  echo "⚠️  Pods com problemas encontrados!"
else
  echo "✅ Todos os pods estão OK"
fi

# Verificar CSRs pendentes
if oc get csr | grep -q Pending; then
  echo "⚠️  CSRs pendentes encontrados!"
  oc get csr | grep Pending
else
  echo "✅ Nenhum CSR pendente"
fi

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

# Contar pods por namespace
oc get pods -A --no-headers | awk '{print $1}' | sort | uniq -c

# Contar pods por node
oc get pods -A -o wide --no-headers | awk '{print $8}' | sort | uniq -c

# Contar eventos por tipo
oc get events --no-headers | awk '{print $3}' | sort | uniq -c
```

### Filtros Combinados Complexos
```bash
# Pods não-Running em namespaces específicos
oc get pods -A | egrep "my-app|my-service" | egrep -v "Running|Completed"

# Eventos de warning dos últimos 10 minutos
oc get events --field-selector type=Warning | grep "$(date -d '10 minutes ago' +'%Y-%m-%d')"

# Nodes com alta utilização
oc adm top nodes --no-headers | awk '$3 > 80 {print $1, $3}'

# Pods usando mais de 80% da memória solicitada
oc adm top pods --all-namespaces --no-headers | awk '$4 > 80 {print $1, $2, $4}'
```

---

## 🛠️ Troubleshooting com Filtros

### Encontrar Pods com Problemas Específicos
```bash
# Pods com restart alto
oc get pods -A -o wide | awk '$5 > 5 {print $0}'

# Pods em CrashLoopBackOff
oc get pods -A | grep CrashLoopBackOff

# Pods em ImagePullBackOff
oc get pods -A | grep ImagePullBackOff

# Pods Pending há muito tempo
oc get pods -A --field-selector=status.phase=Pending --sort-by='.metadata.creationTimestamp'
```

### Análise de Recursos
```bash
# PVCs não bound
oc get pvc -A | grep -v Bound

# Services sem endpoints
for svc in $(oc get svc -o name); do
  if [ -z "$(oc get endpoints ${svc##*/} -o jsonpath='{.subsets[*].addresses[*].ip}')" ]; then
    echo "Service sem endpoints: $svc"
  fi
done

# Routes sem host
oc get routes -A -o custom-columns=NAME:.metadata.name,HOST:.spec.host | grep -E "^[^ ]+ *$"
```

---

## 📚 Recursos Adicionais

- **Field Selectors**: https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/
- **Label Selectors**: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
- **GREP Manual**: https://www.gnu.org/software/grep/manual/

---

## 📖 Navegação

- [← Voltar para Comandos Customizados](23-comandos-customizados.md)
- [→ Próximo: Formatação de Output](25-formatacao-output.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
