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
**Exibir endereço IP do pod**

```bash
oc get pod my-pod -o jsonpath='{.status.podIP}'
```

**Testar conectividade entre pods**

```bash ignore-test
oc exec my-pod -- ping <ip-pod-destino>
oc exec my-pod -- curl <ip-pod-destino>:<porta>
```

**Testar service por nome**

```bash ignore-test
oc exec my-pod -- curl <nome-service>:<porta>
```

**Testar DNS**

```bash ignore-test
oc exec my-pod -- nslookup <nome-service>
```

**Executar comando dentro do pod especificado**

```bash
oc exec my-pod -- ip route
```

**Executar comando dentro do pod especificado**

```bash
oc exec my-pod -- ip addr
```

### Network Policies
**Listar políticas de rede configuradas no namespace**

```bash
oc get networkpolicy
```

**Exibir detalhes completos do política de rede**

```bash ignore-test
oc describe networkpolicy test-app
```

**Exibir política de rede em formato YAML completo**

```bash
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
**Listar todos os services do namespace atual**

```bash
oc get svc
```

**Exibir detalhes completos do service**

```bash
oc describe svc test-app
```

**Exibir service "test-app" em formato JSON**

```bash
oc get svc test-app -o jsonpath='{.spec.clusterIP}'
```

**Exibir service "test-app" em formato JSON**

```bash
oc get svc test-app -o jsonpath='{.spec.ports}'
```

**Testar service de dentro do cluster**

```bash ignore-test
oc run test-pod --image=quay.io/chiaretto/netshoot --rm -it --restart=Never -- wget -O- <service-name>:<port>
```

### Endpoints
**Listar endpoints**

```bash
oc get endpoints
```

**Endpoints de service específico**

```bash
oc get endpoints test-app
```

**Exibir endpoints "test-app" em formato JSON**

```bash ignore-test
oc get endpoints test-app -o jsonpath='{.subsets[*].addresses[*].ip}'
```

**Exibir service "test-app" em formato JSON**

```bash ignore-test
oc get svc test-app -o jsonpath='{.spec.selector}'
oc get pods --selector=<label-do-service>
```

**Exibir detalhes completos do service**

```bash
oc describe svc test-app | grep Selector
oc get pods --show-labels
```

---

## Routes e Ingress

### Troubleshoot Routes
**Listar todas as routes expostas no namespace**

```bash
oc get routes
```

**Exibir detalhes completos do route**

```bash
oc describe route test-app
```

**Exibir route "test-app" em formato JSON**

```bash
oc get route test-app -o jsonpath='{.spec.host}'
```

**Testar route externamente**

```bash ignore-test
curl -v https://<hostname-da-route>
```

**Exibir route "test-app" em formato JSON**

```bash
oc get route test-app -o jsonpath='{.spec.tls}'
```

**Exibir route "test-app" em formato JSON**

```bash
oc get route test-app -o jsonpath='{.spec.to.name}'
```

**Ver se service existe**

```bash ignore-test
oc get svc <service-name>
```

### Ingress Controller
**Status do router**

```bash
oc get pods -n openshift-ingress
```

**Exibir logs de todos os pods que correspondem ao label**

```bash
oc logs -n openshift-ingress -l app=router
```

**Exibir ingresses.config.openshift.io em formato JSON**

```bash
oc get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}'
```

**IngressController config**

```bash
oc get ingresscontroller -n openshift-ingress-operator
```

**Exibir detalhes completos do ingresscontroller**

```bash
oc describe ingresscontroller default -n openshift-ingress-operator
```

---

## SDN/OVN

### Verificar Rede do Cluster
**Exibir network.config.openshift.io em formato JSON**

```bash
oc get network.config.openshift.io cluster -o jsonpath='{.spec.networkType}'
```

**Exibir network.config.openshift.io em formato YAML**

```bash
oc get network.config.openshift.io cluster -o yaml
```

**Pods de rede**

```bash
oc get pods -n openshift-sdn
oc get pods -n openshift-ovn-kubernetes
```

**Logs de rede (SDN)**

```bash ignore-test
oc logs -n openshift-sdn <sdn-pod-name>
```

**Logs de rede (OVN)**

```bash ignore-test
oc logs -n openshift-ovn-kubernetes <ovn-pod-name>
```

### OVN-Kubernetes Debug
**Ver flows OVN**

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-ofctl dump-flows br-int
```

**Ver interfaces**

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-vsctl show
```

**Trace de pacote**

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-appctl ofproto/trace br-int <flow>
```

**Ver tabelas OVN**

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-master-pod> -- ovn-nbctl show
oc -n openshift-ovn-kubernetes exec <ovnkube-master-pod> -- ovn-sbctl show
```

### Multus e CNI
**Listar NetworkAttachmentDefinitions**

```bash
oc get network-attachment-definitions
```

**Ver CNI configs**

```bash
oc get pods -n openshift-multus
```

**Logs do Multus**

```bash ignore-test
oc logs -n openshift-multus <multus-pod>
```

---

## DNS

### Diagnóstico DNS
**Pods do CoreDNS/DNS**

```bash
oc get pods -n openshift-dns
```

**Logs do DNS**

```bash ignore-test
oc logs -n openshift-dns <dns-pod-name>
```

**Executar comando dentro do pod especificado**

```bash ignore-test
oc exec my-pod -- nslookup kubernetes.default
oc exec my-pod -- nslookup <service-name>
oc exec my-pod -- nslookup <service-name>.<namespace>.svc.cluster.local
```

**Executar comando dentro do pod especificado**

```bash
oc exec my-pod -- cat /etc/resolv.conf
```

**Verificar DNS operator**

```bash
oc get clusteroperator dns
```

**Exibir dns.operator/default em formato YAML**

```bash
oc get dns.operator/default -o yaml
```

### Problemas Comuns de DNS
**Verificar se DNS pods estão rodando**

```bash
oc get pods -n openshift-dns
```

**Deletar o pod especificado**

```bash ignore-test
oc delete pod -n openshift-dns --all
```

**Verificar se service do DNS existe**

```bash
oc get svc -n openshift-dns
```

**Executar comando dentro do pod especificado**

```bash
oc exec my-pod -- nslookup redhat.com
```

**Executar comando dentro do pod especificado**

```bash
oc exec my-pod -- nslookup kubernetes.default.svc.cluster.local
```

---

## Ferramentas de Debug

### Pod de Debug de Rede
**Criar e executar pod**

```bash ignore-test
oc run netshoot --rm -i --tty --image quay.io/chiaretto/netshoot -- /bin/bash
```

**Criar e executar pod**

```bash ignore-test
oc run debug --rm -i --tty --image=registry.redhat.io/rhel9/support-tools -- /bin/bash
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
**Debug node e captura de pacotes**

```bash ignore-test
oc debug node/<node-name>
```

* No node (chroot):

```bash ignore-test
chroot /host
```

**Capturar tráfego**

```bash ignore-test
tcpdump -i any -n host <ip-do-pod>
tcpdump -i any -n port <porta>
```

**Salvar captura**

```bash ignore-test
tcpdump -i any -w /tmp/capture.pcap
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking">Networking - Troubleshooting network issues</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support">Support - Troubleshooting</a>
---


## Navegação

- [← Anterior: Troubleshooting de Pods](13-troubleshooting-pods.md)
- [→ Próximo: Troubleshooting de Storage](15-troubleshooting-storage.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
