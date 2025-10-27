# Segurança e RBAC

Este documento contém comandos para gerenciar segurança, permissões e RBAC no OpenShift.

---

## Índice

1. [Índice](#índice)
2. [RBAC Básico](#rbac-básico)
3. [Roles e RoleBindings](#roles-e-rolebindings)
4. [Service Accounts](#service-accounts)
5. [Security Context Constraints (SCC)](#security-context-constraints-(scc))
6. [Policies e Auditoria](#policies-e-auditoria)
7. [Documentação Oficial](#documentação-oficial)
8. [Navegação](#navegação)
---

## RBAC Básico

### Verificar Permissões
**Ação:** Quem pode fazer determinada ação
**Ação:** oc adm policy <resource-name> get pods
**Ação:** oc adm policy <resource-name> delete projects
```

```bash ignore-test
oc adm policy who-can <verbo> <recurso>

oc adm policy who-can get pods

oc adm policy who-can delete projects
```

**Ação:** Verificar minhas permissões
```

```bash ignore-test
oc auth can-i <verbo> <recurso>
oc auth can-i create pods
oc auth can-i delete projects
```

**Ação:** Como outro usuário
```

```bash ignore-test
oc auth can-i get pods --as=<usuario>
```

**Ação:** Verificar se usuário tem permissão para executar ação específica
```

```bash
oc auth can-i --list
```

### Usuários e Grupos
**Ação:** Listar usuários
```

```bash
oc get users
```

**Ação:** Listar grupos
```

```bash
oc get groups
```

**Ação:** Ver identidades
```

```bash
oc get identities
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe user <username>`
```

```bash
oc describe user chiaretto
```

---

## Roles e RoleBindings

### Cluster Roles
**Ação:** Listar ClusterRoles
```

```bash
oc get clusterroles
```

**Ação:** Exibir cluster role "admin" em formato YAML
**Exemplo:** `oc get clusterrole <role-name> -o yaml`
**Ação:** oc get clusterrole <role-name> -o yaml
**Ação:** oc get clusterrole <role-name> -o yaml
```

```bash
oc get clusterrole admin -o yaml
oc get clusterrole edit -o yaml
oc get clusterrole view -o yaml
```

**Ação:** Descrever ClusterRole
```

```bash ignore-test
oc describe clusterrole <nome-da-role>
```

**Ação:** Exibir detalhes completos do cluster role
**Exemplo:** `oc describe clusterrole <role-name> | grep -A 50 PolicyRule`
```

```bash
oc describe clusterrole admin | grep -A 50 PolicyRule
```

### Roles (Namespace)
**Ação:** Listar roles customizados do namespace
```

```bash
oc get roles
```

**Ação:** Criar Role customizada
```

```bash ignore-test
oc create role test-app --verb=<verbos> --resource=<recursos>
```

**Ação:** Exemplo
**Exemplo:** `oc create role <role-name> --verb=get,list,watch --resource=pods`
```

```bash
oc create role pod-reader --verb=get,list,watch --resource=pods
```

**Ação:** Abrir editor para modificar recurso interativamente
**Exemplo:** `oc edit role <role-name>`
```

```bash ignore-test
oc edit role pod-reader
```

**Ação:** Deletar o role especificado
**Exemplo:** `oc delete role <role-name>`
```

```bash
oc delete role pod-reader
```

### ClusterRoleBindings
**Ação:** Listar ClusterRoleBindings
```

```bash
oc get clusterrolebindings
```

**Ação:** Exibir recurso em formato JSON
```

```bash ignore-test
oc get clusterrolebinding -o json | jq -r '.items[] | select(.roleRef.name=="cluster-admin") | .metadata.name'
```

**Ação:** Adicionar usuário como cluster-admin
```

```bash ignore-test
oc adm policy add-cluster-role-to-user cluster-admin <username>
```

**Ação:** Remover cluster-admin
```

```bash ignore-test
oc adm policy remove-cluster-role-from-user cluster-admin <username>
```

**Ação:** Adicionar grupo
```

```bash ignore-test
oc adm policy add-cluster-role-to-group cluster-admin <groupname>
```

### RoleBindings (Namespace)
**Ação:** Listar vinculações de roles no namespace atual
```

```bash
oc get rolebindings
```

**Ação:** Adicionar role a usuário no namespace
```

```bash ignore-test
oc adm policy add-role-to-user <role> <username>
oc adm policy add-role-to-user admin <username>
oc adm policy add-role-to-user edit <username>
oc adm policy add-role-to-user view <username>
```

**Ação:** Adicionar role a grupo
```

```bash ignore-test
oc adm policy add-role-to-group <role> <groupname>
```

**Ação:** Remover role
```

```bash ignore-test
oc adm policy remove-role-from-user <role> <username>
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe rolebinding <rolebinding-name>`
```

```bash
oc describe rolebinding admin
```

---

## Service Accounts

### Gerenciar Service Accounts
**Ação:** Listar Service Accounts
```

```bash
oc get serviceaccounts
oc get sa
```

**Ação:** Criar novo recurso
**Exemplo:** `oc create serviceaccount <serviceaccount-name>`
```

```bash
oc create serviceaccount test-app
```

**Ação:** Exibir detalhes completos do serviceaccount
**Exemplo:** `oc describe sa <serviceaccount-name>`
```

```bash
oc describe sa test-app
```

**Ação:** Exibir serviceaccount "test-app" em formato JSON
**Exemplo:** `oc get sa <serviceaccount-name> -o jsonpath='{.secrets[*].name}'`
```

```bash ignore-test
oc get sa test-app -o jsonpath='{.secrets[*].name}'
```

**Ação:** Deletar o serviceaccount especificado
**Exemplo:** `oc delete sa <serviceaccount-name>`
```

```bash ignore-test
oc delete sa test-app
```

### Usar Service Accounts
**Ação:** Adicionar role a Service Account
```

```bash ignore-test
oc adm policy add-role-to-user <role> system:serviceaccount:development:test-app
```

**Ação:** Exemplo: dar role edit
**Exemplo:** `oc adm policy <resource-name> <username> system:serviceaccount:development:test-app`
```

```bash
oc adm policy add-role-to-user edit system:serviceaccount:development:test-app
```

**Ação:** ClusterRole para SA
```

```bash ignore-test
oc adm policy add-cluster-role-to-user <role> system:serviceaccount:development:test-app
```

**Ação:** Usar SA em deployment
**Exemplo:** `oc set serviceaccount <serviceaccount-name>/test-app test-app`
```

```bash ignore-test
oc set serviceaccount deployment/test-app test-app
```

**Ação:** Exibir recurso "test-app" em formato JSON
**Exemplo:** `oc get pod <resource-name>app -o jsonpath='{.spec.serviceAccountName}'`
```

```bash ignore-test
oc get pod test-app -o jsonpath='{.spec.serviceAccountName}'
```

---

## Security Context Constraints (SCC)

### Listar e Ver SCCs
**Ação:** Listar SCCs
```

```bash
oc get scc
```

**Ação:** Exibir recurso "restricted" em formato YAML
```

```bash
oc get scc restricted -o yaml
oc get scc privileged -o yaml
oc get scc anyuid -o yaml
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe scc <resource-name>`
```

```bash
oc describe scc restricted
```

```bash --ignore-test
# Ver qual SCC o pod está usando
# oc get pod <resource-name>app -o yaml | grep scc
oc get pod test-app -o yaml | grep scc
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe scc <resource-name> | grep Users`
```

```bash
oc describe scc restricted | grep Users
```

### Adicionar Permissões SCC
**Ação:** Exemplos comuns e use com moderação
**Exemplo:** `oc adm policy <resource-name> <username> system:serviceaccount:<namespace>:<sa-name>`
**Exemplo:** `oc adm policy <resource-name> <username> system:serviceaccount:<namespace>:<sa-name>`
```

```bash
oc adm policy add-scc-to-user anyuid system:serviceaccount:development:test-app
oc adm policy add-scc-to-user privileged system:serviceaccount:development:test-app
```

**Ação:** Adicionar grupo
**Exemplo:** `oc adm policy <resource-name> <group-name> "cn=ocpusers,cn=users,dc=chiaretto,dc=home"`
```

```bash
oc adm policy add-scc-to-group restricted "cn=ocpusers,cn=users,dc=chiaretto,dc=home"
```

**Ação:** Remover SCC de grupo
**Exemplo:** `oc adm policy <resource-name> <group-name> "cn=ocpusers,cn=users,dc=chiaretto,dc=home"`
```

```bash
oc adm policy remove-scc-from-group restricted "cn=ocpusers,cn=users,dc=chiaretto,dc=home"
```

**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe scc <resource-name>`
```

```bash
oc describe scc restricted
```

### Troubleshoot SCC
**Ação:** Exibir detalhes completos do recurso
**Exemplo:** `oc describe pod <resource-name> | grep -i scc`
```

```bash
oc describe pod test-app | grep -i scc
```

**Ação:** Ver eventos relacionados a SCC
```

```bash ignore-test
oc get events --field-selector involvedObject.name=<pod-name> | grep -i scc
```

**Ação:** Listar recurso de todos os namespaces do cluster
**Exemplo:** `oc get pod <resource-name>app -o yaml | grep -A 10 securityContext`
```

```bash ignore-test
oc get pod test-app -o yaml | grep -A 10 securityContext
```

---

## Policies e Auditoria

### Audit Logs
**Ação:** Ver audit logs (em node)
```

```bash ignore-test
oc debug node/<node-name>
chroot /host
cat /var/log/oauth-apiserver/audit.log
cat /var/log/openshift-apiserver/audit.log
cat /var/log/kube-apiserver/audit.log
```

**Ação:** Buscar ações de usuário específico
```

```bash ignore-test
grep <username> /var/log/openshift-apiserver/audit.log
```

### OAuth e Autenticação
**Ação:** Exibir recurso "cluster" em formato YAML
```

```bash
oc get oauth cluster -o yaml
```

**Ação:** Exibir recurso "cluster" em formato JSON
```

```bash
oc get oauth cluster -o jsonpath='{.spec.identityProviders}'
```

**Ação:** Ver pods do OAuth
```

```bash
oc get pods -n openshift-authentication
```

**Ação:** Logs do OAuth
```

```bash ignore-test
oc logs -n openshift-authentication <oauth-pod>
```

### Secrets de TLS
**Ação:** Listar recurso filtrados por campo específico
```

```bash
oc get secrets --field-selector type=kubernetes.io/tls
```

**Ação:** Ver certificado
```

```bash ignore-test
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

**Ação:** Verificar validade
```

```bash ignore-test
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

**Ação:** Criar secret TLS
```

```bash ignore-test
oc create secret tls test-app --cert=<cert-file> --key=<key-file>
```

## Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization">Authentication and authorization</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/security_and_compliance">Security and compliance - Security Context Constraints</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization/using-rbac">RBAC - Using RBAC to define and apply permissions</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/authentication_and_authorization/understanding-and-creating-service-accounts">Service Accounts</a>
---

---

## Navegação

- [← Anterior: Troubleshooting de Storage](15-troubleshooting-storage.md)
- [→ Próximo: Cluster Operators](17-cluster-operators.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
