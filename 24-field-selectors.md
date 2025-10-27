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
**Listar pods filtrados por campo específico**

```bash
oc get pods --field-selector=status.phase=Running
```

**Listar pods em estado Pending (aguardando)**

```bash
oc get pods --field-selector=status.phase=Pending
```

**Listar pods que falharam**

```bash
oc get pods --field-selector=status.phase=Failed
```

**Listar pods que não estão em estado Running**

```bash
oc get pods --field-selector=status.phase!=Running
```

**Listar pods filtrados por campo específico**

```bash
oc get pods --field-selector=status.phase=Succeeded
```

### Filtrar por Namespace
**Listar pods filtrados por campo específico**

```bash
oc get pods --field-selector=metadata.namespace=default
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A --field-selector=metadata.namespace=default,metadata.namespace=kube-system
```

### Filtrar Eventos
**Listar apenas eventos do tipo Warning**

```bash
oc get events --field-selector type=Warning
```

**Listar eventos filtrados por campo específico**

```bash
oc get events --field-selector type=Normal
```

**Eventos de um recurso específico**

```bash ignore-test
oc get events --field-selector involvedObject.name=<pod-name>
```

**Eventos de um namespace**

```bash ignore-test
oc get events --field-selector involvedObject.namespace=<namespace>
```

### Filtrar Nodes
**Listar nodes filtrados por campo específico**

```bash
oc get nodes --field-selector spec.unschedulable=true
```

**Listar nodes filtrados por campo específico**

```bash
oc get nodes --field-selector spec.unschedulable=false
```

---

## Field Selectors Avançados

### CSR (Certificate Signing Requests)
**CSRs pendentes**

```bash ignore-test
oc get csr | grep -i Pending
```

**Listar Certificate Signing Requests pendentes**

```bash
oc get csr
```

**Listar todos os CSRs pendentes (alternativa)**

```bash ignore-test
oc get csr | grep Pending
```

### Builds
**Listar recurso filtrados por campo específico**

```bash
oc get builds --field-selector status!=Complete
```

**Listar recurso filtrados por campo específico**

```bash
oc get builds --field-selector status=Complete
```

**Listar recurso filtrados por campo específico**

```bash
oc get builds --field-selector status=Failed
```

### Services
**Exibir service em formato JSON**

```bash
oc get svc -o jsonpath="{range .items[?(@.spec.type=='LoadBalancer')]}{.metadata.name}{'\n'}{end}"
```

**Exibir service em formato JSON**

```bash
oc get svc -o jsonpath="{range .items[?(@.spec.type=='NodePort')]}{.metadata.name}{'\n'}{end}"
```

---

## Label Selectors

### Seleção por Label
**Listar pods filtrados por label**

```bash
oc get pods -l app=nginx
```

**Listar pods filtrados por label**

```bash
oc get pods -l app=nginx,tier=frontend
```

**Listar pods filtrados por label**

```bash
oc get pods -l app
```

**Listar pods filtrados por label**

```bash
oc get pods -l '!app'
```

**Listar pods filtrados por label**

```bash
oc get pods -l 'env in (dev,qa)'
```

**Listar pods filtrados por label**

```bash
oc get pods -l 'env notin (prod)'
```

### Label Selectors Complexos
**Listar pods filtrados por label**

```bash
oc get pods -l 'deployment=test-app,tier!=frontend'
```

**Listar pods filtrados por label**

```bash
oc get pods -l 'deployment=test-app'
```

**Listar pods exibindo todas as labels**

```bash
oc get pods --show-labels | grep "deployment=test-app"
```

### Labels em Diferentes Recursos
**Listar deployments filtrados por label**

```bash
oc get deployments -l app=test-app
```

**Listar service filtrados por label**

```bash
oc get svc -l app=test-app
```

**Listar recurso filtrados por label**

```bash
oc get all -l app=test-app
```

**Listar pods filtrados por label**

```bash
oc get pods -l deployment=test-app
```

---

## Combinação de Filtros

### Field Selector + Label Selector
**Listar pods filtrados por campo específico**

```bash
oc get pods -l app=nginx --field-selector=status.phase=Running
```

**Listar pods filtrados por campo específico**

```bash
oc get pods -l tier=frontend --field-selector=metadata.namespace=production
```

**Listar pods filtrados por campo específico**

```bash
oc get pods -l app=test-app,version=v2 --field-selector=status.phase=Running,metadata.namespace=default
```

### Múltiplos Field Selectors
**Combinar múltiplas condições**

```bash ignore-test
oc get pods --field-selector=status.phase=Running,spec.nodeName=<node-name>
```

**Listar pods de todos os namespaces do cluster**

```bash ignore-test
oc get pods -A --field-selector=spec.nodeName=worker-1
```

**Listar apenas eventos do tipo Warning**

