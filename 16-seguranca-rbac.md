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
**Quem pode fazer determinada ação**
**oc adm policy <resource-name> get pods**
**oc adm policy <resource-name> delete projects**

```bash ignore-test
oc adm policy who-can <verbo> <recurso>

oc adm policy who-can get pods

oc adm policy who-can delete projects
```

**Verificar minhas permissões**

```bash ignore-test
oc auth can-i <verbo> <recurso>
oc auth can-i create pods
oc auth can-i delete projects
```

**Como outro usuário**

```bash ignore-test
oc auth can-i get pods --as=<usuario>
```

**Verificar se usuário tem permissão para executar ação específica**

```bash
oc auth can-i --list
```

### Usuários e Grupos
**Listar usuários**

```bash
oc get users
```

**Listar grupos**

```bash
oc get groups
```

**Ver identidades**

```bash
oc get identities
```

**Exibir detalhes completos do recurso**
**Exemplo:** `oc describe user <username>`

```bash
oc describe user chiaretto
```

---

## Roles e RoleBindings

### Cluster Roles
**Listar ClusterRoles**

```bash
oc get clusterroles
```

**Exibir cluster role "admin" em formato YAML**
**Exemplo:** `oc get clusterrole <role-name> -o yaml`
**oc get clusterrole <role-name> -o yaml**
**oc get clusterrole <role-name> -o yaml**

```bash
oc get clusterrole admin -o yaml
oc get clusterrole edit -o yaml
oc get clusterrole view -o yaml
```

**Descrever ClusterRole**

```bash ignore-test
oc describe clusterrole <nome-da-role>
```

**Exibir detalhes completos do cluster role**
**Exemplo:** `oc describe clusterrole <role-name> | grep -A 50 PolicyRule`

```bash
oc describe clusterrole admin | grep -A 50 PolicyRule
```

### Roles (Namespace)
**Listar roles customizados do namespace**

```bash
oc get roles
```

**Criar Role customizada**

```bash ignore-test
oc create role test-app --verb=<verbos> --resource=<recursos>
```

**Exemplo**
**Exemplo:** `oc create role <role-name> --verb=get,list,watch --resource=pods`

```bash
oc create role pod-reader --verb=get,list,watch --resource=pods
```

**Abrir editor para modificar recurso interativamente**
**Exemplo:** `oc edit role <role-name>`

```bash ignore-test
oc edit role pod-reader
```

**Deletar o role especificado**
**Exemplo:** `oc delete role <role-name>`

```bash
oc delete role pod-reader
```

### ClusterRoleBindings
**Listar ClusterRoleBindings**

```bash
oc get clusterrolebindings
```

**Exibir recurso em formato JSON**

```bash ignore-test
oc get clusterrolebinding -o json | jq -r '.items[] | select(.roleRef.name=="cluster-admin") | .metadata.name'
```

**Adicionar usuário como cluster-admin**

```bash ignore-test
oc adm policy add-cluster-role-to-user cluster-admin <username>
```

**Remover cluster-admin**

```bash ignore-test
oc adm policy remove-cluster-role-from-user cluster-admin <username>
```

**Adicionar grupo**

```bash ignore-test
oc adm policy add-cluster-role-to-group cluster-admin <groupname>
```

### RoleBindings (Namespace)
**Listar vinculações de roles no namespace atual**

```bash
oc get rolebindings
```

**Adicionar role a usuário no namespace**

```bash ignore-test
oc adm policy add-role-to-user <role> <username>
oc adm policy add-role-to-user admin <username>
oc adm policy add-role-to-user edit <username>
oc adm policy add-role-to-user view <username>
```

**Adicionar role a grupo**

```bash ignore-test
oc adm policy add-role-to-group <role> <groupname>
```

**Remover role**

```bash ignore-test
oc adm policy remove-role-from-user <role> <username>
```

**Exibir detalhes completos do recurso**
**Exemplo:** `oc describe rolebinding <rolebinding-name>`

```bash
oc describe rolebinding admin
```

---

## Service Accounts

### Gerenciar Service Accounts
**Listar Service Accounts**

```bash
oc get serviceaccounts
oc get sa
```

**Criar novo recurso**
**Exemplo:** `oc create serviceaccount <serviceaccount-name>`

```bash
oc create serviceaccount test-app
```

**Exibir detalhes completos do serviceaccount**
**Exemplo:** `oc describe sa <serviceaccount-name>`

```bash
oc describe sa test-app
```

**Exibir serviceaccount "test-app" em formato JSON**
**Exemplo:** `oc get sa <serviceaccount-name> -o jsonpath='{.secrets[*].name}'`

```bash ignore-test
oc get sa test-app -o jsonpath='{.secrets[*].name}'
```

**Deletar o serviceaccount especificado**
**Exemplo:** `oc delete sa <serviceaccount-name>`

```bash ignore-test
oc delete sa test-app
```

