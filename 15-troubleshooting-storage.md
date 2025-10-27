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
```markdown
**Ação:** Listar todos os Persistent Volume Claims do namespace
```

```bash
oc get pvc
```

```markdown
**Ação:** Exibir persistent volume claim em formato JSON
```

```bash
oc get pvc -o jsonpath='{.items[?(@.status.phase=="Pending")].metadata.name}'
```

```markdown
**Ação:** Exibir detalhes completos do persistent volume claim
**Exemplo:** `oc describe pvc <resource-name>`
```

```bash
oc describe pvc test-app
```

```markdown
**Ação:** Listar eventos filtrados por campo específico
```

```bash
oc get events --field-selector involvedObject.name=test-app
```

```markdown
**Ação:** Exibir persistent volume claim "test-app" em formato JSON
**Exemplo:** `oc get pvc <resource-name>app -o jsonpath='{.spec.volumeName}'`
```

```bash
oc get pvc test-app -o jsonpath='{.spec.volumeName}'
```

```markdown
**Ação:** Exibir persistent volume claim "test-app" em formato JSON
**Exemplo:** `oc get pvc <resource-name>app -o jsonpath='{.spec.resources.requests.storage}'`
```

```bash
oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
```

### Diagnosticar PV
```markdown
**Ação:** Listar todos os Persistent Volumes do cluster
```

```bash
oc get pv
```

```markdown
**Ação:** Exibir persistent volume em formato JSON
```

```bash
oc get pv -o jsonpath='{.items[?(@.status.phase=="Available")].metadata.name}'
```

```markdown
**Ação:** Exibir persistent volume em formato JSON
```

```bash
oc get pv -o jsonpath='{.items[?(@.status.phase=="Failed")].metadata.name}'
```

```markdown
**Ação:** Descrever PV
```

```bash ignore-test
oc describe pv <nome-do-pv>
```

```markdown
**Ação:** Ver claim que está usando o PV
```

```bash ignore-test
oc get pv <nome-do-pv> -o jsonpath='{.spec.claimRef.name}'
```

```markdown
**Ação:** Ver access modes
```

```bash ignore-test
oc get pv <nome-do-pv> -o jsonpath='{.spec.accessModes}'
```

### Pending PVC
```markdown
**Ação:** Exibir detalhes completos do persistent volume claim
**Exemplo:** `oc describe pvc <resource-name> | grep -A 10 Events`
```

```bash
oc describe pvc test-app | grep -A 10 Events
```

```markdown
**Ação:** Exibir persistent volume em formato JSON
```

```bash
oc get pv -o jsonpath='{.items[?(@.status.phase=="Available")].metadata.name}'
```

```markdown
**Ação:** Verificar StorageClass
```

```bash
oc get sc
```

```markdown
**Ação:** Verificar se StorageClass existe
```

```bash ignore-test
oc get sc <storage-class-name>
```

```markdown
**Ação:** Ver provisioner
```

```bash ignore-test
oc get sc <storage-class-name> -o jsonpath='{.provisioner}'
```

---

## StorageClass

### Verificar StorageClasses
```markdown
**Ação:** Listar StorageClasses
```

```bash
oc get storageclass
oc get sc
```

```markdown
**Ação:** Descrever StorageClass
```

```bash ignore-test
oc describe sc <nome-da-sc>
```

```markdown
**Ação:** Exibir storageclass em formato JSON
```

```bash
oc get sc -o json | jq -r '.items[] | select(.metadata.annotations."storageclass.kubernetes.io/is-default-class"=="true") | .metadata.name'
```

```markdown
**Ação:** Listar storageclass com colunas customizadas
```

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

```markdown
**Ação:** Ver CSI drivers
```

```bash
oc get csidrivers
oc get csinodes
```

```markdown
**Ação:** Listar pods de todos os namespaces do cluster
```

```bash
oc get pods -A | grep csi
```

---

