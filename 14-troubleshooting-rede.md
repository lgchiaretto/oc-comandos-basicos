# Troubleshooting de Rede

Este documento contém comandos para diagnosticar problemas de rede no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Diagnóstico Básico](#diagnóstico-básico)
3. [Services e Endpoints](#services-e-endpoints)
4. [Routes e Ingress](#routes-e-ingress)
5. [SDN/OVN](#sdn/ovn)
6. [DNS](#dns)
7. [Ferramentas de Debug](#ferramentas-de-debug)
8. [Documentação Oficial](#documentação-oficial)
9. [Navegação](#navegação)
---

## Diagnóstico Básico

### Conectividade de Pod
```bash
# Exibir recurso "my-pod" em formato JSON
# oc get pod <resource-name>pod -o jsonpath='{.status.podIP}'
oc get pod my-pod -o jsonpath='{.status.podIP}'
```

```bash ignore-test
# Testar conectividade entre pods
oc exec my-pod -- ping <ip-pod-destino>
oc exec my-pod -- curl <ip-pod-destino>:<porta>
```

```bash ignore-test
# Testar service por nome
oc exec my-pod -- curl <nome-service>:<porta>
```

```bash ignore-test
# Testar DNS
oc exec my-pod -- nslookup <nome-service>
```

```bash
# Executar comando dentro do pod especificado
oc exec my-pod -- ip route
```

```bash
# Executar comando dentro do pod especificado
oc exec my-pod -- ip addr
```

### Network Policies
```bash
# Listar políticas de rede configuradas no namespace
oc get networkpolicy
```

```bash ignore-test
# Exibir detalhes completos do network policy
# oc describe networkpolicy <resource-name>
oc describe networkpolicy test-app
```

```bash
# Exibir network policy em formato YAML
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

## Services e Endpoints

### Verificar Services
```bash
# Listar todos os services do namespace atual
# oc get svc <service-name>
oc get svc
```

```bash
# Exibir detalhes completos do service
# oc describe svc <service-name>
oc describe svc test-app
```

```bash
# Exibir service "test-app" em formato JSON
# oc get svc <service-name> -o jsonpath='{.spec.clusterIP}'
oc get svc test-app -o jsonpath='{.spec.clusterIP}'
```

```bash
# Exibir service "test-app" em formato JSON
# oc get svc <service-name> -o jsonpath='{.spec.ports}'
oc get svc test-app -o jsonpath='{.spec.ports}'
```

```bash ignore-test
# Testar service de dentro do cluster
oc run test-pod --image=quay.io/chiaretto/netshoot --rm -it --restart=Never -- wget -O- <service-name>:<port>
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
# Exibir endpoints "test-app" em formato JSON
# oc get endpoints <resource-name>app -o jsonpath='{.subsets[*].addresses[*].ip}'
oc get endpoints test-app -o jsonpath='{.subsets[*].addresses[*].ip}'
```

```bash ignore-test
# Exibir service "test-app" em formato JSON
# oc get svc <service-name> -o jsonpath='{.spec.selector}'
oc get svc test-app -o jsonpath='{.spec.selector}'
oc get pods --selector=<label-do-service>
```

```bash
# Exibir detalhes completos do service
# oc describe svc <service-name> | grep Selector
oc describe svc test-app | grep Selector
oc get pods --show-labels
```

---

## Routes e Ingress

### Troubleshoot Routes
```bash
# Listar todas as routes expostas no namespace
oc get routes
```

```bash
# Exibir detalhes completos do route
# oc describe route <route-name>>
oc describe route test-app
```

```bash
# Exibir route "test-app" em formato JSON
# oc get route <route-name> -o jsonpath='{.spec.host}'
oc get route test-app -o jsonpath='{.spec.host}'
```

```bash ignore-test
# Testar route externamente
curl -v https://<hostname-da-route>
```

```bash
# Exibir route "test-app" em formato JSON
# oc get route <route-name> -o jsonpath='{.spec.tls}'
oc get route test-app -o jsonpath='{.spec.tls}'
```

```bash
# Exibir route "test-app" em formato JSON
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
# Exibir logs de todos os pods que correspondem ao label
# oc logs -n <namespace> -l app=router
oc logs -n openshift-ingress -l app=router
```

```bash
# Exibir recurso em formato JSON
oc get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}'
```

```bash
# IngressController config
oc get ingresscontroller -n openshift-ingress-operator
```

```bash
# Exibir detalhes completos do recurso
# oc describe ingresscontroller default -n <namespace>
oc describe ingresscontroller default -n openshift-ingress-operator
```

---

## SDN/OVN

### Verificar Rede do Cluster
```bash
# Exibir recurso em formato JSON
oc get network.config.openshift.io cluster -o jsonpath='{.spec.networkType}'
```

```bash
# Exibir recurso em formato YAML
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

## DNS

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
# Executar comando dentro do pod especificado
oc exec my-pod -- nslookup kubernetes.default
oc exec my-pod -- nslookup <service-name>
oc exec my-pod -- nslookup <service-name>.<namespace>.svc.cluster.local
```

```bash
# Executar comando dentro do pod especificado
oc exec my-pod -- cat /etc/resolv.conf
```

```bash
# Verificar DNS operator
# oc get clusteroperator <resource-name>
oc get clusteroperator dns
```

```bash
# Exibir recurso em formato YAML
oc get dns.operator/default -o yaml
```

### Problemas Comuns de DNS
```bash
# Verificar se DNS pods estão rodando
oc get pods -n openshift-dns
```

```bash ignore-test
# Deletar o recurso especificado
# oc delete pod -n <namespace> --all
oc delete pod -n openshift-dns --all
```

```bash
# Verificar se service do DNS existe
oc get svc -n openshift-dns
```

```bash
# Executar comando dentro do pod especificado
oc exec my-pod -- nslookup redhat.com
```

```bash
# Executar comando dentro do pod especificado
oc exec my-pod -- nslookup kubernetes.default.svc.cluster.local
```

---

## Ferramentas de Debug

### Pod de Debug de Rede
```bash ignore-test
# Criar e executar pod
oc run netshoot --rm -i --tty --image quay.io/chiaretto/netshoot -- /bin/bash
```

```bash ignore-test
# Criar e executar pod
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

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking">Networking - Troubleshooting network issues</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support">Support - Troubleshooting</a>
---

---

## Navegação

- [← Anterior: Troubleshooting de Pods](13-troubleshooting-pods.md)
- [→ Próximo: Troubleshooting de Storage](15-troubleshooting-storage.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
