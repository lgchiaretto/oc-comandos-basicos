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
**Ação:** Exibir recurso "my-pod" em formato JSON
**Exemplo:** `oc get pod <resource-name>pod -o jsonpath='{.status.podIP}'`

```bash
oc get pod my-pod -o jsonpath='{.status.podIP}'
```

**Ação:** Testar conectividade entre pods

```bash ignore-test
oc exec my-pod -- ping <ip-pod-destino>
oc exec my-pod -- curl <ip-pod-destino>:<porta>
```

**Ação:** Testar service por nome

```bash ignore-test
oc exec my-pod -- curl <nome-service>:<porta>
```

**Ação:** Testar DNS

```bash ignore-test
oc exec my-pod -- nslookup <nome-service>
```

**Ação:** Executar comando dentro do pod especificado

```bash
oc exec my-pod -- ip route
```

**Ação:** Executar comando dentro do pod especificado

```bash
oc exec my-pod -- ip addr
```

### Network Policies
**Ação:** Listar políticas de rede configuradas no namespace

```bash
oc get networkpolicy
```

**Ação:** Exibir detalhes completos do network policy
**Exemplo:** `oc describe networkpolicy <resource-name>`

```bash ignore-test
oc describe networkpolicy test-app
```

**Ação:** Exibir network policy em formato YAML

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
**Ação:** Listar todos os services do namespace atual
**Exemplo:** `oc get svc <service-name>`

```bash
oc get svc
```

**Ação:** Exibir detalhes completos do service
**Exemplo:** `oc describe svc <service-name>`

```bash
oc describe svc test-app
```

**Ação:** Exibir service "test-app" em formato JSON
**Exemplo:** `oc get svc <service-name> -o jsonpath='{.spec.clusterIP}'`

```bash
oc get svc test-app -o jsonpath='{.spec.clusterIP}'
```

**Ação:** Exibir service "test-app" em formato JSON
**Exemplo:** `oc get svc <service-name> -o jsonpath='{.spec.ports}'`

```bash
oc get svc test-app -o jsonpath='{.spec.ports}'
```

**Ação:** Testar service de dentro do cluster

```bash ignore-test
oc run test-pod --image=quay.io/chiaretto/netshoot --rm -it --restart=Never -- wget -O- <service-name>:<port>
```

### Endpoints
**Ação:** Listar endpoints

```bash
oc get endpoints
```

**Ação:** Endpoints de service específico
**Exemplo:** `oc get endpoints <resource-name>`

```bash
oc get endpoints test-app
```

**Ação:** Exibir endpoints "test-app" em formato JSON
**Exemplo:** `oc get endpoints <resource-name>app -o jsonpath='{.subsets[*].addresses[*].ip}'`

```bash ignore-test
oc get endpoints test-app -o jsonpath='{.subsets[*].addresses[*].ip}'
```

**Ação:** Exibir service "test-app" em formato JSON
**Exemplo:** `oc get svc <service-name> -o jsonpath='{.spec.selector}'`

```bash ignore-test
oc get svc test-app -o jsonpath='{.spec.selector}'
oc get pods --selector=<label-do-service>
```

**Ação:** Exibir detalhes completos do service
**Exemplo:** `oc describe svc <service-name> | grep Selector`

```bash
oc describe svc test-app | grep Selector
oc get pods --show-labels
```

---

## Routes e Ingress

### Troubleshoot Routes
**Ação:** Listar todas as routes expostas no namespace

```bash
oc get routes
```

**Ação:** Exibir detalhes completos do route
**Exemplo:** `oc describe route <route-name>>`

```bash
oc describe route test-app
```

**Ação:** Exibir route "test-app" em formato JSON
**Exemplo:** `oc get route <route-name> -o jsonpath='{.spec.host}'`

```bash
oc get route test-app -o jsonpath='{.spec.host}'
```

**Ação:** Testar route externamente

```bash ignore-test
curl -v https://<hostname-da-route>
```

**Ação:** Exibir route "test-app" em formato JSON
**Exemplo:** `oc get route <route-name> -o jsonpath='{.spec.tls}'`

```bash
oc get route test-app -o jsonpath='{.spec.tls}'
```

**Ação:** Exibir route "test-app" em formato JSON
**Exemplo:** `oc get route <route-name> -o jsonpath='{.spec.to.name}'`

```bash
oc get route test-app -o jsonpath='{.spec.to.name}'
```

**Ação:** Ver se service existe

```bash ignore-test
oc get svc <service-name>
```

