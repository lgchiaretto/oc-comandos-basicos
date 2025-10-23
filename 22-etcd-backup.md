# 💾 Etcd e Backup

Este documento contém comandos para gerenciar etcd e realizar backups do cluster OpenShift.

---

## 📋 Índice

1. [Etcd Status](#etcd-status)
2. [Backup do Cluster](#backup-do-cluster)
3. [Restore](#restore)

---

## 🔍 Etcd Status

### Verificar Etcd
```bash
# Pods do etcd
oc get pods -n openshift-etcd
```

```bash
# Ver etcd members
oc get pods -n openshift-etcd -l app=etcd -o wide
```

```bash
# Status do etcd operator
oc get clusteroperator etcd
```

```bash
# Descrever etcd operator
oc describe co etcd
```

```bash ignore-test
# Logs do etcd
oc logs -n openshift-etcd <etcd-pod-name>
```

```bash ignore-test
# Pegar o log do pod etcd-0
oc logs -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}')
```

```bash ignore-test
# Logs do etcd-operator
oc logs -n openshift-etcd-operator <etcd-operator-pod>
```

### Etcd Health Check
```bash ignore-test
# Executar dentro de pod etcd
oc rsh -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}')
```

```bash ignore-test
# Dentro do pod:
etcdctl endpoint health --cluster
etcdctl endpoint status --cluster -w table
etcdctl member list -w table
```

```bash ignore-test
# 'etcdctl endpoint status --cluster -w table' executado diretamente no pod
oc exec -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}') -- etcdctl endpoint status --cluster -w table
```

```bash ignore-test
# 'etcdctl member list -w table' executado diretamente no pod
oc exec -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[1].metadata.name}') -- etcdctl member list -w table
```

```bash ignore-test
# Verificar alarmes
oc exec -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}') -- etcdctl alarm list
```

---

## 💾 Backup do Cluster

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

> ℹ️ Para um backup automatizado do cluster, acesse:
>
> https://github.com/lgchiaretto/openshift4-backup-automation

---

## 🔄 Restore

### Restore do Etcd
```bash ignore-test
# ⚠️ ATENÇÃO: Restore é procedimento crítico!
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

```bash
# Verificar
oc exec -n openshift-etcd <etcd-pod-name> -- etcdctl alarm list

---

## 📖 Navegação

- [← Anterior: Cluster Version e Updates](21-cluster-version-updates.md)
- [→ Próximo: Comandos Customizados](23-comandos-customizados.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
