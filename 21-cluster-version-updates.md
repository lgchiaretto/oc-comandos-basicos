# Cluster Version e Updates

Este documento contém comandos para gerenciar versão e atualizações do cluster OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Cluster Version](#cluster-version)
3. [Updates](#updates)
4. [Update Channels](#update-channels)
5. [Troubleshooting Updates](#troubleshooting-updates)
6. [Documentação Oficial](#documentação-oficial)
7. [Navegação](#navegação)
---

## Cluster Version

### Ver Versão Atual
**Exibir versão e status de atualização do cluster**

```bash
oc get clusterversion
```

**Exibir detalhes completos do clusterversion**

```bash
oc describe clusterversion version
```

**Exibir versão desejada para o cluster**

```bash ignore-test
oc get clusterversion -o jsonpath='{.items[0].status.desired.version}{"\n"}'
```

**Exibir histórico de versões do cluster**

```bash ignore-test
oc get clusterversion -o jsonpath='{.items[0].status.history}' | jq .
```

**Exibir clusterversion usando JSONPath customizado**

```bash ignore-test
oc get clusterversion -o jsonpath='{.items[0].spec.clusterID}{"\n"}'
```

### Status do Cluster
**Exibir clusterversion em formato YAML completo**

```bash
oc get clusterversion version -o yaml
```

**Exibir status da progressão da atualização**

```bash ignore-test
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].status}{"\n"}'
```

**Exibir mensagem da progressão da atualização**

```bash ignore-test
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].message}{"\n"}'
```

**Percentage de update**

```bash
oc adm upgrade
```

**Exibir versão e status de atualização do cluster**

```bash
oc get clusterversion
```

---

## Updates

### Verificar Updates Disponíveis
**Ver updates disponíveis**

```bash
oc adm upgrade
```

**Listar todas as versões disponíveis**

```bash
oc adm upgrade --to-latest=false
```

**Exibir canal de atualização configurado**

```bash ignore-test
oc get clusterversion -o jsonpath='{.items[0].spec.channel}{"\n"}'
```

### Iniciar Update
**Update para última versão do canal**

```bash ignore-test
oc adm upgrade --to-latest=true
```

**Update para versão específica**

```bash ignore-test
oc adm upgrade --to=<version>
```

**Exemplo**

```bash ignore-test
oc adm upgrade --to=4.19.15
```

**Update forçado (não recomendado)**

```bash ignore-test
oc adm upgrade --to=<version> --force --allow-upgrade-with-warnings
```

### Monitorar Update
**Status do update**

```bash
oc get clusterversion
```

**Listar status de todos os cluster operators**

```bash
oc get co
```

**Operators com problema**

```bash
oc get co | grep -v "True.*False.*False"
```

**Logs de um operator específico**

```bash ignore-test
oc logs -n <operator-namespace> <operator-pod>
```

**Exibir detalhes completos do recurso**

```bash
oc describe clusterversion
```

**Exibir clusterversion em formato JSON completo**

```bash ignore-test
oc get clusterversion -o json | jq '.items[0].status.history'
```

---

## Update Channels

### Ver e Mudar Channel
**Exibir clusterversion usando JSONPath customizado**

```bash
oc get clusterversion version -o jsonpath='{.spec.channel}{"\n"}'
```

```bash
# Canais disponíveis (exemplo para 4.19)
# - stable-4.19
# - fast-4.19
# - eus-4.19 (Extended Update Support)
# - candidate-4.19
```
**Aplicar modificação parcial ao recurso usando patch**

```bash
oc patch clusterversion version --type merge -p '{"spec":{"channel":"stable-4.19"}}'
```

**Aplicar modificação parcial ao recurso usando patch**

```bash
oc patch clusterversion version --type merge -p '{"spec":{"channel":"fast-4.19"}}'
```

**Aplicar modificação parcial ao recurso usando patch**

```bash
oc patch clusterversion version --type merge -p '{"spec":{"channel":"eus-4.19"}}'
```

**Exibir canal de atualização configurado**

```bash
oc get clusterversion -o jsonpath='{.items[0].spec.channel}{"\n"}'
```

**Ver novos updates disponíveis**

```bash
oc adm upgrade
```

### Upstream Update Server
**Exibir clusterversion usando JSONPath customizado**

```bash
oc get clusterversion version -o jsonpath='{.spec.upstream}{"\n"}'
```

---

## Troubleshooting Updates

### Update Stuck ou Falhando
**Exibir detalhes completos do recurso**

```bash
oc describe clusterversion
```

**Ver qual operator está com problema**

```bash
oc get co | grep -v "True.*False.*False"
```

**Descrever operator problemático**

```bash ignore-test
oc describe co <operator-name>
```

**Ver mensagem de erro**

```bash ignore-test
oc get co <operator-name> -o jsonpath='{.status.conditions[?(@.type=="Degraded")].message}{"\n"}'
```

**Ver pods do operator**

```bash ignore-test
oc get pods -n <operator-namespace>
```

**Logs do operator**

```bash ignore-test
oc logs -n <operator-namespace> <pod-name>
```

**Ver eventos**

```bash ignore-test
oc get events -n <operator-namespace> --sort-by='.lastTimestamp'
```

**Exibir status da progressão da atualização**

```bash
oc get clusterversion -o jsonpath='{.items[0].status.conditions[?(@.type=="Progressing")].status}{"\n"}'
```

### Rollback (Não Suportado Oficialmente)
```bash
# OpenShift NÃO suporta rollback
# Se update falhar, o cluster permanece na versão atual e você precisa abrir um chamado na Red Hat
```
**Exibir recurso em formato JSON**

```bash
echo "Current: $(oc get clusterversion -o jsonpath='{.items[0].status.history[0].version}')"
echo "Desired: $(oc get clusterversion -o jsonpath='{.items[0].status.desired.version}')"
```

### Update Prerequisites
**Verificar saúde antes de update**

```bash
echo "=== Cluster Operators ==="
oc get co
```

```bash
echo -e "\n=== Nodes ==="
oc get nodes
```

```bash
echo -e "\n=== Degraded Pods ==="
oc get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded
```

```bash
echo -e "\n=== Cluster Version ==="
oc get clusterversion
```

```bash
echo -e "\n=== MachineConfigPools ==="
oc get mcp
```

**Script de verificação**

```bash
cat > /tmp/pre-update-check.sh << 'EOF'
#!/bin/bash
echo "=== Pre-Update Health Check ==="
echo ""
```

**Exibir cluster operator em formato JSON**

```bash
DEGRADED=$(oc get co -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Degraded" and .status=="True")) | .metadata.name' | wc -l)
echo "Degraded Operators: $DEGRADED"
```

**Exibir nodes em formato JSON**

```bash
NOT_READY=$(oc get nodes -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Ready" and .status!="True")) | .metadata.name' | wc -l)
echo "Not Ready Nodes: $NOT_READY"
```

**Listar pods de todos os namespaces do cluster**

```bash
BAD_PODS=$(oc get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded -o json | jq '.items | length')
echo "Non-Running Pods: $BAD_PODS"
```

**Exibir recurso em formato JSON**

```bash
UPDATING_MCP=$(oc get mcp -o json | jq -r '.items[] | select(.status.conditions[] | select(.type=="Updating" and .status=="True")) | .metadata.name' | wc -l)
echo "Updating MCPs: $UPDATING_MCP"
```

```bash
echo ""
if [ $DEGRADED -eq 0 ] && [ $NOT_READY -eq 0 ] && [ $BAD_PODS -eq 0 ] && [ $UPDATING_MCP -eq 0 ]; then
  echo " Cluster is healthy for update"
  exit 0
else
  echo " Cluster has issues - investigate before updating"
  exit 1
fi
EOF
```

```bash
chmod +x /tmp/pre-update-check.sh
/tmp/pre-update-check.sh
```

### Cincinnati Graph
**Exibir recurso "version" em formato JSON**

```bash
CLUSTER_ID=$(oc get clusterversion version -o jsonpath='{.spec.clusterID}')
CURRENT_VERSION=$(oc get clusterversion version -o jsonpath='{.status.desired.version}')
CHANNEL=$(oc get clusterversion version -o jsonpath='{.spec.channel}')
```

```bash ignore-test
curl -sH "Accept: application/json" \
  "https://api.openshift.com/api/upgrades_info/v1/graph?channel=${CHANNEL}&id=${CLUSTER_ID}"
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/updating_clusters">Updating clusters</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration">Post-installation configuration</a>
---


## Navegação

- [← Anterior: Cluster Networking](20-cluster-networking.md)
- [→ Próximo: Etcd e Backup](22-etcd-backup.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Dezembro 2025
