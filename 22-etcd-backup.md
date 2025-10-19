# 💾 Etcd e Backup

Este documento contém comandos para gerenciar etcd e realizar backups do cluster OpenShift.

---

## 📋 Índice

1. [Etcd Status](#etcd-status)
2. [Backup do Cluster](#backup-do-cluster)
3. [Restore](#restore)
4. [Etcd Defrag](#etcd-defrag)

---

## 🔍 Etcd Status

### Verificar Etcd
```bash
# Pods do etcd
oc get pods -n openshift-etcd

# Ver etcd members
oc get pods -n openshift-etcd -l app=etcd -o wide

# Status do etcd operator
oc get clusteroperator etcd

# Descrever etcd operator
oc describe co etcd

# Logs do etcd
oc logs -n openshift-etcd <etcd-pod-name>

# Logs do etcd-operator
oc logs -n openshift-etcd-operator <etcd-operator-pod>
```

### Etcd Health Check
```bash
# Executar dentro de pod etcd
oc rsh -n openshift-etcd <etcd-pod-name>

# Dentro do pod:
etcdctl endpoint health --cluster
etcdctl endpoint status --cluster -w table
etcdctl member list -w table

# Ou diretamente:
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl endpoint health --cluster

# Ver tamanho do etcd
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl endpoint status --cluster -w table

# Verificar alarmes
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl alarm list
```

---

## 💾 Backup do Cluster

### Backup Manual do Etcd
```bash
# Conectar a um master node
oc debug node/<master-node-name>

# No debug shell:
chroot /host

# Executar backup
/usr/local/bin/cluster-backup.sh /home/core/backup

# Verificar backup criado
ls -lh /home/core/backup/

# Sair do debug
exit
exit

# Copiar backup do node
oc rsync <master-node-name>:/home/core/backup/ ./cluster-backup/
```

### Script Automatizado de Backup
```bash
# Criar script de backup
cat > /tmp/etcd-backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="/home/core/backup-${DATE}"
MASTER_NODE=$(oc get nodes -l node-role.kubernetes.io/master -o jsonpath='{.items[0].metadata.name}')

echo "=== Starting etcd backup at $(date) ==="
echo "Master node: ${MASTER_NODE}"
echo "Backup dir: ${BACKUP_DIR}"

# Executar backup
oc debug node/${MASTER_NODE} -- chroot /host /usr/local/bin/cluster-backup.sh ${BACKUP_DIR}

if [ $? -eq 0 ]; then
  echo "✅ Backup completed successfully"
  echo "Files created:"
  oc debug node/${MASTER_NODE} -- chroot /host ls -lh ${BACKUP_DIR}/
else
  echo "❌ Backup failed"
  exit 1
fi
EOF

chmod +x /tmp/etcd-backup.sh
```

### Backup Programado (CronJob)
```bash
# Criar namespace
oc create namespace etcd-backup

# Criar ServiceAccount com permissões
oc create sa etcd-backup -n etcd-backup
oc adm policy add-scc-to-user privileged -z etcd-backup -n etcd-backup
oc adm policy add-cluster-role-to-user cluster-admin -z etcd-backup -n etcd-backup

# Criar CronJob
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: etcd-backup
  namespace: etcd-backup
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: etcd-backup
          nodeSelector:
            node-role.kubernetes.io/master: ""
          restartPolicy: Never
          hostNetwork: true
          hostPID: true
          containers:
          - name: backup
            image: registry.redhat.io/openshift4/ose-cli:latest
            command:
            - /bin/bash
            - -c
            - |
              set -e
              BACKUP_DIR="/host/home/core/backup-\$(date +%Y%m%d-%H%M%S)"
              echo "Starting backup to \${BACKUP_DIR}"
              /host/usr/local/bin/cluster-backup.sh \${BACKUP_DIR}
              echo "Backup completed"
              ls -lh \${BACKUP_DIR}/
            securityContext:
              privileged: true
              runAsUser: 0
            volumeMounts:
            - name: host
              mountPath: /host
          volumes:
          - name: host
            hostPath:
              path: /
              type: Directory
          tolerations:
          - effect: NoSchedule
            operator: Exists
          - effect: NoExecute
            operator: Exists
EOF

# Verificar CronJob
oc get cronjob -n etcd-backup

# Testar manualmente
oc create job test-backup --from=cronjob/etcd-backup -n etcd-backup

# Ver logs
oc logs -n etcd-backup job/test-backup
```

### Backup de Recursos do Cluster
```bash
# Backup de recursos (não é etcd, são YAMLs)
mkdir -p cluster-resources-backup

# Namespaces
oc get namespaces -o yaml > cluster-resources-backup/namespaces.yaml

# Projects
oc get projects -o yaml > cluster-resources-backup/projects.yaml

# Cluster roles
oc get clusterroles -o yaml > cluster-resources-backup/clusterroles.yaml

# Cluster role bindings
oc get clusterrolebindings -o yaml > cluster-resources-backup/clusterrolebindings.yaml

# Storage classes
oc get sc -o yaml > cluster-resources-backup/storageclasses.yaml

# PVs
oc get pv -o yaml > cluster-resources-backup/pvs.yaml

# CRDs
oc get crd -o yaml > cluster-resources-backup/crds.yaml

# All resources de cada namespace (exemplo)
for ns in $(oc get ns -o jsonpath='{.items[*].metadata.name}'); do
  echo "Backing up namespace: $ns"
  mkdir -p cluster-resources-backup/$ns
  oc get all -n $ns -o yaml > cluster-resources-backup/$ns/all.yaml
done

# Comprimir
tar czf cluster-resources-backup-$(date +%Y%m%d).tar.gz cluster-resources-backup/
```

---

## 🔄 Restore

### Restore do Etcd
```bash
# ⚠️ ATENÇÃO: Restore é procedimento crítico!
# Sempre consulte documentação oficial antes de fazer restore

# 1. Conectar ao master node onde está o backup
oc debug node/<master-node-name>
chroot /host

# 2. Copiar backup para /home/core/backup/
ls -lh /home/core/backup/

# 3. Executar restore
/usr/local/bin/cluster-restore.sh /home/core/backup

# 4. Aguardar cluster reiniciar
# Nodes vão reiniciar automaticamente
# Isso pode levar 20-30 minutos

# 5. Verificar status
oc get nodes
oc get co
oc get clusterversion
```

### Verificar após Restore
```bash
# Nodes
oc get nodes

# Cluster Operators
oc get co

# Etcd pods
oc get pods -n openshift-etcd

# Etcd health
oc exec -n openshift-etcd <etcd-pod> -- etcdctl endpoint health --cluster

# Pods em geral
oc get pods -A
```

---

## 🔧 Etcd Defrag

### Verificar Tamanho do Etcd
```bash
# Ver tamanho do database
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl endpoint status --cluster -w table

# Ver alarmes (NOSPACE alarm indica problema)
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl alarm list
```

### Executar Defrag
```bash
# Defrag de um membro
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl defrag

# Defrag de todos os membros (sequencialmente)
for pod in $(oc get pods -n openshift-etcd -l app=etcd -o name); do
  echo "Defragmenting $pod"
  oc exec -n openshift-etcd ${pod#pod/} -- etcdctl defrag
  sleep 10
done

# Verificar tamanho após defrag
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl endpoint status --cluster -w table
```

### Limpar Alarmes
```bash
# Se houver alarm de NOSPACE
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl alarm disarm

# Verificar
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl alarm list
```

---

## 📖 Navegação

- [← Anterior: Cluster Version e Updates](21-cluster-version-updates.md)
- [→ Próximo: Comandos Customizados](23-comandos-customizados.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