## Problemas Comuns

### Volume Não Monta
```markdown
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe pod <resource-name> | grep -A 10 Volumes`
```

```bash
oc describe pod my-pod | grep -A 10 Volumes
```

```markdown
**Ação:** Listar eventos filtrados por campo específico
```

```bash
oc get events --field-selector involvedObject.name=my-pod
```

```markdown
**Ação:** Listar todos os Persistent Volume Claims do namespace
```

```bash
oc get pvc
```

```markdown
**Ação:** Exibir recurso "my-pod" em formato JSON
**Exemplo:** `oc get pod <resource-name>pod -o jsonpath='{.spec.nodeName}'`
```

```bash
oc get pod my-pod -o jsonpath='{.spec.nodeName}'
```

```markdown
**Ação:** Debug no node
**Ação:** Verificar mounts
```

```bash ignore-test
oc debug node/<node-name>
chroot /host
mount | grep <pv-name>
df -h
```

### ReadOnly Filesystem
```markdown
**Ação:** Exibir persistent volume claim "test-app" em formato JSON
**Exemplo:** `oc get pvc <resource-name>app -o jsonpath='{.spec.accessModes}'`
```

```bash
oc get pvc test-app -o jsonpath='{.spec.accessModes}'
```

```markdown
**Ação:** Verificar access mode do PV
**Exemplo:** `oc get pv <pv-name> -o jsonpath='{.spec.accessModes}'`
```

```bash ignore-test
oc get pv <pv-name> -o jsonpath='{.spec.accessModes}'
```

```markdown
**Ação:** Exibir persistent volume claim "test-app" em formato JSON
**Exemplo:** `oc get pvc <resource-name>app -o jsonpath='{.spec.volumeName}'`
**Ação:** oc get pod <resource-name>pod -o jsonpath='{.spec.nodeName}'
```

```bash ignore-test
oc get pvc test-app -o jsonpath='{.spec.volumeName}'
oc get pod my-pod -o jsonpath='{.spec.nodeName}'
```

### Volume Full (Cheio)
```markdown
**Ação:** Executar comando dentro do pod especificado
```

```bash ignore-test
oc exec my-pod -- df -h
```

```markdown
**Ação:** Exibir persistent volume claim "test-app" em formato JSON
**Exemplo:** `oc get pvc <resource-name>app -o jsonpath='{.spec.resources.requests.storage}'`
```

```bash
oc get pvc test-app -o jsonpath='{.spec.resources.requests.storage}'
```

```markdown
**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch pvc <resource-name>app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'`
```

```bash
oc patch pvc test-app -p '{"spec":{"resources":{"requests":{"storage":"20Gi"}}}}'
```

```markdown
**Ação:** Verificar se expansão é permitida
```

```bash ignore-test
oc get sc <storage-class> -o jsonpath='{.allowVolumeExpansion}'
```

```markdown
**Ação:** Exibir detalhes completos do persistent volume claim
**Exemplo:** `oc describe pvc <resource-name>`
```

```bash
oc describe pvc test-app
```

### PVC Stuck Terminating
```markdown
**Ação:** Exibir pods em formato JSON
```

```bash ignore-test
oc get pods -o json | jq -r '.items[] | select(.spec.volumes[]?.persistentVolumeClaim.claimName=="test-app") | .metadata.name'
```

```markdown
**Ação:** Deletar recurso forçadamente (sem período de espera)
**Exemplo:** `oc delete pod <resource-name>pod --grace-period=0 --force`
```

```bash ignore-test
oc delete pod my-pod --grace-period=0 --force
```

```markdown
**Ação:** Aplicar modificação parcial ao recurso usando patch
**Exemplo:** `oc patch pvc <resource-name>app -p '{"metadata":{"finalizers":null}}'`
```

```bash
oc patch pvc test-app -p '{"metadata":{"finalizers":null}}'
```

```markdown
**Ação:** Exibir persistent volume claim "test-app" em formato JSON
**Exemplo:** `oc get pvc <resource-name>app -o jsonpath='{.metadata.finalizers}'`
```

```bash
oc get pvc test-app -o jsonpath='{.metadata.finalizers}'
```

---

## Operadores de Storage

### ODF (OpenShift Data Foundation)
```markdown
**Ação:** Verificar pods do ODF
```

```bash
oc get pods -n openshift-storage
```

```markdown
**Ação:** Status do ODF
```

```bash
oc get storagecluster -n openshift-storage
```

```markdown
**Ação:** Listar recurso filtrados por label
```

```bash
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph status --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