### Usar Service Accounts
**Adicionar role a Service Account**

```bash ignore-test
oc adm policy add-role-to-user <role> system:serviceaccount:development:test-app
```

**Exemplo: dar role edit**
**Exemplo:** `oc adm policy <resource-name> <username> system:serviceaccount:development:test-app`

```bash
oc adm policy add-role-to-user edit system:serviceaccount:development:test-app
```

**ClusterRole para SA**

```bash ignore-test
oc adm policy add-cluster-role-to-user <role> system:serviceaccount:development:test-app
```

**Usar SA em deployment**
**Exemplo:** `oc set serviceaccount <serviceaccount-name>/test-app test-app`

```bash ignore-test
oc set serviceaccount deployment/test-app test-app
```

**Exibir recurso "test-app" em formato JSON**
**Exemplo:** `oc get pod <resource-name>app -o jsonpath='{.spec.serviceAccountName}'`

```bash ignore-test
oc get pod test-app -o jsonpath='{.spec.serviceAccountName}'
```

---

## Security Context Constraints (SCC)

### Listar e Ver SCCs
**Listar SCCs**

```bash
oc get scc
```

**Exibir recurso "restricted" em formato YAML**

```bash
oc get scc restricted -o yaml
oc get scc privileged -o yaml
oc get scc anyuid -o yaml
```

**Exibir detalhes completos do recurso**
**Exemplo:** `oc describe scc <resource-name>`

```bash
oc describe scc restricted
```

```bash --ignore-test
# Ver qual SCC o pod está usando
# oc get pod <resource-name>app -o yaml | grep scc
oc get pod test-app -o yaml | grep scc
```

**Exibir detalhes completos do recurso**
**Exemplo:** `oc describe scc <resource-name> | grep Users`

```bash
oc describe scc restricted | grep Users
```

### Adicionar Permissões SCC
**Exemplos comuns e use com moderação**
**Exemplo:** `oc adm policy <resource-name> <username> system:serviceaccount:<namespace>:<sa-name>`
**Exemplo:** `oc adm policy <resource-name> <username> system:serviceaccount:<namespace>:<sa-name>`

```bash
oc adm policy add-scc-to-user anyuid system:serviceaccount:development:test-app
oc adm policy add-scc-to-user privileged system:serviceaccount:development:test-app
```

**Adicionar grupo**
**Exemplo:** `oc adm policy <resource-name> <group-name> "cn=ocpusers,cn=users,dc=chiaretto,dc=home"`

```bash
oc adm policy add-scc-to-group restricted "cn=ocpusers,cn=users,dc=chiaretto,dc=home"
```

**Remover SCC de grupo**
**Exemplo:** `oc adm policy <resource-name> <group-name> "cn=ocpusers,cn=users,dc=chiaretto,dc=home"`

```bash
oc adm policy remove-scc-from-group restricted "cn=ocpusers,cn=users,dc=chiaretto,dc=home"
```

**Exibir detalhes completos do recurso**
**Exemplo:** `oc describe scc <resource-name>`

```bash
oc describe scc restricted
```

### Troubleshoot SCC
**Exibir detalhes completos do recurso**
**Exemplo:** `oc describe pod <resource-name> | grep -i scc`

```bash
oc describe pod test-app | grep -i scc
```

**Ver eventos relacionados a SCC**

```bash ignore-test
oc get events --field-selector involvedObject.name=<pod-name> | grep -i scc
```

**Listar recurso de todos os namespaces do cluster**
**Exemplo:** `oc get pod <resource-name>app -o yaml | grep -A 10 securityContext`

```bash ignore-test
oc get pod test-app -o yaml | grep -A 10 securityContext
```

---

## Policies e Auditoria

### Audit Logs
**Ver audit logs (em node)**

```bash ignore-test
oc debug node/<node-name>
chroot /host
cat /var/log/oauth-apiserver/audit.log
cat /var/log/openshift-apiserver/audit.log
cat /var/log/kube-apiserver/audit.log
```

**Buscar ações de usuário específico**

```bash ignore-test
grep <username> /var/log/openshift-apiserver/audit.log
```

### OAuth e Autenticação
**Exibir recurso "cluster" em formato YAML**

```bash
oc get oauth cluster -o yaml
```

**Exibir recurso "cluster" em formato JSON**

```bash
oc get oauth cluster -o jsonpath='{.spec.identityProviders}'
```

**Ver pods do OAuth**

```bash
oc get pods -n openshift-authentication
```

**Logs do OAuth**

```bash ignore-test
oc logs -n openshift-authentication <oauth-pod>
```

### Secrets de TLS
**Listar recurso filtrados por campo específico**

```bash
oc get secrets --field-selector type=kubernetes.io/tls
```

**Ver certificado**

```bash ignore-test
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

**Verificar validade**

```bash ignore-test
oc get secret <secret-name> -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -enddate -noout
```

**Criar secret TLS**

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