### Ingress Controller
**Ação:** Status do router

```bash
oc get pods -n openshift-ingress
```

**Ação:** Exibir logs de todos os pods que correspondem ao label
**Exemplo:** `oc logs -n <namespace> -l app=router`

```bash
oc logs -n openshift-ingress -l app=router
```

**Ação:** Exibir recurso em formato JSON

```bash
oc get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}'
```

**Ação:** IngressController config

```bash
oc get ingresscontroller -n openshift-ingress-operator
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe ingresscontroller default -n <namespace>`

```bash
oc describe ingresscontroller default -n openshift-ingress-operator
```

---

## SDN/OVN

### Verificar Rede do Cluster
**Ação:** Exibir recurso em formato JSON

```bash
oc get network.config.openshift.io cluster -o jsonpath='{.spec.networkType}'
```

**Ação:** Exibir recurso em formato YAML

```bash
oc get network.config.openshift.io cluster -o yaml
```

**Ação:** Pods de rede
* ou para OVN:

```bash
oc get pods -n openshift-sdn
oc get pods -n openshift-ovn-kubernetes
```

**Ação:** Logs de rede (SDN)

```bash ignore-test
oc logs -n openshift-sdn <sdn-pod-name>
```

**Ação:** Logs de rede (OVN)

```bash ignore-test
oc logs -n openshift-ovn-kubernetes <ovn-pod-name>
```

### OVN-Kubernetes Debug
**Ação:** Ver flows OVN

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-ofctl dump-flows br-int
```

**Ação:** Ver interfaces

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-vsctl show
```

**Ação:** Trace de pacote

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-appctl ofproto/trace br-int <flow>
```

**Ação:** Ver tabelas OVN

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-master-pod> -- ovn-nbctl show
oc -n openshift-ovn-kubernetes exec <ovnkube-master-pod> -- ovn-sbctl show
```

### Multus e CNI
**Ação:** Listar NetworkAttachmentDefinitions

```bash
oc get network-attachment-definitions
```

**Ação:** Ver CNI configs

```bash
oc get pods -n openshift-multus
```

**Ação:** Logs do Multus

```bash ignore-test
oc logs -n openshift-multus <multus-pod>
```

---

## DNS

### Diagnóstico DNS
**Ação:** Pods do CoreDNS/DNS

```bash
oc get pods -n openshift-dns
```

**Ação:** Logs do DNS

```bash ignore-test
oc logs -n openshift-dns <dns-pod-name>
```

**Ação:** Executar comando dentro do pod especificado

```bash ignore-test
oc exec my-pod -- nslookup kubernetes.default
oc exec my-pod -- nslookup <service-name>
oc exec my-pod -- nslookup <service-name>.<namespace>.svc.cluster.local
```

**Ação:** Executar comando dentro do pod especificado

```bash
oc exec my-pod -- cat /etc/resolv.conf
```

**Ação:** Verificar DNS operator
**Exemplo:** `oc get clusteroperator <resource-name>`

```bash
oc get clusteroperator dns
```

**Ação:** Exibir recurso em formato YAML

```bash
oc get dns.operator/default -o yaml
```

### Problemas Comuns de DNS
**Ação:** Verificar se DNS pods estão rodando

```bash
oc get pods -n openshift-dns
```

**Ação:** Deletar o recurso especificado
**Exemplo:** `oc delete pod -n <namespace> --all`

```bash ignore-test
oc delete pod -n openshift-dns --all
```

**Ação:** Verificar se service do DNS existe

```bash
oc get svc -n openshift-dns
```

**Ação:** Executar comando dentro do pod especificado

```bash
oc exec my-pod -- nslookup redhat.com
```

**Ação:** Executar comando dentro do pod especificado

```bash
oc exec my-pod -- nslookup kubernetes.default.svc.cluster.local
```

---

## Ferramentas de Debug

### Pod de Debug de Rede
**Ação:** Criar e executar pod

```bash ignore-test
oc run netshoot --rm -i --tty --image quay.io/chiaretto/netshoot -- /bin/bash
```

**Ação:** Criar e executar pod

```bash ignore-test
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
**Ação:** Debug node e captura de pacotes

```bash ignore-test
oc debug node/<node-name>
```

* No node (chroot):

```bash ignore-test
chroot /host
```

**Ação:** Capturar tráfego

```bash ignore-test
tcpdump -i any -n host <ip-do-pod>
tcpdump -i any -n port <porta>
```

**Ação:** Salvar captura

```bash ignore-test
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
