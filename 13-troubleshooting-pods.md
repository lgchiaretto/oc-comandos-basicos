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

# Pods não Running
oc get pods -A --field-selector=status.phase!=Running

# Pods com erro
oc get pods -A --field-selector=status.phase=Failed

# Pods Pending
oc get pods --field-selector=status.phase=Pending

# Descrever pod
oc describe pod <nome-do-pod>

# Ver eventos relacionados
oc get events --field-selector involvedObject.name=<nome-do-pod>

# Status detalhado
oc get pod <nome-do-pod> -o yaml
```

### Verificar Logs
```bash
# Logs do pod
oc logs <nome-do-pod>

# Logs de container específico
oc logs <nome-do-pod> -c <container-name>

# Logs do container anterior (crashado)
oc logs <nome-do-pod> --previous

# Seguir logs em tempo real
oc logs -f <nome-do-pod>

# Últimas 100 linhas
oc logs <nome-do-pod> --tail=100
```

---

## 🚨 Pods com Problemas

### ImagePullBackOff
```bash
# Ver erro de pull
oc describe pod <nome-do-pod> | grep -A 10 Events

# Verificar ImageStream
oc get is

# Verificar secrets de pull
oc get secrets | grep docker

# Tentar pull manual (debug)
oc debug node/<node-name> -- chroot /host podman pull <image>

# Verificar image na spec
oc get pod <nome-do-pod> -o jsonpath='{.spec.containers[0].image}'
```

### CrashLoopBackOff
```bash
# Ver logs do crash
oc logs <nome-do-pod> --previous

# Ver motivo do crash
oc describe pod <nome-do-pod> | grep -i "exit code"

# Verificar liveness/readiness probes
oc get pod <nome-do-pod> -o yaml | grep -A 10 livenessProbe

# Desabilitar probes temporariamente
oc set probe deployment/<nome> --liveness --remove
oc set probe deployment/<nome> --readiness --remove

# Debug interativo
oc debug deployment/<nome>
```

### Pending (Não Agendado)
```bash
# Ver eventos de scheduling
oc describe pod <nome-do-pod> | grep -A 20 Events

# Verificar resources requests
oc get pod <nome-do-pod> -o yaml | grep -A 5 resources

# Ver capacidade dos nodes
oc adm top nodes

# Ver nodes disponíveis
oc get nodes

# Verificar node selectors
oc get pod <nome-do-pod> -o yaml | grep nodeSelector

# Ver taints nos nodes
oc describe nodes | grep Taints
```

### OOMKilled
```bash
# Verificar limite de memória
oc get pod <nome-do-pod> -o jsonpath='{.spec.containers[0].resources.limits.memory}'

# Ver uso atual
oc adm top pod <nome-do-pod>

# Aumentar limite de memória
oc set resources deployment/<nome> --limits=memory=2Gi

# Ver histórico de restarts
oc get pod <nome-do-pod> -o jsonpath='{.status.containerStatuses[0].restartCount}'

# Ver motivo da última terminação
oc get pod <nome-do-pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
```

---

## 🔧 Debug de Containers

### Debug Interativo
```bash
# Criar pod de debug
oc debug pod/<nome-do-pod>

# Debug de deployment
oc debug deployment/<nome>

# Debug de node
oc debug node/<node-name>

# Com imagem específica
oc debug pod/<nome> --image=registry.redhat.io/rhel8/support-tools

# Debug sem iniciar
oc debug pod/<nome> --keep-init-containers=true
```

### Executar Comandos
```bash
# Shell no container
oc rsh <nome-do-pod>

# Comando específico
oc exec <nome-do-pod> -- <comando>

# Em container específico
oc exec <nome-do-pod> -c <container> -- <comando>

# Verificar conectividade
oc exec <nome-do-pod> -- curl -v <url>
oc exec <nome-do-pod> -- ping <host>

# Verificar DNS
oc exec <nome-do-pod> -- nslookup <service>
oc exec <nome-do-pod> -- cat /etc/resolv.conf

# Verificar filesystem
oc exec <nome-do-pod> -- df -h
oc exec <nome-do-pod> -- ls -la /path
```

### Port Forward para Debug
```bash
# Forward de porta
oc port-forward <nome-do-pod> 8080:8080

# Múltiplas portas
oc port-forward <nome-do-pod> 8080:8080 9090:9090

# Em background
oc port-forward <nome-do-pod> 8080:8080 &

# Testar porta
curl http://localhost:8080
```

---

## 🩹 Problemas Comuns

### Volumes e Mounts
```bash
# Verificar PVC
oc get pvc

# Status do PVC
oc describe pvc <nome-do-pvc>

# Verificar mounts no pod
oc describe pod <nome-do-pod> | grep -A 10 Mounts

# Verificar permissões
oc exec <nome-do-pod> -- ls -la /mount/path
```

### ConfigMaps e Secrets
```bash
# Verificar ConfigMap montado
oc get cm <nome> -o yaml

# Verificar Secret
oc get secret <nome> -o yaml

# Ver variáveis de ambiente
oc set env pod/<nome> --list

# Verificar dentro do pod
oc exec <nome-do-pod> -- env | sort
```

### Network Issues
```bash
# Verificar service
oc get svc

# Endpoints do service
oc get endpoints <nome-do-service>

# Teste de conectividade
oc exec <nome-do-pod> -- curl -v <service-name>:<port>

# DNS lookup
oc exec <nome-do-pod> -- nslookup <service-name>

# Ver rede do pod
oc get pod <nome-do-pod> -o jsonpath='{.status.podIP}'
```

### Permissões e Security
```bash
# Verificar ServiceAccount
oc get sa

# Ver SCC do pod
oc get pod <nome-do-pod> -o yaml | grep scc

# Verificar RBAC
oc adm policy who-can <verbo> <recurso>

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
