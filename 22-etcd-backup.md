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
**Pods do etcd**

```bash
oc get pods -n openshift-etcd
```

**Listar pods com informações detalhadas**

```bash
oc get pods -n openshift-etcd -l app=etcd -o wide
```

**Status do etcd operator**

**Exemplo:** `oc get clusteroperator <resource-name>`

```bash
oc get clusteroperator etcd
```

**Exibir detalhes completos do cluster operator**

**Exemplo:** `oc describe co <resource-name>`

```bash
oc describe co etcd
```

**Logs do etcd**

```bash ignore-test
oc logs -n openshift-etcd <etcd-pod-name>
```

**Listar recurso filtrados por label**

```bash ignore-test
oc logs -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}')
```

**Logs do etcd-operator**

```bash ignore-test
oc logs -n openshift-etcd-operator <etcd-operator-pod>
```

### Etcd Health Check
**Listar recurso filtrados por label**

```bash ignore-test
oc rsh -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}')
```

* Dentro do pod:

```bash ignore-test
etcdctl endpoint health --cluster
etcdctl endpoint status --cluster -w table
etcdctl member list -w table
```

**Listar recurso filtrados por label**

```bash ignore-test
oc exec -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}') -- etcdctl endpoint status --cluster -w table
```

**Listar recurso filtrados por label**

```bash ignore-test
oc exec -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[1].metadata.name}') -- etcdctl member list -w table
```

**Listar recurso filtrados por label**

```bash ignore-test
oc exec -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}') -- etcdctl alarm list
```

---

## Backup do Cluster

### Backup Manual do Etcd
**Conectar a um master node**

```bash ignore-test
oc debug node/<master-node-name>
```

* No debug shell:

```bash ignore-test
chroot /host
```

**Executar backup**

```bash ignore-test
/usr/local/bin/cluster-backup.sh /home/core/backup
```

**Verificar backup criado**

```bash ignore-test
ls -lh /home/core/backup/
```

**Sair do debug**

```bash ignore-test
exit
exit
```

**Copiar backup do node**

```bash ignore-test
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
**Se houver alarm de NOSPACE**

```bash ignore-test
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl alarm disarm
```

**Verificar**

```bash ignore-test
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
