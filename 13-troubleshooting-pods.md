# 🐛 Troubleshooting de Pods

Este documento contém comandos para diagnosticar problemas com pods no OpenShift.

---

## 📋 Índice

1. [Diagnóstico Básico](#diagnóstico-básico)
2. [Pods com Problemas](#pods-com-problemas)
3. [Debug de Containers](#debug-de-containers)
4. [Problemas Comuns](#problemas-comuns)

---

## 🔍 Diagnóstico Básico

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

```bash ignore-test
# Descrever pod
oc describe pod <nome-do-pod>
```

```bash ignore-test
# Ver eventos relacionados
oc get events --field-selector involvedObject.name=<nome-do-pod>
```

```bash ignore-test
# Status detalhado
oc get pod <nome-do-pod> -o yaml
```

### Verificar Logs
```bash ignore-test
# Logs do pod
oc logs <nome-do-pod>
```

```bash ignore-test
# Logs de container específico
oc logs <nome-do-pod> -c httpd
```

```bash ignore-test
# Logs do container anterior (crashado)
oc logs <nome-do-pod> --previous
```

```bash ignore-test
# Seguir logs em tempo real
oc logs -f <nome-do-pod>
```

```bash ignore-test
# Últimas 100 linhas
oc logs <nome-do-pod> --tail=100
```

---

## 🚨 Pods com Problemas

### ImagePullBackOff
```bash ignore-test
# Ver erro de pull
oc describe pod <nome-do-pod> | grep -A 10 Events
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
oc get pod <nome-do-pod> -o jsonpath='{.spec.containers[0].image}'
```

### CrashLoopBackOff
```bash ignore-test
# Ver logs do crash
oc logs <nome-do-pod> --previous
```

```bash ignore-test
# Ver motivo do crash
oc describe pod <nome-do-pod> | grep -i "exit code"
```

```bash ignore-test
# Verificar liveness/readiness probes
oc get pod <nome-do-pod> -o yaml | grep -A 10 livenessProbe
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
oc describe pod <nome-do-pod> | grep -A 20 Events
```

```bash ignore-test
# Verificar resources requests
oc get pod <nome-do-pod> -o yaml | grep -A 5 resources
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
oc get pod <nome-do-pod> -o yaml | grep nodeSelector
```

```bash
# Ver taints nos nodes
oc describe nodes | grep Taints
```

### OOMKilled
```bash ignore-test
# Verificar limite de memória
oc get pod <nome-do-pod> -o jsonpath='{.spec.containers[0].resources.limits.memory}'
```

```bash ignore-test
# Ver uso atual
oc adm top pod <nome-do-pod>
```

```bash
# Aumentar limite de memória
# oc set resources <resource-name>/test-app --limits=memory=2Gi
oc set resources deployment/test-app --limits=memory=2Gi
```

```bash ignore-test
# Ver histórico de restarts
oc get pod <nome-do-pod> -o jsonpath='{.status.containerStatuses[0].restartCount}'
```

```bash ignore-test
# Ver motivo da última terminação
oc get pod <nome-do-pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
```

---

## 🔧 Debug de Containers

### Debug Interativo
```bash ignore-test
# Criar pod de debug
oc debug pod/<nome-do-pod>
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
oc rsh <nome-do-pod>
```

```bash ignore-test
# Comando específico
oc exec <nome-do-pod> -- <comando>
```

```bash ignore-test
# Em container específico
oc exec <nome-do-pod> -c <container> -- <comando>
```

```bash ignore-test
# Verificar conectividade
oc exec <nome-do-pod> -- curl -v <url>
oc exec <nome-do-pod> -- ping <host>
```

```bash ignore-test
# Verificar DNS
oc exec <nome-do-pod> -- nslookup <service>
oc exec <nome-do-pod> -- cat /etc/resolv.conf
```

```bash ignore-test
# Verificar filesystem
oc exec <nome-do-pod> -- df -h
oc exec <nome-do-pod> -- ls -la /path
```

### Port Forward para Debug
```bash ignore-test
# Forward de porta
oc port-forward <nome-do-pod> 8080:8080
```

```bash ignore-test
# Múltiplas portas
oc port-forward <nome-do-pod> 8080:8080 9090:9090
```

```bash ignore-test
# Em background
oc port-forward <nome-do-pod> 8080:8080 &
```

```bash
# Testar porta
curl http://localhost:8080
```

---

## 🩹 Problemas Comuns

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
oc describe pod <nome-do-pod> | grep -A 10 Mounts
```

```bash ignore-test
# Verificar permissões
oc exec <nome-do-pod> -- ls -la /mount/path
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
oc exec <nome-do-pod> -- env | sort
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
oc exec <nome-do-pod> -- curl -v <service-name>:<port>
```

```bash ignore-test
# DNS lookup
oc exec <nome-do-pod> -- nslookup <service-name>
```

```bash ignore-test
# Ver rede do pod
oc get pod <nome-do-pod> -o jsonpath='{.status.podIP}'
```

### Permissões e Security
```bash
# Verificar ServiceAccount
oc get sa
```

```bash ignore-test
# Ver SCC do pod
oc get pod <nome-do-pod> -o yaml | grep scc
```

```bash ignore-test
# Verificar RBAC
oc adm policy who-can <verbo> <recurso>
```

```bash ignore-test
# Ver runAsUser
oc get pod <nome-do-pod> -o jsonpath='{.spec.securityContext.runAsUser}'
```

---

## 📖 Navegação

- [← Anterior: Must-Gather](12-must-gather.md)
- [→ Próximo: Troubleshooting de Rede](14-troubleshooting-rede.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
