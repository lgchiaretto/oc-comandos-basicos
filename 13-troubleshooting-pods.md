# Troubleshooting de Pods

Este documento contém comandos para diagnosticar problemas com pods no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Diagnóstico Básico](#diagnóstico-básico)
3. [Pods com Problemas](#pods-com-problemas)
4. [Debug de Containers](#debug-de-containers)
5. [Problemas Comuns](#problemas-comuns)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## Diagnóstico Básico

### Verificar Status
**Ação:** Listar todos os pods de todos os namespaces do cluster
```

```bash
oc get pods -A
```

**Ação:** Listar pods de todos os namespaces do cluster
```

```bash
oc get pods -A --field-selector=status.phase!=Running
```

**Ação:** Listar pods de todos os namespaces do cluster
```

```bash
oc get pods -A --field-selector=status.phase=Failed
```

**Ação:** Listar pods em estado Pending (aguardando)
```

```bash
oc get pods --field-selector=status.phase=Pending
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe pod <resource-name>`
```

```bash
oc describe pod my-pod
```

**Ação:** Listar eventos filtrados por campo específico
```

```bash ignore-test
oc get events --field-selector involvedObject.name=my-pod
```

**Ação:** Exibir recurso "my-pod" em formato YAML
**Exemplo:** `oc get pod <resource-name>pod -o yaml`
```

```bash
oc get pod my-pod -o yaml
```

### Verificar Logs
**Ação:** Exibir logs do pod especificado
```

```bash ignore-test
oc logs my-pod
```

**Ação:** Exibir logs de container específico do pod
**Exemplo:** `oc logs my-pod -c <container-name>`
```

```bash ignore-test
oc logs my-pod -c httpd
```

**Ação:** Exibir logs da instância anterior do container (após crash)
```

```bash ignore-test
oc logs my-pod --previous
```

**Ação:** Acompanhar logs em tempo real do pod
```

```bash ignore-test
oc logs -f my-pod
```

**Ação:** Exibir últimas N linhas dos logs
```

```bash ignore-test
oc logs my-pod --tail=100
```

---

## Pods com Problemas

### ImagePullBackOff
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe pod <resource-name> | grep -A 10 Events`
```

```bash ignore-test
oc describe pod my-pod | grep -A 10 Events
```

**Ação:** Listar todas as ImageStreams do projeto
```

```bash
oc get is
```

**Ação:** Tentar pull manual (debug)
```

```bash ignore-test
oc debug node/<node-name> -- chroot /host podman pull <image>
```

**Ação:** Exibir recurso "my-pod" em formato JSON
**Exemplo:** `oc get pod <resource-name>pod -o jsonpath='{.spec.containers[0].image}'`
```

```bash ignore-test
oc get pod my-pod -o jsonpath='{.spec.containers[0].image}'
```

### CrashLoopBackOff
**Ação:** Exibir logs da instância anterior do container (após crash)
```

```bash ignore-test
oc logs my-pod --previous
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe pod <resource-name> | grep -i "exit code"`
```

```bash ignore-test
oc describe pod my-pod | grep -i "exit code"
```

**Ação:** Listar recurso de todos os namespaces do cluster
**Exemplo:** `oc get pod <resource-name>pod -o yaml | grep -A 10 livenessProbe`
```

```bash ignore-test
oc get pod my-pod -o yaml | grep -A 10 livenessProbe
```

**Ação:** Desabilitar probes temporariamente
**Exemplo:** `oc set probe <resource-name>/test-app --liveness --remove`
**Ação:** oc set probe <resource-name>/test-app --readiness --remove
```

```bash
oc set probe deployment/test-app --liveness --remove
oc set probe deployment/test-app --readiness --remove
```

**Ação:** Criar cópia de pod para debug interativo
**Exemplo:** `oc debug deployment/<deployment-name>`
```

```bash ignore-test
oc debug deployment/test-app
```

### Pending (Não Agendado)
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe pod <resource-name> | grep -A 20 Events`
```

```bash ignore-test
oc describe pod my-pod | grep -A 20 Events
```

**Ação:** Listar recurso de todos os namespaces do cluster
**Exemplo:** `oc get pod <resource-name>pod -o yaml | grep -A 5 resources`
```

```bash ignore-test
oc get pod my-pod -o yaml | grep -A 5 resources
```

**Ação:** Ver capacidade dos nodes
**Exemplo:** `oc adm top <resource-name>`
```

```bash
oc adm top nodes
```

**Ação:** Listar todos os nodes do cluster
```

```bash
oc get nodes
```

**Ação:** Exibir recurso "my-pod" em formato YAML
**Exemplo:** `oc get pod <resource-name>pod -o yaml | grep nodeSelector`
```

```bash ignore-test
oc get pod my-pod -o yaml | grep nodeSelector
```

**Ação:** Exibir detalhes completos do nodes
```

```bash
oc describe nodes | grep Taints
```

### OOMKilled
**Ação:** Exibir recurso "my-pod" em formato JSON
**Exemplo:** `oc get pod <resource-name>pod -o jsonpath='{.spec.containers[0].resources.limits.memory}'`
```

```bash
oc get pod my-pod -o jsonpath='{.spec.containers[0].resources.limits.memory}'
```

**Ação:** Ver uso atual
**Exemplo:** `oc adm top <resource-name> my-pod`
```

```bash ignore-test
oc adm top pod my-pod
```

**Ação:** Definir/atualizar requests e limits de recursos
**Exemplo:** `oc set resources <resource-name>/test-app --limits=memory=2Gi`
```

```bash
oc set resources deployment/test-app --limits=memory=2Gi
```

**Ação:** Exibir recurso "my-pod" em formato JSON
**Exemplo:** `oc get pod <resource-name>pod -o jsonpath='{.status.containerStatuses[0].restartCount}'`
```

```bash
oc get pod my-pod -o jsonpath='{.status.containerStatuses[0].restartCount}'
```

**Ação:** Exibir recurso "my-pod" em formato JSON
**Exemplo:** `oc get pod <resource-name>pod -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'`
```

```bash
oc get pod my-pod -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
```

---

## Debug de Containers

### Debug Interativo
**Ação:** Criar cópia de pod para debug interativo
**Exemplo:** `oc debug pod/<pod-name>`
```

```bash ignore-test
oc debug pod/my-pod
```

**Ação:** Criar cópia de pod para debug interativo
**Exemplo:** `oc debug deployment/<deployment-name>`
```

```bash ignore-test
oc debug deployment/test-app
```

**Ação:** Debug de node
```

```bash ignore-test
oc debug node/<node-name>
```

### Executar Comandos
**Ação:** Abrir shell interativo dentro do pod
```

```bash ignore-test
oc rsh my-pod
```

**Ação:** Comando específico
```

```bash ignore-test
oc exec my-pod -- <comando>
```

**Ação:** Em container específico
```

```bash ignore-test
oc exec my-pod -c <container> -- <comando>
```

**Ação:** Verificar conectividade
```

```bash ignore-test
oc exec my-pod -- curl -v <url>
oc exec my-pod -- ping <host>
```

**Ação:** Verificar DNS
```

```bash ignore-test
oc exec my-pod -- nslookup <service>
oc exec my-pod -- cat /etc/resolv.conf
```

**Ação:** Executar comando dentro do pod especificado
```

```bash ignore-test
oc exec my-pod -- df -h
oc exec my-pod -- ls -la /path
```

### Port Forward para Debug
**Ação:** Forward de porta
**Exemplo:** `oc port-forward my-pod <pod-name>:8080`
```

```bash ignore-test
oc port-forward my-pod 8080:8080
```

**Ação:** Múltiplas portas
**Exemplo:** `oc port-forward my-pod <pod-name>:8080 9090:9090`
```

```bash ignore-test
oc port-forward my-pod 8080:8080 9090:9090
```

**Ação:** Em background
**Exemplo:** `oc port-forward my-pod <pod-name>:8080 &`
```

```bash ignore-test
oc port-forward my-pod 8080:8080 &
```

**Ação:** Testar porta
```

```bash
curl http://localhost:8080
```

---

## Problemas Comuns

### Volumes e Mounts
**Ação:** Listar todos os Persistent Volume Claims do namespace
```

```bash
oc get pvc
```

**Ação:** Exibir detalhes completos do persistent volume claim
**Exemplo:** `oc describe pvc <resource-name>`
```

```bash ignore-test
oc describe pvc test-app
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe pod <resource-name> | grep -A 10 Mounts`
```

```bash ignore-test
oc describe pod my-pod | grep -A 10 Mounts
```

**Ação:** Executar comando dentro do pod especificado
```

```bash ignore-test
oc exec my-pod -- ls -la /mount/path
```

### ConfigMaps e Secrets
**Ação:** Exibir configmap "test-app" em formato YAML
**Exemplo:** `oc get cm <configmap-name> -o yaml`
```

```bash
oc get cm test-app -o yaml
```

**Ação:** Exibir secret "test-app" em formato YAML
**Exemplo:** `oc get secret <secret-name> -o yaml`
```

```bash
oc get secret test-app -o yaml
```

**Ação:** Definir/atualizar variáveis de ambiente no recurso
**Exemplo:** `oc set env <resource-name>/test-app --list`
```

```bash ignore-test
oc set env pod/test-app --list
```

**Ação:** Executar comando dentro do pod especificado
```

```bash ignore-test
oc exec my-pod -- env | sort
```

### Network Issues
**Ação:** Listar todos os services do namespace atual
```

```bash
oc get svc
```

**Ação:** Endpoints do service
**Exemplo:** `oc get endpoints <resource-name>`
```

```bash
oc get endpoints test-app
```

**Ação:** Teste de conectividade
```

```bash ignore-test
oc exec my-pod -- curl -v <service-name>:<port>
```

**Ação:** DNS lookup
```

```bash ignore-test
oc exec my-pod -- nslookup <service-name>
```

**Ação:** Exibir recurso "my-pod" em formato JSON
**Exemplo:** `oc get pod <resource-name>pod -o jsonpath='{.status.podIP}'`
```

```bash ignore-test
oc get pod my-pod -o jsonpath='{.status.podIP}'
```

### Permissões e Security
**Ação:** Listar todas as ServiceAccounts do namespace
```

```bash
oc get sa
```

**Ação:** Exibir recurso "my-pod" em formato YAML
**Exemplo:** `oc get pod <resource-name>pod -o yaml | grep scc`
```

```bash ignore-test
oc get pod my-pod -o yaml | grep scc
```

**Ação:** Verificar RBAC
```

```bash ignore-test
oc adm policy who-can <verbo> <recurso>
```

**Ação:** Exibir recurso "my-pod" em formato JSON
**Exemplo:** `oc get pod <resource-name>pod -o jsonpath='{.spec.securityContext.runAsUser}'`
```

```bash ignore-test
oc get pod my-pod -o jsonpath='{.spec.securityContext.runAsUser}'
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support">Support - Troubleshooting</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
---

---

## Navegação

- [← Anterior: Must-Gather](12-must-gather.md)
- [→ Próximo: Troubleshooting de Rede](14-troubleshooting-rede.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
