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
**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A --field-selector=status.phase!=Running
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A --field-selector=status.phase=Failed
```

**Listar pods em estado Pending (aguardando)**

```bash
oc get pods --field-selector=status.phase=Pending
```

**Exibir detalhes completos do pod**

```bash
oc describe pod my-pod
```

**Listar eventos filtrados por campo específico**

```bash ignore-test
oc get events --field-selector involvedObject.name=my-pod
```

**Exibir configuração completa do pod em formato YAML**

```bash
oc get pod my-pod -o yaml
```

### Verificar Logs
**Exibir logs do pod especificado**

```bash ignore-test
oc logs my-pod
```

**Exibir logs de container específico do pod**

```bash ignore-test
oc logs my-pod -c httpd
```

**Exibir logs da instância anterior do container (após crash)**

```bash ignore-test
oc logs my-pod --previous
```

**Acompanhar logs em tempo real do pod**

```bash ignore-test
oc logs -f my-pod
```

**Exibir últimas N linhas dos logs**

```bash ignore-test
oc logs my-pod --tail=100
```

---

## Pods com Problemas

### ImagePullBackOff
**Exibir detalhes completos do pod**

```bash ignore-test
oc describe pod my-pod | grep -A 10 Events
```

**Listar todas as ImageStreams do projeto**

```bash
oc get is
```

**Tentar pull manual (debug)**

```bash ignore-test
oc debug node/<node-name> -- chroot /host podman pull <image>
```

**Exibir pod em formato JSON**

```bash ignore-test
oc get pod my-pod -o jsonpath='{.spec.containers[0].image}'
```

### CrashLoopBackOff
**Exibir logs da instância anterior do container (após crash)**

```bash ignore-test
oc logs my-pod --previous
```

**Exibir detalhes completos do pod**

```bash ignore-test
oc describe pod my-pod | grep -i "exit code"
```

**Exibir configuração completa do pod em formato YAML**

```bash ignore-test
oc get pod my-pod -o yaml | grep -A 10 livenessProbe
```

**Desabilitar probes temporariamente**

**oc set probe <resource-name>/test-app --readiness --remove**

```bash
oc set probe deployment/test-app --liveness --remove
oc set probe deployment/test-app --readiness --remove
```

**Criar cópia de pod para debug interativo**

```bash ignore-test
oc debug deployment/test-app
```

### Pending (Não Agendado)
**Exibir detalhes completos do pod**

```bash ignore-test
oc describe pod my-pod | grep -A 20 Events
```

**Exibir configuração completa do pod em formato YAML**

```bash ignore-test
oc get pod my-pod -o yaml | grep -A 5 resources
```

**Ver capacidade dos nodes**

```bash
oc adm top nodes
```

**Listar todos os nodes do cluster**

```bash
oc get nodes
```

**Exibir configuração completa do pod em formato YAML**

```bash ignore-test
oc get pod my-pod -o yaml | grep nodeSelector
```

**Exibir detalhes completos do nodes**

```bash
oc describe nodes | grep Taints
```

### OOMKilled
**Exibir pod em formato JSON**

```bash
oc get pod my-pod -o jsonpath='{.spec.containers[0].resources.limits.memory}'
```

**Ver uso atual**

```bash ignore-test
oc adm top pod my-pod
```

**Definir/atualizar requests e limits de recursos**

```bash
oc set resources deployment/test-app --limits=memory=2Gi
```

**Exibir pod em formato JSON**

```bash
oc get pod my-pod -o jsonpath='{.status.containerStatuses[0].restartCount}'
```

**Exibir pod em formato JSON**

```bash
oc get pod my-pod -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
```

---

## Debug de Containers

### Debug Interativo
**Criar cópia de pod para debug interativo**

```bash ignore-test
oc debug pod/my-pod
```

**Criar cópia de pod para debug interativo**

```bash ignore-test
oc debug deployment/test-app
```

**Debug de node**

```bash ignore-test
oc debug node/<node-name>
```

### Executar Comandos
**Abrir shell interativo dentro do pod**

```bash ignore-test
oc rsh my-pod
```

**Comando específico**

```bash ignore-test
oc exec my-pod -- <comando>
```

**Em container específico**

```bash ignore-test
oc exec my-pod -c <container> -- <comando>
```

**Verificar conectividade**

```bash ignore-test
oc exec my-pod -- curl -v <url>
oc exec my-pod -- ping <host>
```

**Verificar DNS**

```bash ignore-test
oc exec my-pod -- nslookup <service>
oc exec my-pod -- cat /etc/resolv.conf
```

**Executar comando dentro do pod especificado**

```bash ignore-test
oc exec my-pod -- df -h
oc exec my-pod -- ls -la /path
```

### Port Forward para Debug
**Forward de porta**

```bash ignore-test
oc port-forward my-pod 8080:8080
```

**Múltiplas portas**

```bash ignore-test
oc port-forward my-pod 8080:8080 9090:9090
```

**Em background**

```bash ignore-test
oc port-forward my-pod 8080:8080 &
```

**Testar porta**

```bash
curl http://localhost:8080
```

---

## Problemas Comuns

### Volumes e Mounts
**Listar todos os Persistent Volume Claims do namespace**

```bash
oc get pvc
```

**Exibir detalhes completos do persistent volume claim**

```bash ignore-test
oc describe pvc test-app
```

**Exibir detalhes completos do pod**

```bash ignore-test
oc describe pod my-pod | grep -A 10 Mounts
```

**Executar comando dentro do pod especificado**

```bash ignore-test
oc exec my-pod -- ls -la /mount/path
```

### ConfigMaps e Secrets
**Exibir configmap "test-app" em formato YAML**

```bash
oc get cm test-app -o yaml
```

**Exibir secret "test-app" em formato YAML**

```bash
oc get secret test-app -o yaml
```

**Definir/atualizar variáveis de ambiente no recurso**

```bash ignore-test
oc set env pod/test-app --list
```

**Executar comando dentro do pod especificado**

```bash ignore-test
oc exec my-pod -- env | sort
```

### Network Issues
**Listar todos os services do namespace atual**

```bash
oc get svc
```

**Endpoints do service**

```bash
oc get endpoints test-app
```

**Teste de conectividade**

```bash ignore-test
oc exec my-pod -- curl -v <service-name>:<port>
```

**DNS lookup**

```bash ignore-test
oc exec my-pod -- nslookup <service-name>
```

**Exibir pod em formato JSON**

```bash ignore-test
oc get pod my-pod -o jsonpath='{.status.podIP}'
```

### Permissões e Security
**Listar todas as ServiceAccounts do namespace**

```bash
oc get sa
```

**Exibir configuração completa do pod em formato YAML**

```bash ignore-test
oc get pod my-pod -o yaml | grep scc
```

**Verificar RBAC**

```bash ignore-test
oc adm policy who-can <verbo> <recurso>
```

**Exibir pod em formato JSON**

```bash ignore-test
oc get pod my-pod -o jsonpath='{.spec.securityContext.runAsUser}'
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support">Support - Troubleshooting</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes">Nodes</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications">Building applications</a>
---


## Navegação

- [← Anterior: Must-Gather](12-must-gather.md)
- [→ Próximo: Troubleshooting de Rede](14-troubleshooting-rede.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
