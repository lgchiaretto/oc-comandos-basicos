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
```bash
# Listar todos os pods
oc get pods -A
```

```bash
# Pods não Running
oc get pods -A --field-selector=status.phase!=Running
```

```bash
# Pods com erro
oc get pods -A --field-selector=status.phase=Failed
```

```bash
# Pods Pending
oc get pods --field-selector=status.phase=Pending
```

```bash
# Descrever pod
# oc describe pod <resource-name>
oc describe pod my-pod
```

```bash ignore-test
# Ver eventos relacionados
oc get events --field-selector involvedObject.name=my-pod
```

```bash
# Status detalhado
# oc get pod <resource-name>pod -o yaml
oc get pod my-pod -o yaml
```

### Verificar Logs
```bash ignore-test
# Logs do pod
oc logs my-pod
```

```bash ignore-test
# Logs de container específico
# oc logs my-pod -c <container-name>
oc logs my-pod -c httpd
```

```bash ignore-test
# Logs do container anterior (crashado)
oc logs my-pod --previous
```

```bash ignore-test
# Seguir logs em tempo real
oc logs -f my-pod
```

```bash ignore-test
# Últimas 100 linhas
oc logs my-pod --tail=100
```

---

## Pods com Problemas

### ImagePullBackOff
```bash ignore-test
# Ver erro de pull
# oc describe pod <resource-name> | grep -A 10 Events
oc describe pod my-pod | grep -A 10 Events
```

```bash
# Verificar ImageStream
oc get is
```

```bash ignore-test
# Tentar pull manual (debug)
oc debug node/<node-name> -- chroot /host podman pull <image>
```

```bash ignore-test
# Verificar image na spec
# oc get pod <resource-name>pod -o jsonpath='{.spec.containers[0].image}'
oc get pod my-pod -o jsonpath='{.spec.containers[0].image}'
```

### CrashLoopBackOff
```bash ignore-test
# Ver logs do crash
oc logs my-pod --previous
```

```bash ignore-test
# Ver motivo do crash
# oc describe pod <resource-name> | grep -i "exit code"
oc describe pod my-pod | grep -i "exit code"
```

```bash ignore-test
# Verificar liveness/readiness probes
# oc get pod <resource-name>pod -o yaml | grep -A 10 livenessProbe
oc get pod my-pod -o yaml | grep -A 10 livenessProbe
```

```bash
# Desabilitar probes temporariamente
# oc set probe <resource-name>/test-app --liveness --remove
oc set probe deployment/test-app --liveness --remove
# oc set probe <resource-name>/test-app --readiness --remove
oc set probe deployment/test-app --readiness --remove
```

```bash ignore-test
# Debug interativo
oc debug deployment/test-app
```

### Pending (Não Agendado)
```bash ignore-test
# Ver eventos de scheduling
# oc describe pod <resource-name> | grep -A 20 Events
oc describe pod my-pod | grep -A 20 Events
```

```bash ignore-test
# Verificar resources requests
# oc get pod <resource-name>pod -o yaml | grep -A 5 resources
oc get pod my-pod -o yaml | grep -A 5 resources
```

```bash
# Ver capacidade dos nodes
# oc adm top <resource-name>
oc adm top nodes
```

```bash
# Ver nodes disponíveis
oc get nodes
```

```bash ignore-test
# Verificar node selectors
# oc get pod <resource-name>pod -o yaml | grep nodeSelector
oc get pod my-pod -o yaml | grep nodeSelector
```

```bash
# Ver taints nos nodes
oc describe nodes | grep Taints
```

### OOMKilled
```bash ignore-test
# Verificar limite de memória
# oc get pod <resource-name>pod -o jsonpath='{.spec.containers[0].resources.limits.memory}'
oc get pod my-pod -o jsonpath='{.spec.containers[0].resources.limits.memory}'
```

```bash ignore-test
# Ver uso atual
# oc adm top <resource-name> my-pod
oc adm top pod my-pod
```

