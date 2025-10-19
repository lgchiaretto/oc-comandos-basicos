# 🔒 Segurança e RBAC

Este documento contém comandos para gerenciar segurança, permissões e RBAC no OpenShift.

---

## 📋 Índice

1. [RBAC Básico](#rbac-básico)
2. [Roles e RoleBindings](#roles-e-rolebindings)
3. [Service Accounts](#service-accounts)
4. [Security Context Constraints (SCC)](#security-context-constraints-scc)
5. [Policies e Auditoria](#policies-e-auditoria)

---

## 👥 RBAC Básico

### Verificar Permissões
```bash
# Quem pode fazer determinada ação
oc adm policy who-can <verbo> <recurso>
oc adm policy who-can get pods
oc adm policy who-can delete projects

# Verificar minhas permissões
oc auth can-i <verbo> <recurso>
oc auth can-i create pods
oc auth can-i delete projects

# Como outro usuário
oc auth can-i get pods --as=<usuario>

# Listar minhas permissões
oc auth can-i --list
```

### Usuários e Grupos
```bash
# Listar usuários
oc get users

# Listar grupos
oc get groups

# Ver identidades
oc get identities

# Descrever usuário
oc describe user <username>

# Ver grupos de um usuário
oc describe user <username> | grep Groups
```

---

## 🎭 Roles e RoleBindings

### Cluster Roles
```bash
# Listar ClusterRoles
oc get clusterroles

# Roles importantes
oc get clusterrole admin -o yaml
oc get clusterrole edit -o yaml
oc get clusterrole view -o yaml

# Descrever ClusterRole
oc describe clusterrole <nome-da-role>

# Ver permissões de uma ClusterRole
oc describe clusterrole admin | grep -A 50 PolicyRule
```

### Roles (Namespace)
```bash
# Listar Roles no namespace
oc get roles

# Criar Role customizada
oc create role <nome> --verb=<verbos> --resource=<recursos>

# Exemplo
oc create role pod-reader --verb=get,list,watch --resource=pods

# Editar Role
oc edit role <nome>

# Deletar Role
oc delete role <nome>
```

### ClusterRoleBindings
```bash
# Listar ClusterRoleBindings
oc get clusterrolebindings

# Ver quem tem role cluster-admin
oc get clusterrolebinding -o json | jq -r '.items[] | select(.roleRef.name=="cluster-admin") | .metadata.name'

# Adicionar usuário como cluster-admin
oc adm policy add-cluster-role-to-user cluster-admin <username>

# Remover cluster-admin
oc adm policy remove-cluster-role-from-user cluster-admin <username>

# Adicionar grupo
oc adm policy add-cluster-role-to-group cluster-admin <groupname>
```

### RoleBindings (Namespace)
```bash
# Listar RoleBindings
oc get rolebindings

# Adicionar role a usuário no namespace
oc adm policy add-role-to-user <role> <username>
oc adm policy add-role-to-user admin <username>
oc adm policy add-role-to-user edit <username>
oc adm policy add-role-to-user view <username>

# Adicionar role a grupo
oc adm policy add-role-to-group <role> <groupname>

# Remover role
oc adm policy remove-role-from-user <role> <username>

# Ver RoleBinding específico
oc describe rolebinding <nome>
```

---

## 🤖 Service Accounts

### Gerenciar Service Accounts
```bash
# Listar Service Accounts
oc get serviceaccounts
oc get sa

# Criar Service Account
oc create serviceaccount <nome>

# Descrever Service Account
oc describe sa <nome>

# Ver token da SA
oc sa get-token <nome>

# Ver secrets da SA
oc get sa <nome> -o jsonpath='{.secrets[*].name}'

# Deletar Service Account
oc delete sa <nome>
```

### Usar Service Accounts
```bash
# Adicionar role a Service Account
oc adm policy add-role-to-user <role> system:serviceaccount:<namespace>:<sa-name>

# Exemplo: dar role edit
oc adm policy add-role-to-user edit system:serviceaccount:myproject:mysa

# ClusterRole para SA
oc adm policy add-cluster-role-to-user <role> system:serviceaccount:<namespace>:<sa-name>

# Usar SA em deployment
oc set serviceaccount deployment/<nome> <sa-name>

# Ver qual SA o pod está usando
oc get pod <nome> -o jsonpath='{.spec.serviceAccountName}'
```

---

## 🛡️ Security Context Constraints (SCC)

### Listar e Ver SCCs
```bash
# Listar SCCs
oc get scc

# SCCs principais
oc get scc restricted -o yaml
oc get scc privileged -o yaml
oc get scc anyuid -o yaml

# Descrever SCC
oc describe scc <nome>

# Ver qual SCC o pod está usando
oc get pod <nome> -o yaml | grep scc

# Ver usuários/SAs em uma SCC
oc describe scc <nome> | grep Users
```

### Adicionar Permissões SCC
```bash
# Adicionar SA a uma SCC
oc adm policy add-scc-to-user <scc-name> system:serviceaccount:<namespace>:<sa-name>

# Exemplos comuns
oc adm policy add-scc-to-user anyuid system:serviceaccount:myproject:mysa
oc adm policy add-scc-to-user privileged system:serviceaccount:myproject:mysa

# Adicionar grupo
oc adm policy add-scc-to-group <scc-name> <group-name>

# Remover de SCC
oc adm policy remove-scc-from-user <scc-name> system:serviceaccount:<namespace>:<sa-name>

# Ver quem pode usar SCC
oc describe scc <scc-name>
```

### Troubleshoot SCC
```bash
# Ver por que pod não está rodando devido a SCC
oc describe pod <nome> | grep -i scc

# Ver eventos relacionados a SCC
oc get events --field-selector involvedObject.name=<pod-name> | grep -i scc

# Verificar capabilities do container
oc get pod <nome> -o yaml | grep -A 10 securityContext
```

---

## 📜 Policies e Auditoria

### Audit Logs
```bash
# Ver audit logs (em node)
oc debug node/<node-name>
chroot /host
cat /var/log/oauth-apiserver/audit.log
cat /var/log/openshift-apiserver/audit.log
cat /var/log/kube-apiserver/audit.log

# Buscar ações de usuário específico
grep <username> /var/log/openshift-apiserver/audit.log
```

### OAuth e Autenticação
```bash
# Ver OAuth config
oc get oauth cluster -o yaml

# Ver identity providers
oc get oauth cluster -o jsonpath='{.spec.identityProviders}'

# Ver pods do OAuth
oc get pods -n openshift-authentication

# Logs do OAuth
oc logs -n openshift-authentication <oauth-pod>
```

### Secrets de TLS
```bash
# Listar secrets TLS
oc get secrets --field-selector type=kubernetes.io/tls

# Ver certificado
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout

# Verificar validade
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout

# Criar secret TLS
oc create secret tls <nome> --cert=<cert-file> --key=<key-file>
```

---

## 📖 Navegação

- [← Anterior: Troubleshooting de Storage](15-troubleshooting-storage.md)
- [→ Próximo: Cluster Operators](17-cluster-operators.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
