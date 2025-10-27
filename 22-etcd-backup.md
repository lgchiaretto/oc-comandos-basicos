# Etcd e Backup

Este documento contém comandos para gerenciar etcd e realizar backups do cluster OpenShift.

---

## Índice

- [Etcd e Backup](#etcd-e-backup)
  - [Índice](#índice)
  - [Etcd Status](#etcd-status)
    - [Verificar Etcd](#verificar-etcd)
    - [Etcd Health Check](#etcd-health-check)
  - [Backup do Cluster](#backup-do-cluster)
    - [Backup Manual do Etcd](#backup-manual-do-etcd)
    - [Script Automatizado de Backup](#script-automatizado-de-backup)
  - [Restore](#restore)
    - [Restore do Etcd](#restore-do-etcd)
    - [Limpar Alarmes](#limpar-alarmes)
  - [Documentação Oficial](#documentação-oficial)
  - [Navegação](#navegação)
---

## Etcd Status

### Verificar Etcd
```bash
# Pods do etcd
oc get pods -n openshift-etcd
```

```bash
# Listar pods com informações detalhadas
oc get pods -n openshift-etcd -l app=etcd -o wide
```

```bash
# Status do etcd operator
# oc get clusteroperator <resource-name>
oc get clusteroperator etcd
```

```bash
# Exibir detalhes completos do cluster operator
# oc describe co <resource-name>
oc describe co etcd
```

```bash ignore-test
# Logs do etcd
oc logs -n openshift-etcd <etcd-pod-name>
```

```bash ignore-test
# Listar recurso filtrados por label
oc logs -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}')
```

```bash ignore-test
# Logs do etcd-operator
oc logs -n openshift-etcd-operator <etcd-operator-pod>
```

### Etcd Health Check
```bash ignore-test
# Listar recurso filtrados por label
oc rsh -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}')
```

```bash ignore-test
# Dentro do pod:
etcdctl endpoint health --cluster
etcdctl endpoint status --cluster -w table
etcdctl member list -w table
```

```bash ignore-test
# Listar recurso filtrados por label
oc exec -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}') -- etcdctl endpoint status --cluster -w table
```

```bash ignore-test
# Listar recurso filtrados por label
oc exec -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[1].metadata.name}') -- etcdctl member list -w table
```

```bash ignore-test
# Listar recurso filtrados por label
oc exec -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}') -- etcdctl alarm list
```

---

## Backup do Cluster

### Backup Manual do Etcd
```bash ignore-test
# Conectar a um master node
oc debug node/<master-node-name>
```

```bash ignore-test
# No debug shell:
chroot /host
```

```bash ignore-test
# Executar backup
/usr/local/bin/cluster-backup.sh /home/core/backup
```

```bash ignore-test
# Verificar backup criado
ls -lh /home/core/backup/
```

```bash ignore-test
# Sair do debug
exit
exit
```

```bash ignore-test
# Copiar backup do node
oc rsync <master-node-name>:/home/core/backup/ ./cluster-backup/
```

### Script Automatizado de Backup

> ℹ Para um backup automatizado do cluster, acesse:
>
> https://github.com/lgchiaretto/openshift4-backup-automation

---

## Restore

### Restore do Etcd
```bash ignore-test
# ATENÇÃO: Restore é procedimento crítico!
# Sempre consulte documentação oficial antes de fazer restore
# Para rodar o restore você obrigatoriamente precisa ter acesso a um dos 
# masters seja por SSH ou 'oc debug'
# Para restaurar um backup do etcd siga o processo descrito na documentação oficial
```

### Limpar Alarmes
```bash ignore-test
# Se houver alarm de NOSPACE
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl alarm disarm
```

```bash ignore-test
# Verificar
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl alarm list
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/backup_and_restore">Backup and restore - Backing up etcd</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/postinstallation_configuration">Post-installation configuration</a>
---

---

## Navegação

- [← Anterior: Cluster Version e Updates](21-cluster-version-updates.md)
- [→ Próximo: Comandos Customizados](23-comandos-customizados.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
