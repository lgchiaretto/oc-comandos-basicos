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
```markdown
**Ação:** Exibir recurso "my-pod" em formato JSON
**Exemplo:** `oc get pod <resource-name>pod -o jsonpath='{.status.podIP}'`
```

```bash
oc get pod my-pod -o jsonpath='{.status.podIP}'
```

```markdown
**Ação:** Testar conectividade entre pods
```

```bash ignore-test
oc exec my-pod -- ping <ip-pod-destino>
oc exec my-pod -- curl <ip-pod-destino>:<porta>
```

```markdown
**Ação:** Testar service por nome
```

```bash ignore-test
oc exec my-pod -- curl <nome-service>:<porta>
```

```markdown
**Ação:** Testar DNS
```

```bash ignore-test
oc exec my-pod -- nslookup <nome-service>
```

```markdown
**Ação:** Executar comando dentro do pod especificado
```

```bash
oc exec my-pod -- ip route
```

```markdown
**Ação:** Executar comando dentro do pod especificado
```

```bash
oc exec my-pod -- ip addr
```

### Network Policies
```markdown
**Ação:** Listar políticas de rede configuradas no namespace
```

```bash
oc get networkpolicy
```

```markdown
**Ação:** Exibir detalhes completos do network policy
**Exemplo:** `oc describe networkpolicy <resource-name>`
```

```bash ignore-test
oc describe networkpolicy test-app
```

```markdown
**Ação:** Exibir network policy em formato YAML
```

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
```markdown
**Ação:** Listar todos os services do namespace atual
**Exemplo:** `oc get svc <service-name>`
```

```bash
oc get svc
```

```markdown
**Ação:** Exibir detalhes completos do service
**Exemplo:** `oc describe svc <service-name>`
```

```bash
oc describe svc test-app
```

```markdown
**Ação:** Exibir service "test-app" em formato JSON
**Exemplo:** `oc get svc <service-name> -o jsonpath='{.spec.clusterIP}'`
```

```bash
oc get svc test-app -o jsonpath='{.spec.clusterIP}'
```

```markdown
**Ação:** Exibir service "test-app" em formato JSON
**Exemplo:** `oc get svc <service-name> -o jsonpath='{.spec.ports}'`
```

```bash
oc get svc test-app -o jsonpath='{.spec.ports}'
```

```markdown
**Ação:** Testar service de dentro do cluster
```

```bash ignore-test
oc run test-pod --image=quay.io/chiaretto/netshoot --rm -it --restart=Never -- wget -O- <service-name>:<port>
```

### Endpoints
```markdown
**Ação:** Listar endpoints
```

```bash
oc get endpoints
```

```markdown
**Ação:** Endpoints de service específico
**Exemplo:** `oc get endpoints <resource-name>`
```

```bash
oc get endpoints test-app
```

```markdown
**Ação:** Exibir endpoints "test-app" em formato JSON
**Exemplo:** `oc get endpoints <resource-name>app -o jsonpath='{.subsets[*].addresses[*].ip}'`
```

```bash ignore-test
oc get endpoints test-app -o jsonpath='{.subsets[*].addresses[*].ip}'
```

```markdown
**Ação:** Exibir service "test-app" em formato JSON
**Exemplo:** `oc get svc <service-name> -o jsonpath='{.spec.selector}'`
```

```bash ignore-test
oc get svc test-app -o jsonpath='{.spec.selector}'
oc get pods --selector=<label-do-service>
```

```markdown
**Ação:** Exibir detalhes completos do service
**Exemplo:** `oc describe svc <service-name> | grep Selector`
```

```bash
oc describe svc test-app | grep Selector
oc get pods --show-labels
```

---

## Routes e Ingress

### Troubleshoot Routes
```markdown
**Ação:** Listar todas as routes expostas no namespace
```

```bash
oc get routes
```

```markdown
**Ação:** Exibir detalhes completos do route
**Exemplo:** `oc describe route <route-name>>`
```

```bash
oc describe route test-app
```

```markdown
**Ação:** Exibir route "test-app" em formato JSON
**Exemplo:** `oc get route <route-name> -o jsonpath='{.spec.host}'`
```

```bash
oc get route test-app -o jsonpath='{.spec.host}'
```

```markdown
**Ação:** Testar route externamente
```

```bash ignore-test
curl -v https://<hostname-da-route>
```

```markdown
**Ação:** Exibir route "test-app" em formato JSON
**Exemplo:** `oc get route <route-name> -o jsonpath='{.spec.tls}'`
```

```bash
oc get route test-app -o jsonpath='{.spec.tls}'
```

```markdown
**Ação:** Exibir route "test-app" em formato JSON
**Exemplo:** `oc get route <route-name> -o jsonpath='{.spec.to.name}'`
```

```bash
oc get route test-app -o jsonpath='{.spec.to.name}'
```

```markdown
**Ação:** Ver se service existe
```

```bash ignore-test
oc get svc <service-name>
```

### Ingress Controller
```markdown
**Ação:** Status do router
```

```bash
oc get pods -n openshift-ingress
```

