# Pods e Containers

Este documento contém comandos para gerenciar pods e containers no OpenShift.

---

## Índice

- [Pods e Containers](#pods-e-containers)
  - [Índice](#índice)
  - [Listagem e Informações](#listagem-e-informações)
  - [Gerenciamento de Pods](#gerenciamento-de-pods)
    - [Criar e Deletar](#criar-e-deletar)
    - [Listar Pods](#listar-pods)
  - [Interação com Pods](#interação-com-pods)
    - [Acessar Shell](#acessar-shell)
    - [Copiar Arquivos](#copiar-arquivos)
    - [Reiniciar Pods](#reiniciar-pods)
  - [Debug e Troubleshooting](#debug-e-troubleshooting)
    - [Debug Interativo](#debug-interativo)
    - [Verificações](#verificações)
  - [Logs](#logs)
    - [Ver Logs](#ver-logs)
  - [Monitoramento e Eventos](#monitoramento-e-eventos)
    - [Ver Eventos](#ver-eventos)
  - [Documentação Oficial](#documentação-oficial)
  - [Navegação](#navegação)
---

## Listagem e Informações


## Gerenciamento de Pods

### Criar e Deletar

```bash
# Aplicar configuração do arquivo YAML/JSON ao cluster
# Essa imagem é uma copia da docker.io/nicolaka/netshoot
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
    image: quay.io/chiaretto/netshoot:latest
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
# Aplicar configuração do arquivo YAML/JSON ao cluster
oc apply -f pod.yaml
```

```bash ignore-test
# Deletar o recurso especificado
# oc delete pod <resource-name>
oc delete pod my-pod
```

```bash ignore-test
# Deletar recurso forçadamente (sem período de espera)
# oc delete pod <resource-name>pod --grace-period=0 --force
oc delete pod my-pod --grace-period=0 --force
```

```bash
# Deletar pods que correspondem ao seletor de label
oc delete pods -l app=test-app
```

### Listar Pods
```bash
# Listar todos os pods do namespace atual
oc get pods
```

```bash
# Listar todos os pods de todos os namespaces do cluster
oc get pods -A
```

```bash
# Listar pods com informações adicionais (node, IP, etc)
oc get pods -o wide
```

```bash
# Listar pods mostrando todas as labels associadas
oc get pods --show-labels
```

```bash
# Listar pods filtrados por label
oc get pods -l app=test-app
```

```bash
# Listar pods em um projeto específico
# oc get pods -n <namespace>
oc get pods -n development
```

```bash
# Listar pods com colunas customizadas
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP
```

```bash
# Exibir detalhes completos do recurso
# oc describe pod <resource-name>
oc describe pod my-pod
```

```bash
# Exibir recurso "my-pod" em formato YAML
# oc get pod <resource-name>pod -o yaml
oc get pod my-pod -o yaml
```

```bash
# Exibir recurso "my-pod" em formato JSON
# oc get pod <resource-name>pod -o json
oc get pod my-pod -o json
```

```bash
# Exibir recurso "my-pod" em formato JSON
# oc get pod <resource-name>pod -o jsonpath='{.status.phase}'
oc get pod my-pod -o jsonpath='{.status.phase}'
```

```bash
# Aguardar pod ficar no estado Ready
# oc wait --for=condition=Ready pod/<pod-name>
oc wait --for=condition=Ready pod/my-pod
```

---

## Interação com Pods

### Acessar Shell
```bash ignore-test
# Abrir shell interativo dentro do pod
oc rsh my-pod
```

```bash ignore-test
# Executar comando em um pod
oc exec my-pod -- <comando>
```

```bash
# Executar comando interativo dentro do pod
oc exec -it my-pod -- /bin/date
```

```bash
# Executar comando em container específico do pod
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
# Copiar arquivo/diretório da máquina local para o pod
oc cp /local/dir my-pod:/container/dir
```

```bash ignore-test
# Sincronizar diretórios entre máquina local e pod (requer rsync no pod)
oc rsync /local/dir my-pod:/container/dir
```

```bash ignore-test
# Exemplo
oc cp ./config.json mypod:/etc/config/config.json
```

---

### Reiniciar Pods
```bash
# Reiniciar deployment (recria todos os pods)
# oc rollout restart <resource-name>/test-app
oc rollout restart deployment/test-app
```

```bash ignore-test
# Deletar o recurso especificado
# oc delete pod <resource-name>
oc delete pod my-pod
```

```bash
# Escalar deployment para zero (parar todos os pods)
# oc scale deployment <deployment-name> --replicas=0
oc scale deployment test-app --replicas=0
```
```bash
# Ajustar número de réplicas do deployment/replicaset
# oc scale deployment <deployment-name> --replicas=2
oc scale deployment test-app --replicas=2
```
---

## Debug e Troubleshooting

### Debug Interativo
```bash ignore-test
# Criar cópia de pod para debug interativo
# oc debug pod/<pod-name>
oc debug pod/my-pod
```

```bash ignore-test
# Criar pod de debug com imagem customizada
# oc debug pod/<pod-name> --image=quay.io/chiaretto/netshoot
oc debug pod/my-pod-debug --image=quay.io/chiaretto/netshoot
```

```bash
# Criar pod temporário interativo (removido ao sair)
oc run debug-pod --image=quay.io/chiaretto/netshoot -it --rm --restart=Never -- hostname
```

```bash ignore-test
# Criar pod temporário interativo (removido ao sair)
oc run debug-pod --image=quay.io/chiaretto/netshoot -it --rm --restart=Never -- sh
```

### Verificações
```bash
# Listar pods que não estão em estado Running
oc get pods --field-selector=status.phase!=Running
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
# Exibir detalhes completos do recurso
# oc describe pod <resource-name> | grep -A 10 "Events:"
oc describe pod my-pod | grep -A 10 "Events:"
```

---

## Logs

### Ver Logs
```bash ignore-test
# Exibir logs do pod especificado
oc logs my-pod
```

```bash ignore-test
# Acompanhar logs em tempo real do pod
oc logs -f my-pod
```

```bash ignore-test
# Exibir logs de container específico do pod
# oc logs my-pod -c <container-name>
oc logs my-pod -c my-container
```

```bash ignore-test
# Exibir logs da instância anterior do container (após crash)
oc logs my-pod --previous
```

```bash ignore-test
# Ver últimas N linhas dos logs
oc logs my-pod --tail=<numero>
```

```bash ignore-test
# Exibir logs a partir de um período de tempo
oc logs my-pod --since=1h
```

```bash
# Exibir logs de todos os pods que correspondem ao label
oc logs -l app=test-app
```

## Monitoramento e Eventos

### Ver Eventos
```bash
# Listar eventos ordenados por campo específico
oc get events --sort-by='.lastTimestamp'
```

```bash
# Listar eventos ordenados por campo específico
oc get events -n development --sort-by='.lastTimestamp'
```

```bash
# Listar eventos ordenados por campo específico
oc get events -n development --sort-by='.lastTimestamp' | head -10
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/working-with-pods">Nodes - Working with pods</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes</a>
---

---

## Navegação

- [← Anterior: Aplicações](03-aplicacoes.md)
- [→ Próximo: Deployments e Scaling](05-deployments-scaling.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
