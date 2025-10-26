# Pods e Containers

Este documento contém comandos para gerenciar pods e containers no OpenShift.

---

## Índice

1. [Listagem e Informações](#listagem-e-informações)
2. [Gerenciamento de Pods](#gerenciamento-de-pods)
3. [Interação com Pods](#interação-com-pods)
4. [Debug e Troubleshooting](#debug-e-troubleshooting)
5. [Logs](#logs)
6. [Monitoramento e Eventos](#monitoramento-e-eventos)
---

## Listagem e Informações


## Gerenciamento de Pods

### Criar e Deletar

```bash
# Criar ou atualizar um pod usando um yaml
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  securityContext:
    runAsUser: 1000
  containers:
  - name: my-container
    image: registry.access.redhat.com/ubi9:latest
    command: ["/bin/sh"]
    args: ["-c", "sleep infinity"]
    resources:
      requests:
        cpu: "500m"
        memory: "100Mi"
      limits:
        cpu: 1
        memory: 1Gi
EOF
```

```bash ignore-test
# Aplicar mudanças em pod
oc apply -f pod.yaml
```

```bash ignore-test
# Deletar um pod
# oc delete pod <resource-name>
oc delete pod my-pod
```

```bash ignore-test
# Deletar pod forçadamente
# oc delete pod <resource-name>pod --grace-period=0 --force
oc delete pod my-pod --grace-period=0 --force
```

```bash
# Deletar todos os pods com label
oc delete pods -l app=test-app
```

### Listar Pods
```bash
# Listar todos os pods
oc get pods
```

```bash
# Listar pods em todos os namespaces
oc get pods -A
```

```bash
# Listar pods com mais detalhes
oc get pods -o wide
```

```bash
# Listar pods com labels
oc get pods --show-labels
```

```bash
# Listar pods por seletor
oc get pods -l app=test-app
```

```bash
# Listar pods em um projeto específico
# oc get pods -n <namespace>
oc get pods -n development
```

```bash
# Listar pods com status customizado
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP
```

```bash
# Descrever um pod
# oc describe pod <resource-name>
oc describe pod my-pod
```

```bash
# Ver definição YAML do pod
# oc get pod <resource-name>pod -o yaml
oc get pod my-pod -o yaml
```

```bash
# Ver definição JSON do pod
# oc get pod <resource-name>pod -o json
oc get pod my-pod -o json
```

```bash
# Ver apenas o status
# oc get pod <resource-name>pod -o jsonpath='{.status.phase}'
oc get pod my-pod -o jsonpath='{.status.phase}'
```

```bash
# Esperar um pod ficar running
oc wait --for=condition=Ready pod/my-pod
```

---

## Interação com Pods

### Acessar Shell
```bash ignore-test
# Acessar shell de um pod
oc rsh my-pod
```

```bash ignore-test
# Executar comando em um pod
oc exec my-pod -- <comando>
```

```bash
# Executar comando interativo
oc exec -it my-pod -- /bin/date
```

```bash
# Executar comando em container específico
# oc exec my-pod -c <container-name> -- /bin/date
oc exec my-pod -c my-container -- /bin/date
```

```bash ignore-test
# Exemplo prático
oc exec -it mypod -- /bin/sh
```

### Copiar Arquivos
```bash ignore-test
# Copiar arquivo para o pod
oc cp <arquivo-local> my-pod:<caminho-no-pod>
```

```bash ignore-test
# Copiar arquivo do pod
oc cp my-pod:<caminho-no-pod> <arquivo-local>
```

```bash ignore-test
# Copiar diretório
oc cp /local/dir my-pod:/container/dir
```

```bash ignore-test
# Copiar diretório com rsync (precisa ter rsync instalado no pod)
oc rsync /local/dir my-pod:/container/dir
```

```bash ignore-test
# Exemplo
oc cp ./config.json mypod:/etc/config/config.json
```

---

### Reiniciar Pods
```bash
# Reiniciar pods de um deployment
# oc rollout restart <resource-name>/test-app
oc rollout restart deployment/test-app
```

```bash ignore-test
# Deletar pod para forçar recriação
# oc delete pod <resource-name>
oc delete pod my-pod
```

```bash
# Scale down deployment test-app
# oc scale deployment <deployment-name> --replicas=0
oc scale deployment test-app --replicas=0
```
```bash
# Scale up deployment test-app
# oc scale deployment <deployment-name> --replicas=2
oc scale deployment test-app --replicas=2
```
---

## Debug e Troubleshooting

### Debug Interativo
```bash ignore-test
# Debug interativo de pod
oc debug pod/my-pod
```

```bash ignore-test
# Debug com imagem customizada
oc debug pod/my-pod-debug --image=nicolaka/netshoot
```

```bash
# Criar pod de debug temporário e imprima o hostname
oc run debug-pod --image=nicolaka/netshoot -it --rm --restart=Never -- hostname
```

```bash ignore-test
# Criar pod de debug temporário e conecte
oc run debug-pod --image=nicolaka/netshoot -it --rm --restart=Never -- sh
```

### Verificações
```bash
# Ver pods com problemas
oc get pods --field-selector=status.phase!=Running
```

```bash
# Ver pods pendentes
oc get pods --field-selector=status.phase=Pending
```

```bash
# Ver pods falhados
oc get pods --field-selector=status.phase=Failed
```

```bash
# Ver motivo de erro do pod
# oc describe pod <resource-name> | grep -A 10 "Events:"
oc describe pod my-pod | grep -A 10 "Events:"
```

---

## Logs

### Ver Logs
```bash ignore-test
# Ver logs de um pod
oc logs my-pod
```

```bash ignore-test
# Ver logs em tempo real
oc logs -f my-pod
```

```bash ignore-test
# Ver logs de container específico
# oc logs my-pod -c <container-name>
oc logs my-pod -c my-container
```

```bash ignore-test
# Ver logs anteriores (pod crasheado)
oc logs my-pod --previous
```

```bash ignore-test
# Ver últimas N linhas dos logs
oc logs my-pod --tail=<numero>
```

```bash ignore-test
# Ver logs desde timestamp específico
oc logs my-pod --since=1h
```

```bash
# Ver logs de todos os pods com label
oc logs -l app=test-app
```

## Monitoramento e Eventos

### Ver Eventos
```bash
# Ver eventos ordenados por timestamp
oc get events --sort-by='.lastTimestamp'
```

```bash
# Em namespace específico
oc get events -n development --sort-by='.lastTimestamp'
```

```bash
# Últimos 10 eventos
oc get events -n development --sort-by='.lastTimestamp' | head -10
```


## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/pods" target="_blank">Nodes - Working with pods</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/containers" target="_blank">Nodes - Working with containers</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications" target="_blank">Building applications</a>

---

## Navegação

- [← Anterior: Aplicações](03-aplicacoes.md)
- [→ Próximo: Deployments e Scaling](05-deployments-scaling.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