```bash
# Aumentar limite de memória
# oc set resources <resource-name>/test-app --limits=memory=2Gi
oc set resources deployment/test-app --limits=memory=2Gi
```

```bash ignore-test
# Ver histórico de restarts
# oc get pod <resource-name>pod -o jsonpath='{.status.containerStatuses[0].restartCount}'
oc get pod my-pod -o jsonpath='{.status.containerStatuses[0].restartCount}'
```

```bash ignore-test
# Ver motivo da última terminação
# oc get pod <resource-name>pod -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
oc get pod my-pod -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
```

---

## Debug de Containers

### Debug Interativo
```bash ignore-test
# Criar pod de debug
oc debug pod/my-pod
```

```bash ignore-test
# Debug de deployment
oc debug deployment/test-app
```

```bash ignore-test
# Debug de node
oc debug node/<node-name>
```

### Executar Comandos
```bash ignore-test
# Shell no container
oc rsh my-pod
```

```bash ignore-test
# Comando específico
oc exec my-pod -- <comando>
```

```bash ignore-test
# Em container específico
oc exec my-pod -c <container> -- <comando>
```

```bash ignore-test
# Verificar conectividade
oc exec my-pod -- curl -v <url>
oc exec my-pod -- ping <host>
```

```bash ignore-test
# Verificar DNS
oc exec my-pod -- nslookup <service>
oc exec my-pod -- cat /etc/resolv.conf
```

```bash ignore-test
# Verificar filesystem
oc exec my-pod -- df -h
oc exec my-pod -- ls -la /path
```

### Port Forward para Debug
```bash ignore-test
# Forward de porta
oc port-forward my-pod 8080:8080
```

```bash ignore-test
# Múltiplas portas
oc port-forward my-pod 8080:8080 9090:9090
```

```bash ignore-test
# Em background
oc port-forward my-pod 8080:8080 &
```

```bash
# Testar porta
curl http://localhost:8080
```

---

## Problemas Comuns

### Volumes e Mounts
```bash
# Verificar PVC
oc get pvc
```

```bash ignore-test
# Status do PVC
# oc describe pvc test-app
# oc describe pvc <resource-name>
oc describe pvc test-app
```

```bash ignore-test
# Verificar mounts no pod
# oc describe pod <resource-name> | grep -A 10 Mounts
oc describe pod my-pod | grep -A 10 Mounts
```

```bash ignore-test
# Verificar permissões
oc exec my-pod -- ls -la /mount/path
```

### ConfigMaps e Secrets
```bash
# Verificar ConfigMap montado
# oc get cm <configmap-name> -o yaml
oc get cm test-app -o yaml
```

```bash
# Verificar Secret
# oc get secret <secret-name> -o yaml
oc get secret test-app -o yaml
```

```bash ignore-test
# Ver variáveis de ambiente
# oc set env <resource-name>/test-app --list
oc set env pod/test-app --list
```

```bash ignore-test
# Verificar dentro do pod
oc exec my-pod -- env | sort
```

### Network Issues
```bash
# Verificar service
oc get svc
```

```bash
# Endpoints do service
# oc get endpoints <resource-name>
oc get endpoints test-app
```

```bash ignore-test
# Teste de conectividade
oc exec my-pod -- curl -v <service-name>:<port>
```

```bash ignore-test
# DNS lookup
oc exec my-pod -- nslookup <service-name>
```

```bash ignore-test
# Ver rede do pod
# oc get pod <resource-name>pod -o jsonpath='{.status.podIP}'
oc get pod my-pod -o jsonpath='{.status.podIP}'
```

### Permissões e Security
```bash
# Verificar ServiceAccount
oc get sa
```

```bash ignore-test
# Ver SCC do pod
# oc get pod <resource-name>pod -o yaml | grep scc
oc get pod my-pod -o yaml | grep scc
```

```bash ignore-test
# Verificar RBAC
oc adm policy who-can <verbo> <recurso>
```

```bash ignore-test
# Ver runAsUser
# oc get pod <resource-name>pod -o jsonpath='{.spec.securityContext.runAsUser}'
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
