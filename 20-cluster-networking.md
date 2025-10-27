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
```markdown
**Ação:** Exibir recurso em formato YAML
```

```bash
oc get network.config.openshift.io cluster -o yaml
```

```markdown
**Ação:** Exibir recurso em formato JSON
```

```bash
oc get network.config.openshift.io cluster -o jsonpath='{.spec.networkType}'
```

```markdown
**Ação:** Exibir recurso em formato JSON
```

```bash
oc get network.config.openshift.io cluster -o jsonpath='{.spec.clusterNetwork}'
```

```markdown
**Ação:** Exibir recurso em formato JSON
```

```bash
oc get network.config.openshift.io cluster -o jsonpath='{.spec.serviceNetwork}'
```

```markdown
**Ação:** Ver network operator
**Exemplo:** `oc get clusteroperator <resource-name>`
```

```bash
oc get clusteroperator network
```

```markdown
**Ação:** Exibir recurso em formato YAML
```

```bash
oc get network.operator.openshift.io cluster -o yaml
```

### Pod Network
```markdown
**Ação:** Exibir recurso em formato JSON
```

```bash ignore-test
oc get network.config.openshift.io cluster -o jsonpath='{.spec.clusterNetwork[*].cidr}'
```

```markdown
**Ação:** Exibir recurso em formato JSON
```

```bash ignore-test
oc get network.config.openshift.io cluster -o jsonpath='{.spec.serviceNetwork[*]}'
```

```markdown
**Ação:** Ver IP de um pod
```

```bash ignore-test
oc get pod <pod-name> -o jsonpath='{.status.podIP}'
```

```markdown
**Ação:** Listar pods de todos os namespaces do cluster
```

```bash
oc get pods -o wide -A
```

```markdown
**Ação:** Listar pods de todos os namespaces do cluster
```

```bash ignore-test
oc get pods -A -o json | jq -r '.items[].status.podIP' | sort -V | uniq
```

## Ingress Controllers


### Listar Ingress Controllers
```markdown
**Ação:** Listar IngressControllers
```

```bash
oc get ingresscontroller -n openshift-ingress-operator
```

```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe ingresscontroller -n <namespace> default`
```

```bash
oc describe ingresscontroller -n openshift-ingress-operator default
```

### Escalar Ingress Controller
```markdown
**Ação:** Ajustar número de réplicas do deployment/replicaset
**Exemplo:** `oc scale ingresscontroller -n openshift-ingress-operator --replicas=<N> default`
```

```bash
oc scale ingresscontroller -n openshift-ingress-operator --replicas=2 default
```
---

## Network Policies

### Criar Network Policies
```markdown
**Ação:** Listar políticas de rede configuradas no namespace
```

```bash
oc get networkpolicy
oc get netpol
```

```markdown
**Ação:** Exibir detalhes completos do network policy
**Exemplo:** `oc describe networkpolicy <resource-name>`
```

```bash ignore-test
oc describe networkpolicy test-app
```

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash
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

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash
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

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash
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
```markdown
**Ação:** Antes de aplicar policy, testar conectividade
```

```bash ignore-test
oc run test-pod --image=quay.io/chiaretto/netshoot --rm -it --restart=Never -- wget -O- <target-service>
```

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash ignore-test
oc apply -f networkpolicy.yaml
```

```markdown
**Ação:** Testar novamente
```

```bash ignore-test
oc run test-pod --image=quay.io/chiaretto/netshoot --rm -it --restart=Never -- wget -O- <target-service>
```

```markdown
**Ação:** Verificar logs/eventos
```

```bash ignore-test
oc get events | grep -i network
```

### Debugging Network Policies
```markdown
**Ação:** Exibir network policy em formato YAML
```

```bash
oc get networkpolicy -o yaml
```

```markdown
**Ação:** Listar pods mostrando todas as labels associadas
```

```bash ignore-test
oc get pods --show-labels
```

```markdown
**Ação:** Exibir detalhes completos do network policy
**Exemplo:** `oc describe networkpolicy <resource-name>`
```

```bash ignore-test
oc describe networkpolicy test-app
```

```markdown
**Ação:** Deletar o network policy especificado
**Exemplo:** `oc delete networkpolicy <resource-name>`
```

```bash ignore-test
oc delete networkpolicy test-app
```


## Configurações Avançadas

### Multus - Múltiplas Interfaces
```markdown
**Ação:** NetworkAttachmentDefinitions
```

```bash
oc get network-attachment-definitions
```

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash
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
```markdown
**Ação:** Exibir recurso em formato JSON
```

```bash
oc get network.operator.openshift.io cluster -o jsonpath='{.spec.defaultNetwork.ovnKubernetesConfig.mtu}'
```

```markdown
**Ação:** Executar comando dentro do pod especificado
```

```bash ignore-test
oc exec my-pod -- ip link show eth0
```

### Network Diagnostics
```markdown
**Ação:** Listar nodes com informações detalhadas
```

```bash
oc get nodes -o wide
```

```markdown
**Ação:** Aplicar configuração do arquivo YAML/JSON ao cluster
```

```bash ignore-test
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

```markdown
**Ação:** Listar recurso filtrados por label
```

```bash ignore-test
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
