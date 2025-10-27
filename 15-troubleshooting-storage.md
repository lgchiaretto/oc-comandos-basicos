# Troubleshooting de Storage

Este documento contém comandos para diagnosticar problemas de storage no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [PV e PVC](#pv-e-pvc)
3. [StorageClass](#storageclass)
4. [Problemas Comuns](#problemas-comuns)
5. [Operadores de Storage](#operadores-de-storage)
6. [Debug Avançado](#debug-avançado)
7. [Documentação Oficial](#documentação-oficial)
8. [Navegação](#navegação)
---

## PV e PVC

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
**Listar todos os Persistent Volume Claims do namespace**

```bash
oc get pvc
```

**Exibir persistent volume claim em formato JSON**

```bash
oc get pvc -o jsonpath='{.items[?(@.status.phase=="Pending")].metadata.name}'
```

**Exibir detalhes completos do persistent volume claim**


```bash
oc describe pvc test-app
```

**Listar eventos filtrados por campo específico**

```bash
oc get events --field-selector involvedObject.name=test-app
```

**Exibir persistent volume claim "test-app" em formato JSON**


```bash
oc get pvc test-app -o jsonpath='{.spec.volumeName}'
```

**Exibir persistent volume claim "test-app" em formato JSON**


```bash
oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
```

### Diagnosticar PV
**Listar todos os Persistent Volumes do cluster**

```bash
oc get pv
```

**Exibir persistent volume em formato JSON**

```bash
oc get pv -o jsonpath='{.items[?(@.status.phase=="Available")].metadata.name}'
```

**Exibir persistent volume em formato JSON**

```bash
oc get pv -o jsonpath='{.items[?(@.status.phase=="Failed")].metadata.name}'
```

**Descrever PV**

```bash ignore-test
oc describe pv <nome-do-pv>
```

**Ver claim que está usando o PV**

```bash ignore-test
oc get pv <nome-do-pv> -o jsonpath='{.spec.claimRef.name}'
```

**Ver access modes**

```bash ignore-test
oc get pv <nome-do-pv> -o jsonpath='{.spec.accessModes}'
```

### Pending PVC
**Exibir detalhes completos do persistent volume claim**


```bash
oc describe pvc test-app | grep -A 10 Events
```

**Exibir persistent volume em formato JSON**

```bash
oc get pv -o jsonpath='{.items[?(@.status.phase=="Available")].metadata.name}'
```

**Verificar StorageClass**

```bash
oc get sc
```

**Verificar se StorageClass existe**

```bash ignore-test
oc get sc <storage-class-name>
```

**Ver provisioner**

```bash ignore-test
oc get sc <storage-class-name> -o jsonpath='{.provisioner}'
```

---

## StorageClass

### Verificar StorageClasses
**Listar StorageClasses**

```bash
oc get storageclass
oc get sc
```

**Descrever StorageClass**

```bash ignore-test
oc describe sc <nome-da-sc>
```

**Exibir storageclass em formato JSON**

```bash
oc get sc -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'
```

**Listar storageclass com colunas customizadas**

```bash
oc get sc -o custom-columns=NAME:.metadata.name,PROVISIONER:.provisioner
```
ignore-test
```bash 
# Verificar parâmetros
# oc get sc <resource-name> -o yaml
oc get sc <resource-name> -o yaml
```

### Problemas com StorageClass

**Ver CSI drivers**

```bash
oc get csidrivers
oc get csinodes
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep csi
```

---

## Problemas Comuns

### Volume Não Monta
**Exibir detalhes completos do recurso**


```bash
oc describe pod my-pod | grep -A 10 Volumes
```

**Listar eventos filtrados por campo específico**

```bash
oc get events --field-selector involvedObject.name=my-pod
```

**Listar todos os Persistent Volume Claims do namespace**

```bash
oc get pvc
```

**Exibir recurso "my-pod" em formato JSON**


```bash
oc get pod my-pod -o jsonpath='{.spec.nodeName}'
```

**Debug no node**
**Verificar mounts**

```bash ignore-test
oc debug node/<node-name>
chroot /host
mount | grep <pv-name>
df -h
```

### ReadOnly Filesystem
**Exibir persistent volume claim "test-app" em formato JSON**


```bash
oc get pvc test-app -o jsonpath='{.spec.accessModes}'
```

**Verificar access mode do PV**


```bash ignore-test
oc get pv <pv-name> -o jsonpath='{.spec.accessModes}'
```

**Exibir persistent volume claim "test-app" em formato JSON**

**oc get pod <resource-name>pod -o jsonpath='{.spec.nodeName}'**

```bash ignore-test
oc get pvc test-app -o jsonpath='{.spec.volumeName}'
oc get pod my-pod -o jsonpath='{.spec.nodeName}'
```

### Volume Full (Cheio)
**Executar comando dentro do pod especificado**

```bash ignore-test
oc exec my-pod -- df -h
```

**Exibir persistent volume claim "test-app" em formato JSON**


```bash
oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
```

**Aplicar modificação parcial ao recurso usando patch**


```bash
oc patch pvc test-app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'
```

**Verificar se expansão é permitida**

```bash ignore-test
oc get sc <storage-class> -o jsonpath='{.allowVolumeExpansion}'
```

**Exibir detalhes completos do persistent volume claim**


```bash
oc describe pvc test-app
```

### PVC Stuck Terminating
**Exibir pods em formato JSON**

```bash ignore-test
oc get pods -o json | jq -r '.items[] | select(.spec.volumes[]?.persistentVolumeClaim.claimName=="test-app") | .metadata.name'
```

**Deletar recurso forçadamente (sem período de espera)**


```bash ignore-test
oc delete pod my-pod --grace-period=0 --force
```

**Aplicar modificação parcial ao recurso usando patch**


```bash
oc patch pvc test-app -p '{"metadata":{"finalizers":null}}'
```

**Exibir persistent volume claim "test-app" em formato JSON**


```bash
oc get pvc test-app -o jsonpath='{.metadata.finalizers}'
```

---

## Operadores de Storage

### ODF (OpenShift Data Foundation)
**Verificar pods do ODF**

```bash
oc get pods -n openshift-storage
```

**Status do ODF**

```bash
oc get storagecluster -n openshift-storage
```

**Listar recurso filtrados por label**

```bash
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph status --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

**Listar recurso filtrados por label**

```bash
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph health detail --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

**Listar recurso filtrados por label**

```bash
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph osd status --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

**Coletar dados de diagnóstico completo do cluster**

```bash ignore-test
oc adm must-gather --image=registry.redhat.io/odf4/ocs-must-gather-rhel8:latest
```

### Local Storage Operator
**Listar recurso de todos os namespaces do cluster**

```bash
oc get localvolume -A
```

**Ver pods do local storage**

```bash
oc get pods -n openshift-local-storage
```

**Exibir logs de todos os pods que correspondem ao label**


```bash
oc logs -n openshift-local-storage -l name=local-storage-operator
```

### CSI Drivers
**Listar CSI drivers instalados**

```bash
oc get csidrivers
```

**Listar pods de todos os namespaces do cluster**

```bash
oc get pods -A | grep csi
```

**Logs do CSI driver (exemplo)**

```bash ignore-test
oc logs -n <namespace> <csi-driver-pod> -c csi-driver
```

**Ver CSI nodes**

```bash
oc get csinodes
```

**Descrever CSI node**

```bash ignore-test
oc describe csinode <node-name>
```

---

## Debug Avançado

### Verificar Backend de Storage
**Debug em node específico**

```bash ignore-test
oc debug node/<node-name>
chroot /host
```

**Ver discos**

```bash ignore-test
lsblk
fdisk -l
```

**Ver mounts**

```bash ignore-test
mount | grep pvc
df -h
```

**Ver logs do kubelet relacionados a storage**

```bash ignore-test
journalctl -u kubelet | grep -i volume
```

**Ver logs do CRI-O**

```bash ignore-test
journalctl -u crio | grep -i volume
```

### Comandos Úteis em Nodes
* Dentro do debug node:

```bash ignore-test
chroot /host
```

**Ver volumes do Kubernetes**

```bash ignore-test
ls -la /var/lib/kubelet/pods/
```

**Ver PVs montados**

```bash ignore-test
ls -la /var/lib/origin/openshift.local.volumes/
```

**Verificar permissões**

```bash ignore-test
ls -laZ /var/lib/kubelet/pods/<pod-id>/volumes/
```

**Verificar SELinux contexts**

```bash ignore-test
ls -laZ /path/to/mount
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/storage">Storage - Troubleshooting persistent storage</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/support">Support - Troubleshooting</a>
---

---

## Navegação

- [← Anterior: Troubleshooting de Rede](14-troubleshooting-rede.md)
- [→ Próximo: Segurança e RBAC](16-seguranca-rbac.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
