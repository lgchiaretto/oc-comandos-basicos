# Backup e Disaster Recovery

Este documento contém estratégias e comandos para backup e recuperação de desastres no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [Backup de Aplicações](#backup-de-aplicações)
3. [Backup de Dados](#backup-de-dados)
4. [Disaster Recovery](#disaster-recovery)
5. [Documentação Oficial](#documentação-oficial)
6. [Navegação](#navegação)
---

## Backup de Aplicações

### Velero - Backup Tool
**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
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

**Aguardar instalação**

```bash ignore-test
oc get csv -n openshift-adp
```

**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
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
**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
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

**Verificar snapshot**

```bash
oc get volumesnapshot
```

**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash
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
**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
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

**Aguardar condição específica do recurso**

```bash ignore-test
oc wait --for=condition=ready pod/backup-pod
```

**Executar comando dentro do pod especificado**

```bash ignore-test
oc exec backup-pod -- tar czf /tmp/backup.tar.gz /data
```

**Copiar arquivo entre máquina local e pod**

```bash ignore-test
oc cp backup-pod:/tmp/backup.tar.gz ./pvc-backup.tar.gz
```

**Deletar o recurso especificado**

```bash ignore-test
oc delete pod backup-pod
```

### Backup de Database
**MySQL/MariaDB**

```bash ignore-test
oc exec <mysql-pod> -- mysqldump -u root -p<password> --all-databases > mysql-backup.sql
```

**PostgreSQL**

```bash ignore-test
oc exec <postgres-pod> -- pg_dumpall -U postgres > postgres-backup.sql
```

**MongoDB**

```bash ignore-test
oc exec <mongodb-pod> -- mongodump --archive > mongodb-backup.archive
```

**Restore (exemplos)**

```bash ignore-test
oc exec -i <mysql-pod> -- mysql -u root -p<password> < mysql-backup.sql
oc exec -i <postgres-pod> -- psql -U postgres < postgres-backup.sql
oc exec -i <mongodb-pod> -- mongorestore --archive < mongodb-backup.archive
```

---

## Disaster Recovery

### Preparação para DR
**Checklist de preparação**

```bash ignore-test
cat > /tmp/dr-checklist.md << 'EOF'
# Disaster Recovery Checklist
```

**# Backups Configurados**

```bash ignore-test
- [ ] Etcd backup diário
- [ ] Application manifests backup
- [ ] PV snapshots ou backup
- [ ] Database backups
- [ ] Registry images backup
- [ ] Cluster configuration backup
```

**# Documentação**

```bash ignore-test
- [ ] Procedimentos de restore documentados
- [ ] Lista de contatos de emergência
- [ ] Diagrama de arquitetura atualizado
- [ ] Inventário de aplicações críticas
- [ ] RTO/RPO definidos por aplicação
```

**# Testes**

```bash ignore-test
- [ ] Teste de restore de etcd
- [ ] Teste de restore de aplicações
- [ ] Teste de restore de dados
- [ ] DR drill completo (anual)
```

**# Armazenamento**

```bash ignore-test
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
**1. Restore de namespace**

```bash ignore-test
tar xzf namespace-backup-myproject-*.tar.gz
cd namespace-backup-myproject-*/
```

**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
oc apply -f namespace.yaml
```

**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
oc apply -f secrets.yaml
oc apply -f configmaps.yaml
```

**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
oc apply -f /tmp/persistentvolumeclaims.yaml
```

**Listar todos os Persistent Volume Claims do namespace**

```bash ignore-test
oc get pvc
```

**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
oc apply -f /tmp/serviceaccounts.yaml
oc apply -f /tmp/roles.yaml
oc apply -f /tmp/rolebindings.yaml
```

**Aplicar configuração do arquivo YAML/JSON ao cluster**

```bash ignore-test
oc apply -f /tmp/deployments.yaml
oc apply -f /tmp/statefulsets.yaml
oc apply -f /tmp/services.yaml
oc apply -f /tmp/routes.yaml
```

**Listar todos os recursos principais do namespace**

```bash ignore-test
oc get all
```

---

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/backup_and_restore">Backup and restore</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration">Post-installation configuration</a>

---

## Navegação

- [← Anterior: Templates e Manifests](26-templates-manifests.md)
- [→ Próximo: Patch e Edit](28-patch-edit.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
