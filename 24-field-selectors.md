# Field Selectors e Filtros Avançados

Este documento contém comandos avançados usando field selectors, label selectors e filtros complexos para buscar e filtrar recursos no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Field Selectors Básicos](#field-selectors-básicos)
3. [Field Selectors Avançados](#field-selectors-avançados)
4. [Label Selectors](#label-selectors)
5. [Combinação de Filtros](#combinação-de-filtros)
6. [Filtros com GREP](#filtros-com-grep)
7. [Ordenação e Paginação](#ordenação-e-paginação)
8. [Padrões Úteis](#padrões-úteis)
9. [Troubleshooting com Filtros](#troubleshooting-com-filtros)
10. [Recursos Adicionais](#recursos-adicionais)
11. [Documentação Oficial](#documentação-oficial)
12. [Navegação](#navegação)
---

## Field Selectors Básicos

### Filtrar Pods por Status
```bash
# Listar pods filtrados por campo específico
oc get pods --field-selector=status.phase=Running
```

```bash
# Listar pods em estado Pending (aguardando)
oc get pods --field-selector=status.phase=Pending
```

```bash
# Listar pods que falharam
oc get pods --field-selector=status.phase=Failed
```

```bash
# Listar pods que não estão em estado Running
oc get pods --field-selector=status.phase!=Running
```

```bash
# Listar pods filtrados por campo específico
oc get pods --field-selector=status.phase=Succeeded
```

### Filtrar por Namespace
```bash
# Listar pods filtrados por campo específico
oc get pods --field-selector=metadata.namespace=default
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A --field-selector=metadata.namespace=default,metadata.namespace=kube-system
```

### Filtrar Eventos
```bash
# Listar apenas eventos do tipo Warning
oc get events --field-selector type=Warning
```

```bash
# Listar eventos filtrados por campo específico
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
# Listar nodes filtrados por campo específico
oc get nodes --field-selector spec.unschedulable=true
```

```bash
# Listar nodes filtrados por campo específico
oc get nodes --field-selector spec.unschedulable=false
```

---

## Field Selectors Avançados

### CSR (Certificate Signing Requests)
```bash ignore-test
# CSRs pendentes
oc get csr | grep -i Pending
```

```bash
# Listar Certificate Signing Requests pendentes
oc get csr
```

```bash ignore-test
# Listar todos os CSRs pendentes (alternativa)
oc get csr | grep Pending
```

### Builds
```bash
# Listar recurso filtrados por campo específico
oc get builds --field-selector status!=Complete
```

```bash
# Listar recurso filtrados por campo específico
oc get builds --field-selector status=Complete
```

```bash
# Listar recurso filtrados por campo específico
oc get builds --field-selector status=Failed
```

### Services
```bash
# Exibir service em formato JSON
oc get svc -o jsonpath="{range .items[?(@.spec.type=='LoadBalancer')]}{.metadata.name}{'\n'}{end}"
```

```bash
# Exibir service em formato JSON
oc get svc -o jsonpath="{range .items[?(@.spec.type=='NodePort')]}{.metadata.name}{'\n'}{end}"
```

---

## Label Selectors

### Seleção por Label
```bash
# Listar pods filtrados por label
oc get pods -l app=nginx
```

```bash
# Listar pods filtrados por label
oc get pods -l app=nginx,tier=frontend
```

```bash
# Listar pods filtrados por label
oc get pods -l app
```

```bash
# Listar pods filtrados por label
oc get pods -l '!app'
```

```bash
# Listar pods filtrados por label
oc get pods -l 'env in (dev,qa)'
```

```bash
# Listar pods filtrados por label
oc get pods -l 'env notin (prod)'
```

### Label Selectors Complexos
```bash
# Listar pods filtrados por label
oc get pods -l 'deployment=test-app,tier!=frontend'
```

```bash
# Listar pods filtrados por label
oc get pods -l 'deployment=test-app'
```

```bash
# Listar pods exibindo todas as labels
oc get pods --show-labels | grep "deployment=test-app"
```

### Labels em Diferentes Recursos
```bash
# Listar deployments filtrados por label
oc get deployments -l app=test-app
```

```bash
# Listar service filtrados por label
oc get svc -l app=test-app
```

```bash
# Listar recurso filtrados por label
oc get all -l app=test-app
```

```bash
# Listar pods filtrados por label
oc get pods -l deployment=test-app
```

---

## Combinação de Filtros

### Field Selector + Label Selector
```bash
# Listar pods filtrados por campo específico
oc get pods -l app=nginx --field-selector=status.phase=Running
```

```bash
# Listar pods filtrados por campo específico
oc get pods -l tier=frontend --field-selector=metadata.namespace=production
```

```bash
# Listar pods filtrados por campo específico
oc get pods -l app=test-app,version=v2 --field-selector=status.phase=Running,metadata.namespace=default
```

### Múltiplos Field Selectors
```bash ignore-test
# Combinar múltiplas condições
oc get pods --field-selector=status.phase=Running,spec.nodeName=<node-name>
```

```bash ignore-test
# Listar pods de todos os namespaces do cluster
oc get pods -A --field-selector=spec.nodeName=worker-1
```

```bash
# Listar apenas eventos do tipo Warning
oc get events --field-selector=type=Warning,involvedObject.namespace=development
```

---

## Filtros com GREP 

### Filtros Básicos com GREP
```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep -E -v "Running|Completed"
```

```bash
# Listar pods de todos os namespaces do cluster
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
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep -E "Error|Failed|CrashLoop|ImagePull|Pending|Unknown"
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep -E "kube-system|openshift-"
```

### Grep Inverso (excluir padrões)
```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep -E -v "Running|Completed|Succeeded"
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep -E -v "kube-system|kube-public|openshift-"
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep -E -v "Running|Completed" | grep -E -v "NAME"
```

---

## Ordenação e Paginação

### Ordenar por Campos
```bash
# Listar eventos ordenados por campo específico
oc get events --sort-by='.lastTimestamp'
```

```bash
# Listar eventos ordenados por campo específico
oc get events --sort-by='.lastTimestamp' | tac
```

```bash
# Listar pods ordenados por campo específico
oc get pods --sort-by='.metadata.creationTimestamp'
```

```bash
# Listar nodes ordenados por campo específico
oc get nodes --sort-by='.metadata.name'
```

### Limitar Resultados
```bash
# Listar eventos ordenados por campo específico
oc get events --sort-by='.lastTimestamp' | head -10
```

```bash
# Listar eventos ordenados por campo específico
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

## Padrões Úteis

### Health Checks Rápidos
```bash ignore-test
# Listar recurso de todos os namespaces do cluster
if oc get pods -A | grep -E -v "Running|Completed" | grep -v NAME; then
  echo "  Pods com problemas encontrados!"
else
  echo " Todos os pods estão OK"
fi
```

```bash ignore-test
# Verificar CSRs pendentes
if oc get csr | grep -q Pending; then
  echo "  CSRs pendentes encontrados!"
  oc get csr | grep Pending
else
  echo " Nenhum CSR pendente"
fi
```

```bash ignore-test
# Verificar cluster operators
if oc get co | grep -v "True.*False.*False" | grep -v NAME; then
  echo "  Cluster Operators com problemas!"
  oc get co | grep -v "True.*False.*False" | grep -v NAME
else
  echo " Todos os Cluster Operators estão OK"
fi
```

### Contadores
```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A --no-headers | awk '{print $4}' | sort | uniq -c
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A --no-headers | awk '{print $1}' | sort | uniq -c
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A -o wide --no-headers | awk '{print $8}' | sort | uniq -c
```

```bash
# Contar eventos por tipo
oc get events --no-headers | awk '{print $3}' | sort | uniq -c
```

### Filtros Combinados Complexos
```bash ignore-test
# Listar pods de todos os namespaces do cluster
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

## Troubleshooting com Filtros

### Encontrar Pods com Problemas Específicos
```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A -o wide | awk '$5 > 5 {print $0}'
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A | grep CrashLoopBackOff
```

```bash ignore-tests
# Pods em ImagePullBackOff
oc get pods -A | grep ImagePullBackOff
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -A --field-selector=status.phase=Pending --sort-by='.metadata.creationTimestamp'
```

### Análise de Recursos
```bash
# Listar persistent volume claim de todos os namespaces do cluster
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
# Listar routes de todos os namespaces do cluster
oc get routes -A -o custom-columns=NAME:.metadata.name,HOST:.spec.host | grep -E "^[^ ]+ *$"
```

---

## Recursos Adicionais

- **Field Selectors**: https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/
- **Label Selectors**: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/cli_tools/openshift-cli-oc">CLI Tools - OpenShift CLI (oc)</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
---

---

## Navegação

- [← Voltar para Comandos Customizados](23-comandos-customizados.md)
- [→ Próximo: Formatação de Output](25-output-formatacao.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
