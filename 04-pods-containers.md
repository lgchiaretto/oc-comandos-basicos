# Pods e Containers

Este documento contém comandos para gerenciar pods e containers no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Listagem e Informações](#listagem-e-informações)
3. [Gerenciamento de Pods](#gerenciamento-de-pods)
4. [Interação com Pods](#interação-com-pods)
5. [Debug e Troubleshooting](#debug-e-troubleshooting)
6. [Logs](#logs)
7. [Monitoramento e Eventos](#monitoramento-e-eventos)
8. [Documentação Oficial](#documentação-oficial)
9. [Navegação](#navegação)
---

## Listagem e Informações


## Gerenciamento de Pods

### Criar e Deletar

**Aplicar configuração do arquivo YAML/JSON ao cluster**
* Essa imagem é uma copia da docker.io/nicolaka/netshoot

```bash
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

**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
oc apply -f pod.yaml
```

**Deletar o pod especificado**

```bash ignore-test
oc delete pod my-pod
```

**Deletar recurso forçadamente (sem período de espera)**

```bash ignore-test
oc delete pod my-pod --grace-period=0 --force
```

**Deletar pods que correspondem ao seletor de label**

```bash
oc delete pods -l app=test-app
```

### Listar Pods
**Listar todos os pods do namespace atual**

```bash
oc get pods
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A
```

**Listar pods com informações adicionais (node, IP, etc)**

```bash
oc get pods -o wide
```

**Listar pods mostrando todas as labels associadas**

```bash
oc get pods --show-labels
```

**Listar pods filtrados por label**

```bash
oc get pods -l app=test-app
```

**Listar pods em um projeto específico**

```bash
oc get pods -n development
```

**Listar pods com colunas customizadas**

```bash
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP
```

**Exibir detalhes completos do pod**

```bash
oc describe pod my-pod
```

**Exibir pod em formato YAML completo**

```bash
oc get pod my-pod -o yaml
```

**Exibir configuração completa do pod em formato JSON**

```bash
oc get pod my-pod -o json
```

**Exibir status/fase atual do pod**

```bash
oc get pod my-pod -o jsonpath='{.status.phase}'
```

**Aguardar pod ficar no estado Ready**

```bash
oc wait --for=condition=Ready pod/my-pod
```

---

## Interação com Pods

### Acessar Shell
**Abrir shell interativo dentro do pod**

```bash ignore-test
oc rsh my-pod
```

**Executar comando dentro do pod especificado**

```bash ignore-test
oc exec my-pod -- <comando>
```

**Executar comando dentro do pod especificado**

```bash
oc exec -it my-pod -- /bin/date
```

**Executar comando em container específico do pod**

```bash
oc exec my-pod -c my-container -- /bin/date
```

**Exemplo prático**

```bash ignore-test
oc exec -it mypod -- /bin/sh
```

### Copiar Arquivos
**Copiar arquivo para o pod**

```bash ignore-test
oc cp <arquivo-local> my-pod:<caminho-no-pod>
```

**Copiar arquivo do pod**

```bash ignore-test
oc cp my-pod:<caminho-no-pod> <arquivo-local>
```

**Copiar arquivo/diretório da máquina local para o pod**

```bash ignore-test
oc cp /local/dir my-pod:/container/dir
```

**Sincronizar diretórios entre máquina local e pod (requer rsync no pod)**

```bash ignore-test
oc rsync /local/dir my-pod:/container/dir
```

**Exemplo**

```bash ignore-test
oc cp ./config.json mypod:/etc/config/config.json
```

---

### Reiniciar Pods
**Reiniciar deployment (recria todos os pods)**

```bash
oc rollout restart deployment/test-app
```

**Deletar o pod especificado**

```bash ignore-test
oc delete pod my-pod
```

**Escalar deployment para zero (parar todos os pods)**

```bash
oc scale deployment test-app --replicas=0
```
**Ajustar número de réplicas do deployment/replicaset**

```bash
oc scale deployment test-app --replicas=2
```
---

## Debug e Troubleshooting

### Debug Interativo
**Criar cópia de pod para debug interativo**

```bash ignore-test
oc debug pod/my-pod
```

**Criar pod de debug com imagem customizada**

```bash ignore-test
oc debug pod/my-pod-debug --image=quay.io/chiaretto/netshoot
```

**Criar pod temporário interativo (removido ao sair)**

```bash
oc run debug-pod --image=quay.io/chiaretto/netshoot -it --rm --restart=Never -- hostname
```

**Criar pod temporário interativo (removido ao sair)**

```bash ignore-test
oc run debug-pod --image=quay.io/chiaretto/netshoot -it --rm --restart=Never -- sh
```

### Verificações
**Listar pods que não estão em estado Running**

```bash
oc get pods --field-selector=status.phase!=Running
```

**Listar pods em estado Pending (aguardando)**

```bash
oc get pods --field-selector=status.phase=Pending
```

**Listar pods que falharam**

```bash
oc get pods --field-selector=status.phase=Failed
```

**Exibir detalhes completos do pod filtrando por Events:**

```bash
oc describe pod my-pod | grep -A 10 "Events:"
```

---

## Logs

### Ver Logs
**Exibir logs do pod especificado**

```bash ignore-test
oc logs my-pod
```

**Acompanhar logs em tempo real do pod**

```bash ignore-test
oc logs -f my-pod
```

**Exibir logs de container específico do pod**

```bash ignore-test
oc logs my-pod -c my-container
```

**Exibir logs da instância anterior do container (após crash)**

```bash ignore-test
oc logs my-pod --previous
```

**Ver últimas N linhas dos logs**

```bash ignore-test
oc logs my-pod --tail=<numero>
```

**Exibir logs a partir de um período de tempo**

```bash ignore-test
oc logs my-pod --since=1h
```

**Exibir logs de todos os pods que correspondem ao label**

```bash
oc logs -l app=test-app
```

## Monitoramento e Eventos

### Ver Eventos
**Listar eventos ordenados por campo específico**

```bash
oc get events --sort-by='.lastTimestamp'
```

**Listar eventos ordenados por campo específico**

```bash
oc get events -n development --sort-by='.lastTimestamp'
```

**Listar eventos ordenados por campo específico**

```bash
oc get events -n development --sort-by='.lastTimestamp' | head -10
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes/working-with-pods">Nodes - Working with pods</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes</a>
---


## Navegação

- [← Anterior: Aplicações](03-aplicacoes.md)
- [→ Próximo: Deployments e Scaling](05-deployments-scaling.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Novembro 2025
