# 🌐 Cluster Networking

Este documento contém comandos para configuração e troubleshooting de rede do cluster OpenShift.

---

## 📋 Índice

1. [Configuração de Rede](#configuração-de-rede)
2. [Network Policies](#network-policies)
3. [Egress](#egress)
4. [Service Mesh](#service-mesh)

---

## ⚙️ Configuração de Rede

### Visualizar Configuração
```bash
# Ver configuração de rede do cluster
oc get network.config.openshift.io cluster -o yaml

# Tipo de rede (SDN ou OVN)
oc get network.config.openshift.io cluster -o jsonpath='{.spec.networkType}'

# Ver cluster network
oc get network.config.openshift.io cluster -o jsonpath='{.spec.clusterNetwork}'

# Ver service network
oc get network.config.openshift.io cluster -o jsonpath='{.spec.serviceNetwork}'

# Ver network operator
oc get clusteroperator network

# Network operator config
oc get network.operator.openshift.io cluster -o yaml
```

### Pod Network
```bash
# Ver CIDR dos pods
oc get network.config.openshift.io cluster -o jsonpath='{.spec.clusterNetwork[*].cidr}'

# Ver CIDR dos services
oc get network.config.openshift.io cluster -o jsonpath='{.spec.serviceNetwork[*]}'

# Ver IP de um pod
oc get pod <pod-name> -o jsonpath='{.status.podIP}'

# Ver IPs de todos os pods
oc get pods -o wide -A

# Verificar range de IPs usado
oc get pods -A -o json | jq -r '.items[].status.podIP' | sort -V | uniq
```

---

## 🛡️ Network Policies

### Criar Network Policies
```bash
# Listar network policies
oc get networkpolicy
oc get netpol

# Descrever policy
oc describe networkpolicy <nome>

# Deny all por padrão
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

# Allow específico
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

# Allow de namespace específico
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
```bash
# Antes de aplicar policy, testar conectividade
oc run test-pod --image=busybox --rm -it --restart=Never -- wget -O- <target-service>

# Aplicar policy
oc apply -f networkpolicy.yaml

# Testar novamente
oc run test-pod --image=busybox --rm -it --restart=Never -- wget -O- <target-service>

# Verificar logs/eventos
oc get events | grep -i network
```

### Debugging Network Policies
```bash
# Ver todas as policies do namespace
oc get networkpolicy -o yaml

# Ver labels dos pods
oc get pods --show-labels

# Ver se policy está afetando pod
oc describe networkpolicy <nome>

# Deletar temporariamente para testar
oc delete networkpolicy <nome>
```

---

## 🚪 Egress

### Egress IP
```bash
# Ver EgressIPs
oc get egressip

# Configurar Egress IP
cat <<EOF | oc apply -f -
apiVersion: k8s.ovn.org/v1
kind: EgressIP
metadata:
  name: egressip-prod
spec:
  egressIPs:
  - 192.168.1.100
  namespaceSelector:
    matchLabels:
      env: production
EOF

# Ver status
oc describe egressip <nome>

# Verificar em qual node está
oc get egressip <nome> -o yaml
```

### Egress Router (Legacy - SDN)
```bash
# Criar egress router pod
oc create -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: egress-router
  labels:
    name: egress-router
  annotations:
    pod.network.openshift.io/assign-macvlan: "true"
spec:
  initContainers:
  - name: egress-router-setup
    image: registry.redhat.io/openshift4/ose-egress-router
    securityContext:
      privileged: true
    env:
    - name: EGRESS_SOURCE
      value: "192.168.1.99/24"
    - name: EGRESS_GATEWAY
      value: "192.168.1.1"
    - name: EGRESS_DESTINATION
      value: "203.0.113.25"
  containers:
  - name: egress-router
    image: registry.redhat.io/openshift4/ose-egress-router
    securityContext:
      privileged: true
EOF
```

### Egress Firewall (OVN)
```bash
# Criar Egress Firewall
cat <<EOF | oc apply -f -
apiVersion: k8s.ovn.org/v1
kind: EgressFirewall
metadata:
  name: default
spec:
  egress:
  - type: Allow
    to:
      cidrSelector: 1.2.3.0/24
  - type: Deny
    to:
      cidrSelector: 0.0.0.0/0
EOF

# Ver Egress Firewall
oc get egressfirewall

# Descrever
oc describe egressfirewall default
```

---

## 🕸️ Service Mesh

### Istio/Service Mesh
```bash
# Verificar Service Mesh operator
oc get csv -n openshift-operators | grep servicemesh

# ServiceMeshControlPlane
oc get servicemeshcontrolplane -n istio-system

# ServiceMeshMemberRoll
oc get servicemeshmemberroll -n istio-system

# Pods do Service Mesh
oc get pods -n istio-system

# Ver sidecar injection
oc get deployment <nome> -o yaml | grep sidecar.istio.io/inject
```

### Habilitar Sidecar Injection
```bash
# Annotation no namespace
oc label namespace <namespace> istio-injection=enabled

# Adicionar ao member roll
oc patch servicemeshmemberroll default -n istio-system --type='json' -p='[{"op": "add", "path": "/spec/members/-", "value": "<namespace>"}]'

# Verificar
oc get servicemeshmemberroll default -n istio-system -o yaml
```

### Traffic Management
```bash
# VirtualServices
oc get virtualservice -n <namespace>

# DestinationRules
oc get destinationrule -n <namespace>

# Gateways
oc get gateway -n <namespace>

# Ver configuração Envoy
oc exec <pod-name> -c istio-proxy -- pilot-agent request GET config_dump
```

---

## 🔧 Configurações Avançadas

### Multus - Múltiplas Interfaces
```bash
# NetworkAttachmentDefinitions
oc get network-attachment-definitions

# Criar NAD
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

# Usar em pod
# annotations:
#   k8s.v1.cni.cncf.io/networks: macvlan-conf
```

### MTU Configuration
```bash
# Ver MTU configurado
oc get network.operator.openshift.io cluster -o jsonpath='{.spec.defaultNetwork.ovnKubernetesConfig.mtu}'

# Ou para SDN
oc get network.operator.openshift.io cluster -o jsonpath='{.spec.defaultNetwork.openshiftSDNConfig.mtu}'

# Verificar MTU em pod
oc exec <pod-name> -- ip link show eth0
```

### Network Diagnostics
```bash
# Verificar conectividade entre nodes
oc get nodes -o wide

# Criar DaemonSet de teste
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
        image: nicolaka/netshoot
        command: ["sleep", "infinity"]
EOF

# Testar de cada node
for pod in $(oc get pods -l app=network-test -o name); do
  echo "=== Testing from $pod ==="
  oc exec $pod -- ping -c 2 8.8.8.8
done
```

---

## 📖 Navegação

- [← Anterior: Certificados CSR](19-certificados-csr.md)
- [→ Próximo: Cluster Version e Updates](21-cluster-version-updates.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
