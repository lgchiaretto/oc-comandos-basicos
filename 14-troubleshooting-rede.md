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
```bash
# IP do pod
oc get pod <nome-do-pod> -o jsonpath='{.status.podIP}'

# Testar conectividade entre pods
oc exec <pod-origem> -- ping <ip-pod-destino>
oc exec <pod-origem> -- curl <ip-pod-destino>:<porta>

# Testar service por nome
oc exec <pod-origem> -- curl <nome-service>:<porta>

# Testar DNS
oc exec <pod-origem> -- nslookup <nome-service>

# Verificar rotas de rede
oc exec <pod-origem> -- ip route

# Interfaces de rede
oc exec <pod-origem> -- ip addr
```

### Network Policies
```bash
# Listar network policies
oc get networkpolicy

# Descrever policy
oc describe networkpolicy <nome>

# Ver todas as policies do namespace
oc get networkpolicy -o yaml

# Deletar temporariamente para testar
oc delete networkpolicy <nome>

# Verificar se policy está bloqueando
oc describe pod <nome> | grep -i network
```

---

## 🔌 Services e Endpoints

### Verificar Services
```bash
# Listar services
oc get svc

# Detalhes do service
oc describe svc <nome-do-service>

# Ver ClusterIP
oc get svc <nome> -o jsonpath='{.spec.clusterIP}'

# Ver portas
oc get svc <nome> -o jsonpath='{.spec.ports}'

# Testar service de dentro do cluster
oc run test-pod --image=busybox --rm -it --restart=Never -- wget -O- <service-name>:<port>
```

### Endpoints
```bash
# Listar endpoints
oc get endpoints

# Endpoints de service específico
oc get endpoints <nome-do-service>

# Verificar se endpoints estão vazios
oc get endpoints <nome-do-service> -o jsonpath='{.subsets[*].addresses[*].ip}'

# Comparar labels do service com pods
oc get svc <nome> -o jsonpath='{.spec.selector}'
oc get pods --selector=<label-do-service>

# Se não há endpoints, verificar labels
oc describe svc <nome> | grep Selector
oc get pods --show-labels
```

---

## 🛣️ Routes e Ingress

### Troubleshoot Routes
```bash
# Listar routes
oc get routes

# Detalhes da route
oc describe route <nome-da-route>

# Ver hostname da route
oc get route <nome> -o jsonpath='{.spec.host}'

# Testar route externamente
curl -v https://<hostname-da-route>

# Ver TLS da route
oc get route <nome> -o jsonpath='{.spec.tls}'

# Verificar se route aponta para service correto
oc get route <nome> -o jsonpath='{.spec.to.name}'

# Ver se service existe
oc get svc <service-name>
```

### Ingress Controller
```bash
# Status do router
oc get pods -n openshift-ingress

# Logs do router
oc logs -n openshift-ingress -l app=router

# Verificar domínio padrão
oc get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}'

# IngressController config
oc get ingresscontroller -n openshift-ingress-operator

# Descrever IngressController
oc describe ingresscontroller default -n openshift-ingress-operator
```

---

## 🕸️ SDN/OVN

### Verificar Rede do Cluster
```bash
# Ver tipo de rede (SDN ou OVN)
oc get network.config.openshift.io cluster -o jsonpath='{.spec.networkType}'

# Ver network config
oc get network.config.openshift.io cluster -o yaml

# Pods de rede
oc get pods -n openshift-sdn
# ou para OVN:
oc get pods -n openshift-ovn-kubernetes

# Logs de rede (SDN)
oc logs -n openshift-sdn <sdn-pod-name>

# Logs de rede (OVN)
oc logs -n openshift-ovn-kubernetes <ovn-pod-name>
```

### OVN-Kubernetes Debug
```bash
# Ver flows OVN
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-ofctl dump-flows br-int

# Ver interfaces
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-vsctl show

# Trace de pacote
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-appctl ofproto/trace br-int <flow>

# Ver tabelas OVN
oc -n openshift-ovn-kubernetes exec <ovnkube-master-pod> -- ovn-nbctl show
oc -n openshift-ovn-kubernetes exec <ovnkube-master-pod> -- ovn-sbctl show
```

### Multus e CNI
```bash
# Listar NetworkAttachmentDefinitions
oc get network-attachment-definitions

# Ver CNI configs
oc get pods -n openshift-multus

# Logs do Multus
oc logs -n openshift-multus <multus-pod>
```

---

## 🔤 DNS

### Diagnóstico DNS
```bash
# Pods do CoreDNS/DNS
oc get pods -n openshift-dns

# Logs do DNS
oc logs -n openshift-dns <dns-pod-name>

# Testar DNS de dentro do pod
oc exec <pod-name> -- nslookup kubernetes.default
oc exec <pod-name> -- nslookup <service-name>
oc exec <pod-name> -- nslookup <service-name>.<namespace>.svc.cluster.local

# Ver configuração DNS do pod
oc exec <pod-name> -- cat /etc/resolv.conf

# Verificar DNS operator
oc get clusteroperator dns

# Configuração DNS
oc get dns.operator/default -o yaml
```

### Problemas Comuns de DNS
```bash
# Verificar se DNS pods estão rodando
oc get pods -n openshift-dns

# Restart DNS pods se necessário
oc delete pod -n openshift-dns --all

# Verificar se service do DNS existe
oc get svc -n openshift-dns

# Testar resolução externa
oc exec <pod> -- nslookup google.com

# Testar resolução interna
oc exec <pod> -- nslookup kubernetes.default.svc.cluster.local
```

---

## 🛠️ Ferramentas de Debug

### Pod de Debug de Rede
```bash
# Criar pod com ferramentas de rede
oc run netshoot --rm -i --tty --image nicolaka/netshoot -- /bin/bash

# Ou usando imagem Red Hat
oc run debug --rm -i --tty --image=registry.redhat.io/rhel8/support-tools -- /bin/bash

# Dentro do pod, testar:
# - curl, wget
# - ping, traceroute
# - nslookup, dig
# - telnet, nc (netcat)
# - tcpdump
```

### Captura de Pacotes
```bash
# Debug node e captura de pacotes
oc debug node/<node-name>

# No node (chroot):
chroot /host

# Capturar tráfego
tcpdump -i any -n host <ip-do-pod>
tcpdump -i any -n port <porta>

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