```markdown
**Ação:** Listar recurso filtrados por label
```

```bash
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph health detail --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

```markdown
**Ação:** Listar recurso filtrados por label
```

```bash
oc exec -it $(oc get pods -l app=rook-ceph-operator -o jsonpath='{.items[*].metadata.name}' -n openshift-storage) -n openshift-storage --   ceph osd status --cluster=openshift-storage --conf=/var/lib/rook/openshift-storage/openshift-storage.config --keyring=/var/lib/rook/openshift-storage/client.admin.keyring
```

```markdown
**Ação:** Coletar dados de diagnóstico completo do cluster
```

```bash ignore-test
oc adm must-gather --image=registry.redhat.io/odf4/ocs-must-gather-rhel8:latest
```

### Local Storage Operator
```markdown
**Ação:** Listar recurso de todos os namespaces do cluster
```

```bash
oc get localvolume -A
```

```markdown
**Ação:** Ver pods do local storage
```

```bash
oc get pods -n openshift-local-storage
```

```markdown
**Ação:** Exibir logs de todos os pods que correspondem ao label
**Exemplo:** `oc logs -n <namespace> -l name=local-storage-operator`
```

```bash
oc logs -n openshift-local-storage -l name=local-storage-operator
```

### CSI Drivers
```markdown
**Ação:** Listar CSI drivers instalados
```

```bash
oc get csidrivers
```

```markdown
**Ação:** Listar pods de todos os namespaces do cluster
```

```bash
oc get pods -A | grep csi
```

```markdown
**Ação:** Logs do CSI driver (exemplo)
```

```bash ignore-test
oc logs -n <namespace> <csi-driver-pod> -c csi-driver
```

```markdown
**Ação:** Ver CSI nodes
```

```bash
oc get csinodes
```

```markdown
**Ação:** Descrever CSI node
```

```bash ignore-test
oc describe csinode <node-name>
```

---

## Debug Avançado

### Verificar Backend de Storage
```markdown
**Ação:** Debug em node específico
```

```bash ignore-test
oc debug node/<node-name>
chroot /host
```

```markdown
**Ação:** Ver discos
```

```bash ignore-test
lsblk
fdisk -l
```

```markdown
**Ação:** Ver mounts
```

```bash ignore-test
mount | grep pvc
df -h
```

```markdown
**Ação:** Ver logs do kubelet relacionados a storage
```

```bash ignore-test
journalctl -u kubelet | grep -i volume
```

```markdown
**Ação:** Ver logs do CRI-O
```

```bash ignore-test
journalctl -u crio | grep -i volume
```

### Comandos Úteis em Nodes
```markdown
* Dentro do debug node:
```

```bash ignore-test
chroot /host
```

```markdown
**Ação:** Ver volumes do Kubernetes
```

```bash ignore-test
ls -la /var/lib/kubelet/pods/
```

```markdown
**Ação:** Ver PVs montados
```

```bash ignore-test
ls -la /var/lib/origin/openshift.local.volumes/
```

```markdown
**Ação:** Verificar permissões
```

```bash ignore-test
ls -laZ /var/lib/kubelet/pods/<pod-id>/volumes/
```

```markdown
**Ação:** Verificar SELinux contexts
```

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
