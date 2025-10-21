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

```bash
# Descrever pod
oc describe pod <nome-do-pod>
```

```bash
# Ver eventos relacionados
oc get events --field-selector involvedObject.name=<nome-do-pod>
```

```bash
# Status detalhado
oc get pod <nome-do-pod> -o yaml
```

### Verificar Logs
```bash
# Logs do pod
oc logs <nome-do-pod>
```

```bash
# Logs de container específico
oc logs <nome-do-pod> -c <container-name>
```

```bash
# Logs do container anterior (crashado)
oc logs <nome-do-pod> --previous
```

```bash
# Seguir logs em tempo real
oc logs -f <nome-do-pod>
```

```bash
# Últimas 100 linhas
oc logs <nome-do-pod> --tail=100
```

---

## 🚨 Pods com Problemas

### ImagePullBackOff
```bash
# Ver erro de pull
oc describe pod <nome-do-pod> | grep -A 10 Events
```

```bash
# Verificar ImageStream
oc get is
```

```bash
# Verificar secrets de pull
oc get secrets | grep docker
```

```bash
# Tentar pull manual (debug)
oc debug node/<node-name> -- chroot /host podman pull <image>
```

```bash
# Verificar image na spec
oc get pod <nome-do-pod> -o jsonpath='{.spec.containers[0].image}'
```

### CrashLoopBackOff
```bash
# Ver logs do crash
oc logs <nome-do-pod> --previous
```

```bash
# Ver motivo do crash
oc describe pod <nome-do-pod> | grep -i "exit code"
```

```bash
# Verificar liveness/readiness probes
oc get pod <nome-do-pod> -o yaml | grep -A 10 livenessProbe
```

```bash
# Desabilitar probes temporariamente
oc set probe deployment/test-app --liveness --remove
oc set probe deployment/test-app --readiness --remove
```

```bash
# Debug interativo
oc debug deployment/test-app
```

### Pending (Não Agendado)
```bash
# Ver eventos de scheduling
oc describe pod <nome-do-pod> | grep -A 20 Events
```

```bash
# Verificar resources requests
oc get pod <nome-do-pod> -o yaml | grep -A 5 resources
```

```bash
# Ver capacidade dos nodes
oc adm top nodes
```

```bash
# Ver nodes disponíveis
oc get nodes
```

```bash
# Verificar node selectors
oc get pod <nome-do-pod> -o yaml | grep nodeSelector
```

```bash
# Ver taints nos nodes
oc describe nodes | grep Taints
```

### OOMKilled
```bash
# Verificar limite de memória
oc get pod <nome-do-pod> -o jsonpath='{.spec.containers[0].resources.limits.memory}'
```

```bash
# Ver uso atual
oc adm top pod <nome-do-pod>
```

```bash
# Aumentar limite de memória
oc set resources deployment/test-app --limits=memory=2Gi
```

```bash
# Ver histórico de restarts
oc get pod <nome-do-pod> -o jsonpath='{.status.containerStatuses[0].restartCount}'
```

```bash
# Ver motivo da última terminação
oc get pod <nome-do-pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
```

---

## 🔧 Debug de Containers

### Debug Interativo
```bash
# Criar pod de debug
oc debug pod/<nome-do-pod>
```

```bash
# Debug de deployment
oc debug deployment/test-app
```

```bash
# Debug de node
oc debug node/<node-name>
```

```bash
# Com imagem específica
oc debug pod/test-app --image=registry.redhat.io/rhel8/support-tools
```

```bash
# Debug sem iniciar
oc debug pod/test-app --keep-init-containers=true
```

### Executar Comandos
```bash
# Shell no container
oc rsh <nome-do-pod>
```

```bash
# Comando específico
oc exec <nome-do-pod> -- <comando>
```

```bash
# Em container específico
oc exec <nome-do-pod> -c <container> -- <comando>
```

```bash
# Verificar conectividade
oc exec <nome-do-pod> -- curl -v <url>
oc exec <nome-do-pod> -- ping <host>
```

```bash
# Verificar DNS
oc exec <nome-do-pod> -- nslookup <service>
oc exec <nome-do-pod> -- cat /etc/resolv.conf
```

```bash
# Verificar filesystem
oc exec <nome-do-pod> -- df -h
oc exec <nome-do-pod> -- ls -la /path
```

### Port Forward para Debug
```bash
# Forward de porta
oc port-forward <nome-do-pod> 8080:8080
```

```bash
# Múltiplas portas
oc port-forward <nome-do-pod> 8080:8080 9090:9090
```

```bash
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

```bash
# Status do PVC
oc describe pvc <nome-do-pvc>
```

```bash
# Verificar mounts no pod
oc describe pod <nome-do-pod> | grep -A 10 Mounts
```

```bash
# Verificar permissões
oc exec <nome-do-pod> -- ls -la /mount/path
```

### ConfigMaps e Secrets
```bash
# Verificar ConfigMap montado
oc get cm test-app -o yaml
```

```bash
# Verificar Secret
oc get secret test-app -o yaml
```

```bash
# Ver variáveis de ambiente
oc set env pod/test-app --list
```

```bash
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
oc get endpoints test-app
```

```bash
# Teste de conectividade
oc exec <nome-do-pod> -- curl -v <service-name>:<port>
```

```bash
# DNS lookup
oc exec <nome-do-pod> -- nslookup <service-name>
```

```bash
# Ver rede do pod
oc get pod <nome-do-pod> -o jsonpath='{.status.podIP}'
```

### Permissões e Security
```bash
# Verificar ServiceAccount
oc get sa
```

```bash
# Ver SCC do pod
oc get pod <nome-do-pod> -o yaml | grep scc
```

```bash
# Verificar RBAC
oc adm policy who-can <verbo> <recurso>
```

```bash
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
