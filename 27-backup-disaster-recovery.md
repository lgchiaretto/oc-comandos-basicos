# Backup e Disaster Recovery

Este documento contém estratégias e comandos para backup e recuperação de desastres no OpenShift.

---

## Índice

1. [Backup de Aplicações](#backup de aplicações)
2. [Backup de Dados](#backup de dados)
3. [Disaster Recovery](#disaster recovery)
4. [Backups Configurados](#backups configurados)
5. [Testes](#testes)
6. [Armazenamento](#armazenamento)
---

## Backup de Aplicações

### Velero - Backup Tool
```bash ignore-test
# Instalar Velero Operator
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: redhat-oadp-operator
  namespace: openshift-adp
spec:
  channel: stable-1.4
  name: redhat-oadp-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
EOF
```

```bash ignore-test
# Aguardar instalação
oc get csv -n openshift-adp
```

```bash ignore-test
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
```
---

## Backup de Dados

### Backup de PVCs
```bash ignore-test
# Snapshot de PVC (se StorageClass suportar)
cat <<EOF | oc apply -f -
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: pvc-snapshot
spec:
  volumeSnapshotClassName: ocs-storagecluster-cephfsplugin-snapclass
  source:
    persistentVolumeClaimName: test-app
EOF
```

```bash
# Verificar snapshot
oc get volumesnapshot
```

```bash
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
```bash ignore-test
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
      claimName: test-app
EOF
```

```bash ignore-test
# Aguardar pod ficar ready
oc wait --for=condition=ready pod/backup-pod
```

```bash ignore-test
# Tar dos dados
oc exec backup-pod -- tar czf /tmp/backup.tar.gz /data
```

```bash ignore-test
# Copiar backup
oc cp backup-pod:/tmp/backup.tar.gz ./pvc-backup.tar.gz
```

```bash ignore-test
# Limpeza
# oc delete pod <resource-name>
oc delete pod backup-pod
```

### Backup de Database
```bash ignore-test
# MySQL/MariaDB
oc exec <mysql-pod> -- mysqldump -u root -p<password> --all-databases > mysql-backup.sql
```

```bash ignore-test
# PostgreSQL
oc exec <postgres-pod> -- pg_dumpall -U postgres > postgres-backup.sql
```

```bash ignore-test
# MongoDB
oc exec <mongodb-pod> -- mongodump --archive > mongodb-backup.archive
```

```bash ignore-test
# Restore (exemplos)
oc exec -i <mysql-pod> -- mysql -u root -p<password> < mysql-backup.sql
oc exec -i <postgres-pod> -- psql -U postgres < postgres-backup.sql
oc exec -i <mongodb-pod> -- mongorestore --archive < mongodb-backup.archive
```

---

## Disaster Recovery

### Preparação para DR
```bash ignore-test
# Checklist de preparação
cat > /tmp/dr-checklist.md << 'EOF'
# Disaster Recovery Checklist
```

```bash ignore-test
## Backups Configurados
- [ ] Etcd backup diário
- [ ] Application manifests backup
- [ ] PV snapshots ou backup
- [ ] Database backups
- [ ] Registry images backup
- [ ] Cluster configuration backup
```

```bash ignore-test
## Documentação
- [ ] Procedimentos de restore documentados
- [ ] Lista de contatos de emergência
- [ ] Diagrama de arquitetura atualizado
- [ ] Inventário de aplicações críticas
- [ ] RTO/RPO definidos por aplicação
```

```bash ignore-test
## Testes
- [ ] Teste de restore de etcd
- [ ] Teste de restore de aplicações
- [ ] Teste de restore de dados
- [ ] DR drill completo (anual)
```

```bash ignore-test
## Armazenamento
- [ ] Backups em localização offsite
- [ ] Backups encriptados
- [ ] Retenção de backups configurada
- [ ] Verificação de integridade automática
EOF
```

```bash ignore-test
cat /tmp/dr-checklist.md
```

### Restore de Aplicação
```bash ignore-test
# 1. Restore de namespace
tar xzf namespace-backup-myproject-*.tar.gz
cd namespace-backup-myproject-*/
```

```bash ignore-test
# 2. Criar namespace
oc apply -f namespace.yaml
```

```bash ignore-test
# 3. Restore de secrets e configmaps primeiro
oc apply -f secrets.yaml
oc apply -f configmaps.yaml
```

```bash ignore-test
# 4. Restore de PVCs
oc apply -f /tmp/persistentvolumeclaims.yaml
```

```bash ignore-test
# 5. Aguardar PVCs bound
oc get pvc
```

```bash ignore-test
# 6. Restore de service accounts e RBAC
oc apply -f /tmp/serviceaccounts.yaml
oc apply -f /tmp/roles.yaml
oc apply -f /tmp/rolebindings.yaml
```

```bash ignore-test
# 7. Restore de applications
oc apply -f /tmp/deployments.yaml
oc apply -f /tmp/statefulsets.yaml
oc apply -f /tmp/services.yaml
oc apply -f /tmp/routes.yaml
```

```bash ignore-test
# 8. Verificar
oc get all
```


---


---


## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/backup_and_restore" target="_blank">Backup and restore</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/post_installation_configuration" target="_blank">Post-installation configuration</a>

---

## Navegação

- [← Anterior: Templates e Manifests](26-templates-manifests.md)
- [→ Próximo: Patch e Edit](28-patch-edit.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
