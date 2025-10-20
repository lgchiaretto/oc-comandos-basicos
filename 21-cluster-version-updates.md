# 🔄 Cluster Version e Updates

Este documento contém comandos para gerenciar versão e atualizações do cluster OpenShift.

---

## 📋 Índice

1. [Cluster Version](#cluster-version)
2. [Updates](#updates)
3. [Update Channels](#update-channels)
4. [Troubleshooting Updates](#troubleshooting-updates)

---

## 📌 Cluster Version

### Ver Versão Atual
```bash
# Versão do cluster
oc get clusterversion

# Detalhes da versão
oc describe clusterversion version

# Versão em formato compacto
oc get clusterversion -o jsonpath='{.items[0].status.desired.version}{"\n"}'

# Ver histórico de updates
oc get clusterversion -o jsonpath='{.items[0].status.history}' | jq .

# Cluster ID
oc get clusterversion -o jsonpath='{.items[0].spec.clusterID}{"\n"}'
```

### Status do Cluster
```bash
# Status geral
oc get clusterversion version -o yaml

# Ver se está updating
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].status}{"\n"}'

# Ver mensagem de progresso
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].message}{"\n"}'

# Percentage de update
oc adm upgrade

# Watch do update
oc get clusterversion
```

---

## ⬆️ Updates

### Verificar Updates Disponíveis
```bash
# Ver updates disponíveis
oc adm upgrade

# Listar todas as versões disponíveis
oc adm upgrade --to-latest=false

# Ver canal atual
oc get clusterversion -o jsonpath='{.items[0].spec.channel}{"\n"}'
```

### Iniciar Update
```bash
# Update para última versão do canal
oc adm upgrade --to-latest=true

# Update para versão específica
oc adm upgrade --to=<version>

# Exemplo
oc adm upgrade --to=4.14.15

# Update forçado (não recomendado)
oc adm upgrade --to=<version> --force --allow-upgrade-with-warnings
```

### Monitorar Update
```bash
# Status do update
oc get clusterversion

# Ver Cluster Operators atualizando
oc get co

# Operators com problema
oc get co | grep -v "True.*False.*False"

# Logs de um operator específico
oc logs -n <operator-namespace> <operator-pod>

# Ver progresso detalhado
oc describe clusterversion

# Histórico completo
oc get clusterversion -o json | jq '.items[0].status.history'
```

---

## 📺 Update Channels

### Ver e Mudar Channel
```bash
# Ver canal atual
oc get clusterversion version -o jsonpath='{.spec.channel}{"\n"}'

# Canais disponíveis (exemplo para 4.14)
# - stable-4.14
# - fast-4.14
# - eus-4.14 (Extended Update Support)
# - candidate-4.14

# Mudar para stable
oc patch clusterversion version --type merge -p '{"spec":{"channel":"stable-4.14"}}'

# Mudar para fast
oc patch clusterversion version --type merge -p '{"spec":{"channel":"fast-4.14"}}'

# Mudar para EUS
oc patch clusterversion version --type merge -p '{"spec":{"channel":"eus-4.14"}}'

# Verificar mudança
oc get clusterversion -o jsonpath='{.items[0].spec.channel}{"\n"}'

# Ver novos updates disponíveis
oc adm upgrade
```

### Upstream Update Server
```bash
# Ver upstream configurado
oc get clusterversion version -o jsonpath='{.spec.upstream}{"\n"}'

# Configurar upstream customizado (disconnected)
oc patch clusterversion version --type merge -p '{"spec":{"upstream":"<update-server-url>"}}'
```

---

## 🔧 Troubleshooting Updates

### Update Stuck ou Falhando
```bash
# Ver status detalhado
oc describe clusterversion

# Ver qual operator está com problema
oc get co | grep -v "True.*False.*False"

# Descrever operator problemático
oc describe co <operator-name>

# Ver mensagem de erro
oc get co <operator-name> -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}{"\n"}'

# Ver pods do operator
oc get pods -n <operator-namespace>

# Logs do operator
oc logs -n <operator-namespace> <pod-name>

# Ver eventos
oc get events -n <operator-namespace> --sort-by='.lastTimestamp'
```

### Pausar Update
```bash
# Não há comando nativo para pausar
# Mas pode-se deletar ClusterVersion para "congelar"
# NÃO RECOMENDADO EM PRODUÇÃO!

# Ver se cluster está em update
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].status}{"\n"}'
```

### Rollback (Não Suportado Oficialmente)
```bash
# OpenShift NÃO suporta rollback
# Se update falhar, o cluster permanece na versão atual

# Ver versão atual vs desejada
echo "Current: $(oc get clusterversion -o jsonpath='{.items[0].status.history[0].version}')"
echo "Desired: $(oc get clusterversion -o jsonpath='{.items[0].status.desired.version}')"

# Se precisar "reverter", a única opção é:
# 1. Restaurar etcd backup
# 2. Reinstalar cluster
# (Por isso sempre fazer backup antes de update!)
```

### Update Prerequisites
```bash
# Verificar saúde antes de update
echo "=== Cluster Operators ==="
oc get co

echo -e "\n=== Nodes ==="
oc get nodes

echo -e "\n=== Degraded Pods ==="
oc get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded

echo -e "\n=== Cluster Version ==="
oc get clusterversion

echo -e "\n=== MachineConfigPools ==="
oc get mcp

# Script de verificação
cat > /tmp/pre-update-check.sh << 'EOF'
#!/bin/bash
echo "=== Pre-Update Health Check ==="
echo ""

# Cluster Operators
DEGRADED=$(oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name' | wc -l)
echo "Degraded Operators: $DEGRADED"

# Nodes
NOT_READY=$(oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name' | wc -l)
echo "Not Ready Nodes: $NOT_READY"

# Pods
BAD_PODS=$(oc get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded -o json | jq '.items | length')
echo "Non-Running Pods: $BAD_PODS"

# MCPs
UPDATING_MCP=$(oc get mcp -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Updating" and .status=="True")) | .metadata.name' | wc -l)
echo "Updating MCPs: $UPDATING_MCP"

echo ""
if [ $DEGRADED -eq 0 ] && [ $NOT_READY -eq 0 ] && [ $BAD_PODS -eq 0 ] && [ $UPDATING_MCP -eq 0 ]; then
  echo "✅ Cluster is healthy for update"
  exit 0
else
  echo "❌ Cluster has issues - investigate before updating"
  exit 1
fi
EOF

chmod +x /tmp/pre-update-check.sh
/tmp/pre-update-check.sh
```

### Cincinnati Graph
```bash
# Ver graph de updates disponíveis (com cluster UUID)
CLUSTER_ID=$(oc get clusterversion version -o jsonpath='{.spec.clusterID}')
CURRENT_VERSION=$(oc get clusterversion version -o jsonpath='{.status.desired.version}')
CHANNEL=$(oc get clusterversion version -o jsonpath='{.spec.channel}')

curl -sH "Accept: application/json" \
  "https://api.openshift.com/api/upgrades_info/v1/graph?channel=${CHANNEL}&id=${CLUSTER_ID}"
```

---

## 📖 Navegação

- [← Anterior: Cluster Networking](20-cluster-networking.md)
- [→ Próximo: Etcd e Backup](22-etcd-backup.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