```bash
oc get events --field-selector=type=Warning,involvedObject.namespace=development
```

---

## Filtros com GREP 

### Filtros Básicos com GREP
**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep -E -v "Running|Completed"
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep -E "Error|CrashLoopBackOff|ImagePullBackOff|ErrImagePull|Pending"
```

**Nodes com problemas**

```bash
oc get nodes | grep -v "Ready"
```

**Cluster operators com problemas**

```bash
oc get co | grep -v "True.*False.*False"
```

### Filtros Complexos com grep
**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep -E "Error|Failed|CrashLoop|ImagePull|Pending|Unknown"
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep -E "kube-system|openshift-"
```

### Grep Inverso (excluir padrões)
**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep -E -v "Running|Completed|Succeeded"
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep -E -v "kube-system|kube-public|openshift-"
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep -E -v "Running|Completed" | grep -E -v "NAME"
```

---

## Ordenação e Paginação

### Ordenar por Campos
**Listar eventos ordenados por campo específico**

```bash
oc get events --sort-by='.lastTimestamp'
```

**Listar eventos ordenados por campo específico**

```bash
oc get events --sort-by='.lastTimestamp' | tac
```

**Listar pods ordenados por campo específico**

```bash
oc get pods --sort-by='.metadata.creationTimestamp'
```

**Listar nodes ordenados por campo específico**

```bash
oc get nodes --sort-by='.metadata.name'
```

### Limitar Resultados
**Listar eventos ordenados por campo específico**

```bash
oc get events --sort-by='.lastTimestamp' | head -10
```

**Listar eventos ordenados por campo específico**

```bash
oc get events --sort-by='.lastTimestamp' | tail -10
```

**Paginação customizada**

```bash
oc get pods --chunk-size=50
```

### Ordenar com Sort Unix
**Ordenar pods por uso de CPU**

```bash
oc adm top pods --no-headers | sort -k3 -nr
```

**Ordenar pods por uso de memória**

```bash
oc adm top pods --no-headers | sort -k4 -hr
```

**Ordenar nodes por uso de CPU**

```bash
oc adm top nodes --no-headers | sort -k3 -nr
```

---

## Padrões Úteis

### Health Checks Rápidos
**Listar recurso de todos os namespaces do cluster**

```bash ignore-test
if oc get pods -A | grep -E -v "Running|Completed" | grep -v NAME; then
  echo "  Pods com problemas encontrados!"
else
  echo " Todos os pods estão OK"
fi
```

**Verificar CSRs pendentes**

```bash ignore-test
if oc get csr | grep -q Pending; then
  echo "  CSRs pendentes encontrados!"
  oc get csr | grep Pending
else
  echo " Nenhum CSR pendente"
fi
```

**Verificar cluster operators**

```bash ignore-test
if oc get co | grep -v "True.*False.*False" | grep -v NAME; then
  echo "  Cluster Operators com problemas!"
  oc get co | grep -v "True.*False.*False" | grep -v NAME
else
  echo " Todos os Cluster Operators estão OK"
fi
```

### Contadores
**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A --no-headers | awk '{print $4}' | sort | uniq -c
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A --no-headers | awk '{print $1}' | sort | uniq -c
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A -o wide --no-headers | awk '{print $8}' | sort | uniq -c
```

**Contar eventos por tipo**

```bash
oc get events --no-headers | awk '{print $3}' | sort | uniq -c
```

### Filtros Combinados Complexos
**Listar pods de todos os namespaces do cluster**

```bash ignore-test
oc get pods -A | grep -E "my-app|my-service" | grep -E -v "Running|Completed"
```

**Nodes com alta utilização de CPU**

```bash
oc adm top nodes --no-headers | awk 'int($3) > 80 {print $1, $3}'
```

**Pods usando mais de 80% da memória solicitada**

```bash
oc adm top pods -A --no-headers | awk 'int($4) > 80 {print $1, $2, $4}'
```

---

## Troubleshooting com Filtros

### Encontrar Pods com Problemas Específicos
**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A -o wide | awk '$5 > 5 {print $0}'
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep CrashLoopBackOff
```

```bash ignore-tests
# Pods em ImagePullBackOff
oc get pods -A | grep ImagePullBackOff
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A --field-selector=status.phase=Pending --sort-by='.metadata.creationTimestamp'
```

### Análise de Recursos
**Listar persistent volume claim de todos os namespaces do cluster**

```bash
oc get pvc -A | grep -v Bound
```

**Services sem endpoints**

```bash ignore-test
for svc in $(oc get svc -o name); do
  if [ -z "$(oc get endpoints ${svc##*/} -o jsonpath='{.subsets[*].addresses[*].ip}')" ]; then
    echo "Service sem endpoints: $svc"
  fi
done
```

**Listar routes de todos os namespaces do cluster**

```bash ignore-test
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
