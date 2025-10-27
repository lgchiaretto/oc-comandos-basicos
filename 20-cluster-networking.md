# Cluster Networking

Este documento contém comandos para configuração e troubleshooting de rede do cluster OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Configuração de Rede](#configuração-de-rede)
3. [Ingress Controllers](#ingress-controllers)
4. [Network Policies](#network-policies)
5. [Configurações Avançadas](#configurações-avançadas)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## Configuração de Rede

### Visualizar Configuração
```bash
# Exibir recurso em formato YAML
oc get network.config.openshift.io cluster -o yaml
```

```bash
# Exibir recurso em formato JSON
oc get network.config.openshift.io cluster -o jsonpath='{.spec.networkType}'
```

```bash
# Exibir recurso em formato JSON
oc get network.config.openshift.io cluster -o jsonpath='{.spec.clusterNetwork}'
```

```bash
# Exibir recurso em formato JSON
oc get network.config.openshift.io cluster -o jsonpath='{.spec.serviceNetwork}'
```

```bash
# Ver network operator
# oc get clusteroperator <resource-name>
oc get clusteroperator network
```

```bash
# Exibir recurso em formato YAML
oc get network.operator.openshift.io cluster -o yaml
```

### Pod Network
```bash ignore-test
# Exibir recurso em formato JSON
oc get network.config.openshift.io cluster -o jsonpath='{.spec.clusterNetwork[*].cidr}'
```

```bash ignore-test
# Exibir recurso em formato JSON
oc get network.config.openshift.io cluster -o jsonpath='{.spec.serviceNetwork[*]}'
```

```bash ignore-test
# Ver IP de um pod
oc get pod <pod-name> -o jsonpath='{.status.podIP}'
```

```bash
# Listar pods de todos os namespaces do cluster
oc get pods -o wide -A
```

```bash ignore-test
# Listar pods de todos os namespaces do cluster
oc get pods -A -o json | jq -r '.items[].status.podIP' | sort -V | uniq
```

## Ingress Controllers


### Listar Ingress Controllers
```bash
# Listar IngressControllers
oc get ingresscontroller -n openshift-ingress-operator
```

```bash
# Exibir detalhes completos do recurso
# oc describe ingresscontroller -n <namespace> default
oc describe ingresscontroller -n openshift-ingress-operator default
```

### Escalar Ingress Controller
```bash
# Ajustar número de réplicas do deployment/replicaset
# oc scale ingresscontroller -n openshift-ingress-operator --replicas=<N> default
oc scale ingresscontroller -n openshift-ingress-operator --replicas=2 default
```
---

## Network Policies

### Criar Network Policies
```bash
# Listar políticas de rede configuradas no namespace
oc get networkpolicy
oc get netpol
```

```bash ignore-test
# Exibir detalhes completos do network policy
# oc describe networkpolicy <resource-name>
oc describe networkpolicy test-app
```

```bash
# Aplicar configuração do arquivo YAML/JSON ao cluster
cat <<EOF | oc apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF
```

```bash
# Aplicar configuração do arquivo YAML/JSON ao cluster
cat <<EOF | oc apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-same-namespace
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector: {}
EOF
```

```bash
# Aplicar configuração do arquivo YAML/JSON ao cluster
cat <<EOF | oc apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-monitoring
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: openshift-monitoring
EOF
```

### Testar Network Policies
```bash ignore-test
# Antes de aplicar policy, testar conectividade
oc run test-pod --image=quay.io/chiaretto/netshoot --rm -it --restart=Never -- wget -O- <target-service>
```

```bash ignore-test
# Aplicar configuração do arquivo YAML/JSON ao cluster
oc apply -f networkpolicy.yaml
```

```bash ignore-test
# Testar novamente
oc run test-pod --image=quay.io/chiaretto/netshoot --rm -it --restart=Never -- wget -O- <target-service>
```

```bash ignore-test
# Verificar logs/eventos
oc get events | grep -i network
```

### Debugging Network Policies
```bash
# Exibir network policy em formato YAML
oc get networkpolicy -o yaml
```

```bash ignore-test
# Listar pods mostrando todas as labels associadas
oc get pods --show-labels
```

```bash ignore-test
# Exibir detalhes completos do network policy
# oc describe networkpolicy <resource-name>
oc describe networkpolicy test-app
```

```bash ignore-test
# Deletar o network policy especificado
# oc delete networkpolicy <resource-name>
oc delete networkpolicy test-app
```


## Configurações Avançadas

### Multus - Múltiplas Interfaces
```bash
# NetworkAttachmentDefinitions
oc get network-attachment-definitions
```

```bash
# Aplicar configuração do arquivo YAML/JSON ao cluster
cat <<EOF | oc apply -f -
apiVersion: k8s.cni.cncf.io/v1
kind: NetworkAttachmentDefinition
metadata:
  name: macvlan-conf
spec:
  config: '{
    "cniVersion": "0.3.1",
    "type": "macvlan",
    "master": "eth0",
    "mode": "bridge",
    "ipam": {
      "type": "host-local",
      "subnet": "192.168.1.0/24",
      "rangeStart": "192.168.1.200",
      "rangeEnd": "192.168.1.216",
      "gateway": "192.168.1.1"
    }
  }'
EOF
```

```bash
# Usar em pod
# annotations:
# k8s.v1.cni.cncf.io/networks: macvlan-conf
```

### MTU Configuration
```bash
# Exibir recurso em formato JSON
oc get network.operator.openshift.io cluster -o jsonpath='{.spec.defaultNetwork.ovnKubernetesConfig.mtu}'
```

```bash ignore-test
# Executar comando dentro do pod especificado
oc exec my-pod -- ip link show eth0
```

### Network Diagnostics
```bash
# Listar nodes com informações detalhadas
oc get nodes -o wide
```

```bash ignore-test
# Aplicar configuração do arquivo YAML/JSON ao cluster
cat <<EOF | oc apply -f -
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: network-test
spec:
  selector:
    matchLabels:
      app: network-test
  template:
    metadata:
      labels:
        app: network-test
    spec:
      containers:
      - name: network-test
        image: quay.io/chiaretto/netshoot
        command: ["sleep", "infinity"]
EOF
```

```bash ignore-test
# Listar recurso filtrados por label
for pod in $(oc get pods -l app=network-test -o name); do
  echo "=== Testing from $pod ==="
  oc exec $pod -- ping -c 2 8.8.8.8
done
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking">Networking - Understanding networking</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/networking/multiple-networks">Networking - Multiple networks</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration">Post-installation configuration</a>
---

---

## Navegação

- [← Anterior: Certificados CSR](19-certificados-csr.md)
- [→ Próximo: Cluster Version e Updates](21-cluster-version-updates.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
