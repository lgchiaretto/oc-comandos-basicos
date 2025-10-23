# 🐳 Pods e Containers

Este documento contém comandos para gerenciar pods e containers no OpenShift.

---

## 📋 Índice

1. [Listagem e Informações](#listagem-e-informações)
2. [Interação com Pods](#interação-com-pods)
3. [Gerenciamento de Pods](#gerenciamento-de-pods)
4. [Debug e Troubleshooting](#debug-e-troubleshooting)
5. [Logs](#logs)

---

## 📊 Listagem e Informações

### Listar Pods
```bash
# Listar todos os pods
oc get pods
```

```bash
# Listar pods em todos os namespaces
oc get pods -A
```

```bash
# Listar pods com mais detalhes
oc get pods -o wide
```

```bash
# Listar pods com labels
oc get pods --show-labels
```

```bash
# Listar pods por seletor
oc get pods -l app=test-app
```

```bash
# Listar pods em um projeto específico
# oc get pods -n <namespace>
oc get pods -n development
```

```bash
# Listar pods com status customizado
oc get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,IP:.status.podIP
```

```bash ignore-test
# Descrever um pod
oc describe pod <nome-do-pod>
```

```bash ignore-test
# Ver definição YAML do pod
oc get pod <nome-do-pod> -o yaml
```

```bash ignore-test
# Ver definição JSON do pod
oc get pod <nome-do-pod> -o json
```

```bash ignore-test
# Ver apenas o status
oc get pod <nome-do-pod> -o jsonpath='{.status.phase}'
```

---

## 💻 Interação com Pods

### Acessar Shell
```bash ignore-test
# Acessar shell de um pod
oc rsh <nome-do-pod>
```

```bash ignore-test
# Executar comando em um pod
oc exec <nome-do-pod> -- <comando>
```

```bash ignore-test
# Executar comando interativo
oc exec -it <nome-do-pod> -- /bin/sh
```

```bash ignore-test
# Executar comando em container específico
oc exec <nome-do-pod> -c <nome-do-container> -- <comando>
```

```bash ignore-test
# Exemplo prático
oc exec -it mypod -- /bin/sh
```

### Copiar Arquivos
```bash ignore-test
# Copiar arquivo para o pod
oc cp <arquivo-local> <nome-do-pod>:<caminho-no-pod>
```

```bash ignore-test
# Copiar arquivo do pod
oc cp <nome-do-pod>:<caminho-no-pod> <arquivo-local>
```

```bash ignore-test
# Copiar diretório
oc cp /local/dir <nome-do-pod>:/container/dir
```

```bash ignore-test
# Copiar diretório com rsync (precisa ter rsync instalado no pod)
oc rsync /local/dir <nome-do-pod>:/container/dir
```

```bash ignore-test
# Exemplo
oc cp ./config.json mypod:/etc/config/config.json
```

---

## 🔧 Gerenciamento de Pods

### Criar e Deletar
```bash ignore-test
# Criar pod a partir de arquivo YAML
oc create -f pod.yaml
```

```bash ignore-test
# Aplicar mudanças em pod
oc apply -f pod.yaml
```

```bash ignore-test
# Deletar um pod
oc delete pod <nome-do-pod>
```

```bash ignore-test
# Deletar pod forçadamente
oc delete pod <nome-do-pod> --grace-period=0 --force
```

```bash
# Deletar todos os pods com label
oc delete pods -l app=test-app
```

### Reiniciar Pods
```bash
# Reiniciar pods de um deployment
# oc rollout restart <resource-name>/test-app
oc rollout restart deployment/test-app
```

```bash ignore-test
# Deletar pod para forçar recriação
oc delete pod <nome-do-pod>
```

```bash
# Scale down deployment test-app
# oc scale deployment <deployment-name> --replicas=0
oc scale deployment test-app --replicas=0
```
```bash
# Scale up deployment test-app
# oc scale deployment <deployment-name> --replicas=2
oc scale deployment test-app --replicas=2
```
---

## 🔍 Debug e Troubleshooting

### Debug Interativo
```bash ignore-test
# Debug interativo de pod
oc debug pod/<nome-do-pod>
```

```bash ignore-test
# Debug com imagem customizada
oc debug pod/<nome-do-pod> --image=busybox
```

```bash ignore-test
# Debug como root
oc debug pod/<nome-do-pod> --as-root
```

```bash
# Criar pod de debug temporário e imprima o hostname
oc run debug-pod --image=busybox -it --rm --restart=Never -- hostname
```

```bash ignore-test
# Criar pod de debug temporário e conecte
oc run debug-pod --image=busybox -it --rm --restart=Never -- sh
```

### Verificações
```bash
# Ver pods com problemas
oc get pods --field-selector=status.phase!=Running
```

```bash
# Ver pods pendentes
oc get pods --field-selector=status.phase=Pending
```

```bash
# Ver pods falhados
oc get pods --field-selector=status.phase=Failed
```

```bash ignore-test
# Ver motivo de erro do pod
oc describe pod <nome-do-pod> | grep -A 10 "Events:"
```

---

## 📝 Logs

### Ver Logs
```bash ignore-test
# Ver logs de um pod
oc logs <nome-do-pod>
```

```bash ignore-test
# Ver logs em tempo real
oc logs -f <nome-do-pod>
```

```bash ignore-test
# Ver logs de container específico
oc logs <nome-do-pod> -c <nome-do-container>
```

```bash ignore-test
# Ver logs anteriores (pod crasheado)
oc logs <nome-do-pod> --previous
```

```bash ignore-test
# Ver últimas N linhas dos logs
oc logs <nome-do-pod> --tail=<numero>
```

```bash ignore-test
# Ver logs desde timestamp específico
oc logs <nome-do-pod> --since=1h
```

```bash
# Ver logs de todos os pods com label
oc logs -l app=test-app
```

## 📋 Monitoramento e Eventos

### Ver Eventos
```bash
# Ver eventos ordenados por timestamp
oc get events --sort-by='.lastTimestamp'
```

```bash
# Em namespace específico
oc get events -n development --sort-by='.lastTimestamp'
```

```bash
# Últimos 10 eventos
oc get events -n development --sort-by='.lastTimestamp' | head -10
```

---

## 📖 Navegação

- [← Anterior: Aplicações](03-aplicacoes.md)
- [→ Próximo: Deployments e Scaling](05-deployments-scaling.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
