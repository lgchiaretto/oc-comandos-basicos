# 🌐 Troubleshooting de Rede

Este documento contém comandos para diagnosticar problemas de rede no OpenShift.

---

## 📋 Índice

1. [Diagnóstico Básico](#diagnóstico-básico)
2. [Services e Endpoints](#services-e-endpoints)
3. [Routes e Ingress](#routes-e-ingress)
4. [SDN/OVN](#sdnovn)
5. [DNS](#dns)

---

## 🔍 Diagnóstico Básico

### Conectividade de Pod
```bash ignore-test
# IP do pod
oc get pod <nome-do-pod> -o jsonpath='{.status.podIP}'
```

```bash ignore-test
# Testar conectividade entre pods
oc exec <pod-origem> -- ping <ip-pod-destino>
oc exec <pod-origem> -- curl <ip-pod-destino>:<porta>
```

```bash ignore-test
# Testar service por nome
oc exec <pod-origem> -- curl <nome-service>:<porta>
```

```bash ignore-test
# Testar DNS
oc exec <pod-origem> -- nslookup <nome-service>
```

```bash ignore-test
# Verificar rotas de rede
oc exec <pod-origem> -- ip route
```

```bash ignore-test
# Interfaces de rede
oc exec <pod-origem> -- ip addr
```

### Network Policies
```bash
# Listar network policies
oc get networkpolicy
```

```bash ignore-test
# Descrever policy
# oc describe networkpolicy <resource-name>
oc describe networkpolicy test-app
```

```bash
# Ver todas as policies do namespace
oc get networkpolicy -o yaml
```

```bash ignore-tests
# Deletar temporariamente para testar
# oc delete networkpolicy <resource-name>
oc delete networkpolicy test-app
```

```bash ignore-tests
# Verificar se policy está bloqueando
# oc describe pod <resource-name> | grep -i network
oc describe pod test-app | grep -i network
```

---

## 🔌 Services e Endpoints

### Verificar Services
```bash
# Listar services
oc get svc
```

```bash
# Detalhes do service
# oc describe svc <service-name>
oc describe svc test-app
```

```bash
# Ver ClusterIP
# oc get svc <service-name> -o jsonpath='{.spec.clusterIP}'
oc get svc test-app -o jsonpath='{.spec.clusterIP}'
```

```bash
# Ver portas
# oc get svc <service-name> -o jsonpath='{.spec.ports}'
oc get svc test-app -o jsonpath='{.spec.ports}'
```

```bash ignore-test
# Testar service de dentro do cluster
oc run test-pod --image=busybox --rm -it --restart=Never -- wget -O- <service-name>:<port>
```

### Endpoints
```bash
# Listar endpoints
oc get endpoints
```

```bash
# Endpoints de service específico
# oc get endpoints <resource-name>
oc get endpoints test-app
```

```bash ignore-test
# Verificar se endpoints estão vazios
# oc get endpoints <resource-name>app -o jsonpath='{.subsets[*].addresses[*].ip}'
oc get endpoints test-app -o jsonpath='{.subsets[*].addresses[*].ip}'
```

```bash ignore-test
# Comparar labels do service com pods
# oc get svc <service-name> -o jsonpath='{.spec.selector}'
oc get svc test-app -o jsonpath='{.spec.selector}'
oc get pods --selector=<label-do-service>
```

```bash
# Se não há endpoints, verificar labels
# oc describe svc <service-name> | grep Selector
oc describe svc test-app | grep Selector
oc get pods --show-labels
```

---

## 🛣️ Routes e Ingress

### Troubleshoot Routes
```bash
# Listar routes
oc get routes
```

```bash
# Detalhes da route
# oc describe route <route-name>>
oc describe route test-app
```

```bash
# Ver hostname da route
# oc get route <route-name> -o jsonpath='{.spec.host}'
oc get route test-app -o jsonpath='{.spec.host}'
```

```bash ignore-test
# Testar route externamente
curl -v https://<hostname-da-route>
```

```bash
# Ver TLS da route
# oc get route <route-name> -o jsonpath='{.spec.tls}'
oc get route test-app -o jsonpath='{.spec.tls}'
```

```bash
# Verificar se route aponta para service correto
# oc get route <route-name> -o jsonpath='{.spec.to.name}'
oc get route test-app -o jsonpath='{.spec.to.name}'
```

```bash ignore-test
# Ver se service existe
oc get svc <service-name>
```

### Ingress Controller
```bash
# Status do router
oc get pods -n openshift-ingress
```

```bash
# Logs do router
# oc logs -n <namespace> -l app=router
oc logs -n openshift-ingress -l app=router
```

```bash
# Verificar domínio padrão
oc get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}'
```

```bash
# IngressController config
oc get ingresscontroller -n openshift-ingress-operator
```

```bash
# Descrever IngressController
# oc describe ingresscontroller default -n <namespace>
oc describe ingresscontroller default -n openshift-ingress-operator
```

---

## 🕸️ SDN/OVN

### Verificar Rede do Cluster
```bash
# Ver tipo de rede (SDN ou OVN)
oc get network.config.openshift.io cluster -o jsonpath='{.spec.networkType}'
```

```bash
# Ver network config
oc get network.config.openshift.io cluster -o yaml
```

```bash
# Pods de rede
oc get pods -n openshift-sdn
# ou para OVN:
oc get pods -n openshift-ovn-kubernetes
```

```bash ignore-test
# Logs de rede (SDN)
oc logs -n openshift-sdn <sdn-pod-name>
```

```bash ignore-test
# Logs de rede (OVN)
oc logs -n openshift-ovn-kubernetes <ovn-pod-name>
```

### OVN-Kubernetes Debug
```bash ignore-test
# Ver flows OVN
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-ofctl dump-flows br-int
```

```bash ignore-test
# Ver interfaces
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-vsctl show
```

```bash ignore-test
# Trace de pacote
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-appctl ofproto/trace br-int <flow>
```

```bash ignore-test
# Ver tabelas OVN
oc -n openshift-ovn-kubernetes exec <ovnkube-master-pod> -- ovn-nbctl show
oc -n openshift-ovn-kubernetes exec <ovnkube-master-pod> -- ovn-sbctl show
```

### Multus e CNI
```bash
# Listar NetworkAttachmentDefinitions
oc get network-attachment-definitions
```

```bash
# Ver CNI configs
oc get pods -n openshift-multus
```

```bash ignore-test
# Logs do Multus
oc logs -n openshift-multus <multus-pod>
```

---

## 🔤 DNS

### Diagnóstico DNS
```bash
# Pods do CoreDNS/DNS
oc get pods -n openshift-dns
```

```bash ignore-test
# Logs do DNS
oc logs -n openshift-dns <dns-pod-name>
```

```bash ignore-test
# Testar DNS de dentro do pod
oc exec <pod-name> -- nslookup kubernetes.default
oc exec <pod-name> -- nslookup <service-name>
oc exec <pod-name> -- nslookup <service-name>.<namespace>.svc.cluster.local
```

```bash ignore-test
# Ver configuração DNS do pod
oc exec <pod-name> -- cat /etc/resolv.conf
```

```bash
# Verificar DNS operator
# oc get clusteroperator <resource-name>
oc get clusteroperator dns
```

```bash
# Configuração DNS
oc get dns.operator/default -o yaml
```

### Problemas Comuns de DNS
```bash
# Verificar se DNS pods estão rodando
oc get pods -n openshift-dns
```

```bash ignore-test
# Restart DNS pods se necessário
# oc delete pod -n <namespace> --all
oc delete pod -n openshift-dns --all
```

```bash
# Verificar se service do DNS existe
oc get svc -n openshift-dns
```

```bash ignore-test
# Testar resolução externa
oc exec <pod> -- nslookup google.com
```

```bash ignore-test
# Testar resolução interna
oc exec <pod> -- nslookup kubernetes.default.svc.cluster.local
```

---

## 🛠️ Ferramentas de Debug

### Pod de Debug de Rede
```bash ignore-test
# Criar pod com ferramentas de rede
oc run netshoot --rm -i --tty --image nicolaka/netshoot -- /bin/bash
```

```bash ignore-test
# Ou usando imagem Red Hat
oc run debug --rm -i --tty --image=registry.redhat.io/rhel8/support-tools -- /bin/bash
```

```
# Dentro do pod, testar:
# - curl, wget
# - ping, traceroute
# - nslookup, dig
# - telnet, nc (netcat)
# - tcpdump
```

### Captura de Pacotes
```bash ignore-test
# Debug node e captura de pacotes
oc debug node/<node-name>
```

```bash ignore-test
# No node (chroot):
chroot /host
```

```bash ignore-test
# Capturar tráfego
tcpdump -i any -n host <ip-do-pod>
tcpdump -i any -n port <porta>
```

```bash ignore-test
# Salvar captura
tcpdump -i any -w /tmp/capture.pcap
```

---

## 📖 Navegação

- [← Anterior: Troubleshooting de Pods](13-troubleshooting-pods.md)
- [→ Próximo: Troubleshooting de Storage](15-troubleshooting-storage.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
