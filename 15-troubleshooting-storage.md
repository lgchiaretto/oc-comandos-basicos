# 💾 Troubleshooting de Storage

Este documento contém comandos para diagnosticar problemas de storage no OpenShift.

---

## 📋 Índice

1. [📦 PV e PVC](#pv-e-pvc)
2. [🏪 StorageClass](#storageclass)
3. [🚨 Problemas Comuns](#problemas-comuns)
4. [🔧 Operadores de Storage](#operadores-de-storage)
5. [🛠 ️ Debug Avançado](#debug-avancado)
---

## 📦 PV e PVC

### Criar PVC

```bash
oc create -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-app
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  # Nenhuma linha storageClassName é informada.
  # O OpenShift usará a StorageClass marcada como "(default)".
EOF
```

### Diagnosticar PVC
```bash
# Listar PVCs e status
oc get pvc
```

```bash
# PVCs Pending
oc get pvc -o jsonpath='{.items[?(@.status.phase=="Pending")].metadata.name}'
```

```bash
# Descrever PVC
# oc describe pvc test-app
# oc describe pvc <resource-name>
oc describe pvc test-app
```

```bash
# Ver eventos relacionados
oc get events --field-selector involvedObject.name=test-app
```

```bash
# Ver qual PV está bound
# oc get pvc test-app -o jsonpath='{.spec.volumeName}'
# oc get pvc <resource-name>app -o jsonpath='{.spec.volumeName}'
oc get pvc test-app -o jsonpath='{.spec.volumeName}'
```

```bash
# Verificar capacidade solicitada vs disponível
# oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
# oc get pvc <resource-name>app -o jsonpath='{.spec.resources.requests.storage}'
oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
```

### Diagnosticar PV
```bash
# Listar PVs
oc get pv
```

```bash
# PVs disponíveis
oc get pv -o jsonpath='{.items[?(@.status.phase=="Available")].metadata.name}'
```

```bash
# PVs com problema
oc get pv -o jsonpath='{.items[?(@.status.phase=="Failed")].metadata.name}'
```

```bash ignore-test
# Descrever PV
oc describe pv <nome-do-pv>
```

```bash ignore-test
# Ver claim que está usando o PV
oc get pv <nome-do-pv> -o jsonpath='{.spec.claimRef.name}'
```

```bash ignore-test
# Ver access modes
oc get pv <nome-do-pv> -o jsonpath='{.spec.accessModes}'
```

### Pending PVC
```bash
# Ver por que PVC está Pending
# oc describe pvc test-app | grep -A 10 Events
# oc describe pvc <resource-name> | grep -A 10 Events
oc describe pvc test-app | grep -A 10 Events
```

```bash
# Verificar se há PV disponível
oc get pv -o jsonpath='{.items[?(@.status.phase=="Available")].metadata.name}'
```

```bash
# Verificar StorageClass
oc get sc
```

```bash ignore-test
# Verificar se StorageClass existe
oc get sc <storage-class-name>
```

```bash ignore-test
# Ver provisioner
oc get sc <storage-class-name> -o jsonpath='{.provisioner}'
```

---

## 🏪 StorageClass

### Verificar StorageClasses
```bash
# Listar StorageClasses
oc get storageclass
oc get sc
```

```bash ignore-test
# Descrever StorageClass
oc describe sc <nome-da-sc>
```

```bash
# Ver qual é a storageclass default
oc get sc -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'
```

```bash
# Ver provisioner
oc get sc -o custom-columns=NAME:.metadata.name,PROVISIONER:.provisioner
```
ignore-test
```bash 
# Verificar parâmetros
# oc get sc <resource-name> -o yaml
oc get sc <resource-name> -o yaml
```

### Problemas com StorageClass

```bash
# Ver CSI drivers
oc get csidrivers
oc get csinodes
```

```bash
# Ver CSI pods
oc get pods -A | grep csi
```

---

## 🚨 Problemas Comuns

### Volume Não Monta
```bash
# Verificar pod que usa o volume
# oc describe pod <resource-name> | grep -A 10 Volumes
oc describe pod my-pod | grep -A 10 Volumes
```

```bash
# Ver eventos de mount
oc get events --field-selector involvedObject.name=mypod | grep -i mount
```

```bash
# Verificar se PVC está Bound
oc get pvc
```

```bash
# Ver node do pod
# oc get pod <resource-name>pod -o jsonpath='{.spec.nodeName}'
oc get pod my-pod -o jsonpath='{.spec.nodeName}'
```

```bash ignore-test
# Debug no node
oc debug node/<node-name>
chroot /host
# Verificar mounts
mount | grep <pv-name>
df -h
```

### ReadOnly Filesystem
```bash
# Verificar access mode do PVC
# oc get pvc test-app -o jsonpath='{.spec.accessModes}'
# oc get pvc <resource-name>app -o jsonpath='{.spec.accessModes}'
oc get pvc test-app -o jsonpath='{.spec.accessModes}'
```

```bash ignore-test
# Verificar access mode do PV
# oc get pv <pv-name> -o jsonpath='{.spec.accessModes}'
oc get pv <pv-name> -o jsonpath='{.spec.accessModes}'
```

```bash ignore-test
# Se PV for RWO e pod está em outro node
# oc get pvc test-app -o jsonpath='{.spec.volumeName}'
# oc get pvc <resource-name>app -o jsonpath='{.spec.volumeName}'
oc get pvc test-app -o jsonpath='{.spec.volumeName}'
# oc get pod <resource-name>pod -o jsonpath='{.spec.nodeName}'
oc get pod my-pod -o jsonpath='{.spec.nodeName}'
```

### Volume Full (Cheio)
```bash ignore-test
# Verificar uso dentro do pod
oc exec my-pod -- df -h
```

```bash
# Verificar tamanho do PVC
# oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
# oc get pvc <resource-name>app -o jsonpath='{.spec.resources.requests.storage}'
oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
```

```bash
# Expandir PVC (se StorageClass permitir)
# oc patch pvc test-app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'
# oc patch pvc <resource-name>app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'
oc patch pvc test-app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'
```

```bash ignore-test
# Verificar se expansão é permitida
oc get sc <storage-class> -o jsonpath='{.allowVolumeExpansion}'
```

```bash
# Ver progresso da expansão
# oc describe pvc test-app
# oc describe pvc <resource-name>
oc describe pvc test-app
```

### PVC Stuck Terminating
```bash ignore-test
# Verificar se há pods usando
oc get pods -o json | jq -r '.items[] | select(.spec.volumes[]?.persistentVolumeClaim.claimName=="test-app") | .metadata.name'
```

```bash ignore-test
# Deletar pods que estão usando
# oc delete pod <resource-name>pod --grace-period=0 --force
oc delete pod my-pod --grace-period=0 --force
```

```bash
# Remover finalizers se necessário (CUIDADO!)
# oc patch pvc test-app -p '{"metadata":{"finalizers":null}}'
# oc patch pvc <resource-name>app -p '{"metadata":{"finalizers":null}}'
oc patch pvc test-app -p '{"metadata":{"finalizers":null}}'
```

```bash
# Ver finalizers
# oc get pvc test-app -o jsonpath='{.metadata.finalizers}'
# oc get pvc <resource-name>app -o jsonpath='{.metadata.finalizers}'
oc get pvc test-app -o jsonpath='{.metadata.finalizers}'
```

---

## 🔧 Operadores de Storage

### ODF (OpenShift Data Foundation)
```bash
# Verificar pods do ODF
oc get pods -n openshift-storage
```

```bash
# Status do ODF
oc get storagecluster -n openshift-storage
```

```bash
# Ver Ceph status
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph status --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

```bash
# Ceph health
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph health detail --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

```bash
# Ver OSDs
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph osd status --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

```bash ignore-test
# Must-gather do ODF
oc adm must-gather --image=registry.redhat.io/odf4/ocs-must-gather-rhel8:latest
```

### Local Storage Operator
```bash
# Ver local volumes
oc get localvolume -A
```

```bash
# Ver pods do local storage
oc get pods -n openshift-local-storage
```

```bash
# Logs do local storage operator
# oc logs -n <namespace> -l name=local-storage-operator
oc logs -n openshift-local-storage -l name=local-storage-operator
```

### CSI Drivers
```bash
# Listar CSI drivers instalados
oc get csidrivers
```

```bash
# Ver pods CSI
oc get pods -A | grep csi
```

```bash ignore-test
# Logs do CSI driver (exemplo)
oc logs -n <namespace> <csi-driver-pod> -c csi-driver
```

```bash
# Ver CSI nodes
oc get csinodes
```

```bash ignore-test
# Descrever CSI node
oc describe csinode <node-name>
```

---

## 🛠️ Debug Avançado

### Verificar Backend de Storage
```bash ignore-test
# Debug em node específico
oc debug node/<node-name>
chroot /host
```

```bash ignore-test
# Ver discos
lsblk
fdisk -l
```

```bash ignore-test
# Ver mounts
mount | grep pvc
df -h
```

```bash ignore-test
# Ver logs do kubelet relacionados a storage
journalctl -u kubelet | grep -i volume
```

```bash ignore-test
# Ver logs do CRI-O
journalctl -u crio | grep -i volume
```

### Comandos Úteis em Nodes
```bash ignore-test
# Dentro do debug node:
chroot /host
```

```bash ignore-test
# Ver volumes do Kubernetes
ls -la /var/lib/kubelet/pods/
```

```bash ignore-test
# Ver PVs montados
ls -la /var/lib/origin/openshift.local.volumes/
```

```bash ignore-test
# Verificar permissões
ls -laZ /var/lib/kubelet/pods/<pod-id>/volumes/
```

```bash ignore-test
# Verificar SELinux contexts
ls -laZ /path/to/mount
```

---

## 📚 Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- [Troubleshooting storage issues](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage/troubleshooting-storage-issues)

---

## 📖 Navegação

- [← Anterior: Troubleshooting de Rede](14-troubleshooting-rede.md)
- [→ Próximo: Segurança e RBAC](16-seguranca-rbac.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
