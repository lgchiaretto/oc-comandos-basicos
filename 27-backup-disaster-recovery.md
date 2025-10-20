# 🔄 Backup e Disaster Recovery

Este documento contém estratégias e comandos para backup e recuperação de desastres no OpenShift.

---

## 📋 Índice

1. [Estratégia de Backup](#estratégia-de-backup)
2. [Backup de Aplicações](#backup-de-aplicações)
3. [Backup de Dados](#backup-de-dados)
4. [Disaster Recovery](#disaster-recovery)

---

## 📝 Estratégia de Backup

### O que Fazer Backup
```bash
# 1. ETCD (Cluster state) - JÁ COBERTO em 22-etcd-backup.md
# 2. Persistent Volumes (Dados de aplicações)
# 3. Manifests e Configurações
# 4. Secrets e ConfigMaps
# 5. Registry Images
# 6. Operator configurations
```

### Frequência Recomendada
```bash
# Diário:
# - Etcd backup
# - Application manifests
# - Secrets/ConfigMaps

# Semanal:
# - Full PV backup
# - Registry images backup

# Antes de:
# - Cluster updates
# - Major changes
# - Operator updates
```

---

## 💼 Backup de Aplicações

### Backup de Manifests por Namespace
```bash
# Script completo de backup de namespace
cat > /tmp/backup-namespace.sh << 'EOF'
#!/bin/bash
set -e

NAMESPACE=$1
BACKUP_DIR="namespace-backup-${NAMESPACE}-$(date +%Y%m%d-%H%M%S)"

if [ -z "$NAMESPACE" ]; then
  echo "Usage: $0 <namespace>"
  exit 1
fi

echo "=== Backing up namespace: ${NAMESPACE} ==="
mkdir -p ${BACKUP_DIR}

# Resources to backup
RESOURCES=(
  "deployments"
  "statefulsets"
  "daemonsets"
  "services"
  "routes"
  "configmaps"
  "secrets"
  "persistentvolumeclaims"
  "serviceaccounts"
  "roles"
  "rolebindings"
  "networkpolicies"
  "horizontalpodautoscalers"
  "imagestreams"
  "buildconfigs"
  "deploymentconfigs"
)

for resource in "${RESOURCES[@]}"; do
  echo "Backing up ${resource}..."
  oc get ${resource} -n ${NAMESPACE} -o yaml > ${BACKUP_DIR}/${resource}.yaml 2>/dev/null || true
done

# Backup namespace itself
oc get namespace ${NAMESPACE} -o yaml > ${BACKUP_DIR}/namespace.yaml

# Compress
tar czf ${BACKUP_DIR}.tar.gz ${BACKUP_DIR}/
rm -rf ${BACKUP_DIR}

echo "✅ Backup completed: ${BACKUP_DIR}.tar.gz"
ls -lh ${BACKUP_DIR}.tar.gz
EOF

chmod +x /tmp/backup-namespace.sh

# Usar
/tmp/backup-namespace.sh myproject
```

### Backup de Todo o Cluster (Manifests)
```bash
# Script para backup de todos os namespaces
cat > /tmp/backup-all-namespaces.sh << 'EOF'
#!/bin/bash
set -e

BACKUP_DIR="cluster-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p ${BACKUP_DIR}

echo "=== Cluster-wide resources ==="
mkdir -p ${BACKUP_DIR}/cluster

# Cluster-scoped resources
oc get namespaces -o yaml > ${BACKUP_DIR}/cluster/namespaces.yaml
oc get nodes -o yaml > ${BACKUP_DIR}/cluster/nodes.yaml
oc get clusterroles -o yaml > ${BACKUP_DIR}/cluster/clusterroles.yaml
oc get clusterrolebindings -o yaml > ${BACKUP_DIR}/cluster/clusterrolebindings.yaml
oc get storageclasses -o yaml > ${BACKUP_DIR}/cluster/storageclasses.yaml
oc get persistentvolumes -o yaml > ${BACKUP_DIR}/cluster/persistentvolumes.yaml
oc get customresourcedefinitions -o yaml > ${BACKUP_DIR}/cluster/crds.yaml

echo "=== Backing up user namespaces ==="
for ns in $(oc get ns -o jsonpath='{.items[?(@.metadata.name!~"^(openshift|kube|default).*")].metadata.name}'); do
  echo "Namespace: $ns"
  /tmp/backup-namespace.sh $ns
  mv namespace-backup-${ns}-*.tar.gz ${BACKUP_DIR}/
done

# Compress everything
tar czf ${BACKUP_DIR}.tar.gz ${BACKUP_DIR}/
rm -rf ${BACKUP_DIR}

echo "✅ Full cluster backup: ${BACKUP_DIR}.tar.gz"
EOF

chmod +x /tmp/backup-all-namespaces.sh
```

### Velero - Backup Tool
```bash
# Instalar Velero Operator
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: redhat-oadp-operator
  namespace: openshift-adp
spec:
  channel: stable-1.3
  name: redhat-oadp-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
EOF

# Aguardar instalação
oc get csv -n openshift-adp

# Configurar DataProtectionApplication
cat <<EOF | oc apply -f -
apiVersion: oadp.openshift.io/v1alpha1
kind: DataProtectionApplication
metadata:
  name: velero
  namespace: openshift-adp
spec:
  configuration:
    velero:
      defaultPlugins:
      - openshift
      - aws
    restic:
      enable: true
  backupLocations:
  - velero:
      provider: aws
      default: true
      credential:
        name: cloud-credentials
        key: cloud
      config:
        region: us-east-1
        s3ForcePathStyle: "true"
        s3Url: https://s3.amazonaws.com
      objectStorage:
        bucket: my-backup-bucket
        prefix: velero
EOF

# Criar backup com Velero
velero backup create my-backup --include-namespaces myproject

# Listar backups
velero backup get

# Restore
velero restore create --from-backup my-backup
```

---

## 💾 Backup de Dados

### Backup de PVCs
```bash
# Snapshot de PVC (se StorageClass suportar)
cat <<EOF | oc apply -f -
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: pvc-snapshot
spec:
  volumeSnapshotClassName: <snapshot-class>
  source:
    persistentVolumeClaimName: <pvc-name>
EOF

# Verificar snapshot
oc get volumesnapshot

# Restore de snapshot
cat <<EOF | oc apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: restored-pvc
spec:
  dataSource:
    name: pvc-snapshot
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
EOF
```

### Backup Manual de Dados em PVC
```bash
# Criar pod temporário para acessar PVC
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: backup-pod
spec:
  containers:
  - name: backup
    image: registry.redhat.io/rhel8/support-tools
    command: ["sleep", "infinity"]
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: <pvc-name>
EOF

# Aguardar pod ficar ready
oc wait --for=condition=ready pod/backup-pod

# Tar dos dados
oc exec backup-pod -- tar czf /tmp/backup.tar.gz /data

# Copiar backup
oc cp backup-pod:/tmp/backup.tar.gz ./pvc-backup.tar.gz

# Limpeza
oc delete pod backup-pod
```

### Backup de Database
```bash
# MySQL/MariaDB
oc exec <mysql-pod> -- mysqldump -u root -p<password> --all-databases > mysql-backup.sql

# PostgreSQL
oc exec <postgres-pod> -- pg_dumpall -U postgres > postgres-backup.sql

# MongoDB
oc exec <mongodb-pod> -- mongodump --archive > mongodb-backup.archive

# Restore (exemplos)
oc exec -i <mysql-pod> -- mysql -u root -p<password> < mysql-backup.sql
oc exec -i <postgres-pod> -- psql -U postgres < postgres-backup.sql
oc exec -i <mongodb-pod> -- mongorestore --archive < mongodb-backup.archive
```

---

## 🚨 Disaster Recovery

### Preparação para DR
```bash
# Checklist de preparação
cat > /tmp/dr-checklist.md << 'EOF'
# Disaster Recovery Checklist

## Backups Configurados
- [ ] Etcd backup diário
- [ ] Application manifests backup
- [ ] PV snapshots ou backup
- [ ] Database backups
- [ ] Registry images backup
- [ ] Cluster configuration backup

## Documentação
- [ ] Procedimentos de restore documentados
- [ ] Lista de contatos de emergência
- [ ] Diagrama de arquitetura atualizado
- [ ] Inventário de aplicações críticas
- [ ] RTO/RPO definidos por aplicação

## Testes
- [ ] Teste de restore de etcd
- [ ] Teste de restore de aplicações
- [ ] Teste de restore de dados
- [ ] DR drill completo (anual)

## Armazenamento
- [ ] Backups em localização offsite
- [ ] Backups encriptados
- [ ] Retenção de backups configurada
- [ ] Verificação de integridade automática
EOF

cat /tmp/dr-checklist.md
```

### Restore de Aplicação
```bash
# 1. Restore de namespace
tar xzf namespace-backup-myproject-*.tar.gz
cd namespace-backup-myproject-*/

# 2. Criar namespace
oc apply -f namespace.yaml

# 3. Restore de secrets e configmaps primeiro
oc apply -f secrets.yaml
oc apply -f configmaps.yaml

# 4. Restore de PVCs
oc apply -f persistentvolumeclaims.yaml

# 5. Aguardar PVCs bound
oc get pvc

# 6. Restore de service accounts e RBAC
oc apply -f serviceaccounts.yaml
oc apply -f roles.yaml
oc apply -f rolebindings.yaml

# 7. Restore de applications
oc apply -f deployments.yaml
oc apply -f statefulsets.yaml
oc apply -f services.yaml
oc apply -f routes.yaml

# 8. Verificar
oc get all
```

### DR em Ambiente Secundário
```bash
# Failover para cluster secundário

# 1. Confirmar cluster primário está down
oc get clusterversion # timeout se cluster está down

# 2. No cluster secundário, restore do etcd backup
# (ver 22-etcd-backup.md)

# 3. Restore de aplicações
for backup in namespace-backup-*.tar.gz; do
  tar xzf $backup
  # Aplicar manifests...
done

# 4. Atualizar DNS para apontar para novo cluster
# (fora do escopo do OpenShift)

# 5. Verificar aplicações
oc get pods -A
oc get routes -A

# 6. Testar aplicações críticas
```

### RPO/RTO
```bash
# Recovery Point Objective (RPO)
# = Quanto de dados você pode perder
# Exemplo: Backup a cada 1h = RPO de 1h

# Recovery Time Objective (RTO)
# = Quanto tempo para recuperar
# Exemplo: Restore em 30min = RTO de 30min

# Medir RPO real
LAST_BACKUP=$(ls -t cluster-backup-*.tar.gz | head -1)
BACKUP_TIME=$(stat -c %Y $LAST_BACKUP)
CURRENT_TIME=$(date +%s)
AGE_HOURS=$(( ($CURRENT_TIME - $BACKUP_TIME) / 3600 ))
echo "Last backup was $AGE_HOURS hours ago"
echo "Current RPO: ${AGE_HOURS}h"
```

---

## 📖 Navegação

- [← Anterior: Templates e Manifests](26-templates-manifests.md)
- [→ Próximo: Patch e Edit](28-patch-edit.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