```markdown
**Ação:** Exibir logs de todos os pods que correspondem ao label
**Exemplo:** `oc logs -n <namespace> -l app=router`
```

```bash
oc logs -n openshift-ingress -l app=router
```

```markdown
**Ação:** Exibir recurso em formato JSON
```

```bash
oc get ingresses.config.openshift.io cluster -o jsonpath='{.spec.domain}'
```

```markdown
**Ação:** IngressController config
```

```bash
oc get ingresscontroller -n openshift-ingress-operator
```

```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe ingresscontroller default -n <namespace>`
```

```bash
oc describe ingresscontroller default -n openshift-ingress-operator
```

---

## SDN/OVN

### Verificar Rede do Cluster
```markdown
**Ação:** Exibir recurso em formato JSON
```

```bash
oc get network.config.openshift.io cluster -o jsonpath='{.spec.networkType}'
```

```markdown
**Ação:** Exibir recurso em formato YAML
```

```bash
oc get network.config.openshift.io cluster -o yaml
```

```markdown
**Ação:** Pods de rede
* ou para OVN:
```

```bash
oc get pods -n openshift-sdn
oc get pods -n openshift-ovn-kubernetes
```

```markdown
**Ação:** Logs de rede (SDN)
```

```bash ignore-test
oc logs -n openshift-sdn <sdn-pod-name>
```

```markdown
**Ação:** Logs de rede (OVN)
```

```bash ignore-test
oc logs -n openshift-ovn-kubernetes <ovn-pod-name>
```

### OVN-Kubernetes Debug
```markdown
**Ação:** Ver flows OVN
```

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-ofctl dump-flows br-int
```

```markdown
**Ação:** Ver interfaces
```

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-vsctl show
```

```markdown
**Ação:** Trace de pacote
```

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-node-pod> -- ovs-appctl ofproto/trace br-int <flow>
```

```markdown
**Ação:** Ver tabelas OVN
```

```bash ignore-test
oc -n openshift-ovn-kubernetes exec <ovnkube-master-pod> -- ovn-nbctl show
oc -n openshift-ovn-kubernetes exec <ovnkube-master-pod> -- ovn-sbctl show
```

### Multus e CNI
```markdown
**Ação:** Listar NetworkAttachmentDefinitions
```

```bash
oc get network-attachment-definitions
```

```markdown
**Ação:** Ver CNI configs
```

```bash
oc get pods -n openshift-multus
```

```markdown
**Ação:** Logs do Multus
```

```bash ignore-test
oc logs -n openshift-multus <multus-pod>
```

---

## DNS

### Diagnóstico DNS
```markdown
**Ação:** Pods do CoreDNS/DNS
```

```bash
oc get pods -n openshift-dns
```

```markdown
**Ação:** Logs do DNS
```

```bash ignore-test
oc logs -n openshift-dns <dns-pod-name>
```

```markdown
**Ação:** Executar comando dentro do pod especificado
```

```bash ignore-test
oc exec my-pod -- nslookup kubernetes.default
oc exec my-pod -- nslookup <service-name>
oc exec my-pod -- nslookup <service-name>.<namespace>.svc.cluster.local
```

```markdown
**Ação:** Executar comando dentro do pod especificado
```

```bash
oc exec my-pod -- cat /etc/resolv.conf
```

```markdown
**Ação:** Verificar DNS operator
**Exemplo:** `oc get clusteroperator <resource-name>`
```

```bash
oc get clusteroperator dns
```

```markdown
**Ação:** Exibir recurso em formato YAML
```

```bash
oc get dns.operator/default -o yaml
```

### Problemas Comuns de DNS
```markdown
**Ação:** Verificar se DNS pods estão rodando
```

```bash
oc get pods -n openshift-dns
```

```markdown
**Ação:** Deletar o recurso especificado
**Exemplo:** `oc delete pod -n <namespace> --all`
```

```bash ignore-test
oc delete pod -n openshift-dns --all
```

```markdown
**Ação:** Verificar se service do DNS existe
```

```bash
oc get svc -n openshift-dns
```

```markdown
**Ação:** Executar comando dentro do pod especificado
```

```bash
oc exec my-pod -- nslookup redhat.com
```

```markdown
**Ação:** Executar comando dentro do pod especificado
```

```bash
oc exec my-pod -- nslookup kubernetes.default.svc.cluster.local
```

---

## Ferramentas de Debug

### Pod de Debug de Rede
```markdown
**Ação:** Criar e executar pod
```

```bash ignore-test
oc run netshoot --rm -i --tty --image quay.io/chiaretto/netshoot -- /bin/bash
```

```markdown
**Ação:** Criar e executar pod
```

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
```markdown
**Ação:** Debug node e captura de pacotes
```

```bash ignore-test
oc debug node/<node-name>
```

```markdown
* No node (chroot):
```

```bash ignore-test
chroot /host
```

```markdown
**Ação:** Capturar tráfego
```

```bash ignore-test
tcpdump -i any -n host <ip-do-pod>
tcpdump -i any -n port <porta>
```

```markdown
**Ação:** Salvar captura
```

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
