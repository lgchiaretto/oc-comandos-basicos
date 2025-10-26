# ⏰ Jobs e CronJobs

Este documento contém comandos para gerenciar Jobs e CronJobs no OpenShift.

---

## 📋 Índice

1. [🏃 Jobs](#jobs)
2. [⏰ CronJobs](#cronjobs)
3. [🔧 Troubleshooting](#troubleshooting)
---

## 🏃 Jobs

### Criar Jobs
```bash
# Job simples
# oc create job test-app-job --image=nicolaka/netshoot -- echo "Hello World"
# oc create job <job-name> --image=nicolaka/netshoot -- echo "Hello World"
oc create job test-app-job --image=nicolaka/netshoot -- echo "Hello World"
```

```bash
# De arquivo yaml
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: test-app-job-yaml
spec:
  template:
    spec:
      containers:
      - name: job
        image: nicolaka/netshoot
        command: ["echo", "Hello from Job"]
      restartPolicy: Never
  backoffLimit: 4
EOF
```

```bash
# Job com múltiplas tentativas
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: retry-job
spec:
  template:
    spec:
      containers:
      - name: job
        image: nicolaka/netshoot
        command: ["sh", "-c", "exit 1"]  # Vai falhar
      restartPolicy: Never
  backoffLimit: 3  # Tentar 3 vezes
EOF
```

### Gerenciar Jobs
```bash
# Listar jobs
oc get jobs
```

```bash
# Descrever job
# oc describe job <job-name>
oc describe job test-app-job
```

```bash ignore-test
# Ver logs do job
oc logs job/test-app-job
```

```bash
# Ver pods do job
oc get pods -l job-name=test-app-job
```

```bash
# Deletar job
# oc delete job <job-name>
oc delete job test-app-job
```

```bash ignore-test
# Deletar job e seus pods
# oc delete job <job-name> --cascade=foreground
oc delete job test-app --cascade=foreground
```

### Jobs Paralelos
```bash
# Job com parallelism
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: parallel-job
spec:
  parallelism: 3  # 3 pods simultâneos
  completions: 9  # Total de 9 execuções
  template:
    spec:
      containers:
      - name: job
        image: nicolaka/netshoot
        command: ["sh", "-c", "echo Processing && sleep 5"]
      restartPolicy: Never
EOF
```

```bash ignore-test
# Monitorar
# oc get job <job-name>
oc get job parallel-job
oc get pods -l job-name=parallel-job
```

### Jobs com TTL
```bash ignore-test
# Job que se auto-deleta após completar
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: ttl-job
spec:
  ttlSecondsAfterFinished: 100  # Deletar após 100s
  template:
    spec:
      containers:
      - name: job
        image: nicolaka/netshoot
        command: ["echo", "This job will be deleted"]
      restartPolicy: Never
EOF
```

---

## ⏰ CronJobs

### Criar CronJobs
```bash
# CronJob simples
# oc create cronjob <job-name> --image=nicolaka/netshoot --schedule="*/5 * * * *" -- echo "Hello every 5 minutes"
oc create cronjob test-app-job --image=nicolaka/netshoot --schedule="*/5 * * * *" -- echo "Hello every 5 minutes"
```

```bash ignore-test
# De arquivo
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: test-app
spec:
  schedule: "0 2 * * *"  # Diariamente às 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: job
            image: nicolaka/netshoot
            command: ["sh", "-c", "date; echo Hello from CronJob"]
          restartPolicy: OnFailure
EOF
```

### Gerenciar CronJobs
```bash
# Listar cronjobs
oc get cronjobs
oc get cj
```

```bash ignore-test
# Descrever cronjob
# oc describe cronjob <job-name>
oc describe cronjob test-app-job
```

```bash ignore-test
# Ver jobs criados pelo cronjob
oc get jobs -l cronjob=<cronjob-name>
```

```bash ignore-test
# Ver último job
oc get jobs --sort-by=.metadata.creationTimestamp | grep <cronjob-name> | tail -1
```

```bash ignore-test
# Suspender cronjob
# oc patch cronjob <job-name> -p '{"spec":{"suspend":true}}'
oc patch cronjob test-app-job -p '{"spec":{"suspend":true}}'
```

```bash ignore-test
# Reativar
# oc patch cronjob <job-name> -p '{"spec":{"suspend":false}}'
oc patch cronjob test-app-job -p '{"spec":{"suspend":false}}'
```

```bash
# Deletar cronjob
# oc delete cronjob <job-name>
oc delete cronjob test-app-job
```

```bash ignore-test
# Deletar cronjob e jobs/pods
# oc delete cronjob <job-name> --cascade=foreground
oc delete cronjob test-app --cascade=foreground
```

### CronJob Avançado
```bash
# Com configurações completas
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-cronjob
spec:
  schedule: "0 3 * * *"  # 3 AM diariamente
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  concurrencyPolicy: Forbid  # Não permitir execução simultânea
  startingDeadlineSeconds: 300  # Começar até 5 min após schedule
  suspend: false
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: registry.redhat.io/rhel8/support-tools
            command:
            - /bin/sh
            - -c
            - |
              echo "Starting backup at \$(date)"
              # Seu script de backup aqui
              echo "Backup completed at \$(date)"
          restartPolicy: OnFailure
      backoffLimit: 2
      activeDeadlineSeconds: 3600  # Timeout de 1 hora
EOF
```

### Concurrency Policy
```bash
# Allow - Permitir jobs simultâneos (padrão)
concurrencyPolicy: Allow
```

```bash
# Forbid - Não permitir simultâneos (pula se ainda rodando)
concurrencyPolicy: Forbid
```

```bash
# Replace - Cancela job atual e inicia novo
concurrencyPolicy: Replace
```

---

## 🔧 Troubleshooting

### Debug de Jobs
```bash ignore-test
# Ver status do job
# oc get job <job-name> -o yaml
oc get job test-app-job -o yaml
```

```bash ignore-test
# Ver condições
# oc get job <job-name> -o jsonpath='{.status.conditions}'
oc get job test-app-job -o jsonpath='{.status.conditions}'
```

```bash ignore-test
# Ver por que job falhou
# oc describe job <job-name>
oc describe job test-app-job
```

```bash ignore-test
# Logs do pod anterior (se falhou)
oc logs $POD --previous
```

```bash ignore-test
# Ver eventos
oc get events --field-selector involvedObject.name=test-app-job
```

### Debug de CronJobs
```bash ignore-test
# Ver status do cronjob
# oc get cronjob <job-name> -o yaml
oc get cronjob test-app-job -o yaml
```

```bash ignore-test
# Ver último schedule
# oc get cronjob <job-name> -o jsonpath='{.status.lastScheduleTime}'
oc get cronjob test-app-job -o jsonpath='{.status.lastScheduleTime}'
```

```bash ignore-test
# Criar job manual para testar
oc create job test-job --from=cronjob/<cronjob-name>
```

```bash ignore-test
# Ver histórico de jobs
oc get jobs --sort-by=.metadata.creationTimestamp -l cronjob=test-app-job
```

```bash ignore-test
# Logs do último job
LAST_JOB=$(oc get jobs --sort-by=.metadata.creationTimestamp -l cronjob=test-app-job -o name | tail -1)
oc logs $LAST_JOB
```

### Jobs Travados
```bash
# Ver jobs rodando há muito tempo
oc get jobs -o json | jq -r '.items[] | select(.status.active > 0) | "\(.metadata.name) - \(.metadata.creationTimestamp)"'
```

```bash ignore-test
# Deletar jobs antigos manualmente
oc get jobs -o json | jq -r '.items[] | select(.status.completionTime != null) | select(.status.completionTime < "'$(date -d '7 days ago' -Ins --utc | sed 's/+00:00/Z/')'" ) | .metadata.name' | xargs oc delete job
```

```bash ignore-test
# Ou com script
for job in $(oc get jobs -o name); do
  STATUS=$(oc get $job -o jsonpath='{.status.succeeded}')
  if [ "$STATUS" == "1" ]; then
    echo "Deleting completed job: $job"
    oc delete $job
  fi
done
```

---

### Limpeza de Recursos
```bash ignore-test
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup-old-pods
spec:
  schedule: "0 */6 * * *"  # A cada 6 horas
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: cleanup-sa
          containers:
          - name: cleanup
            image: registry.redhat.io/openshift4/ose-cli:latest
            command:
            - /bin/bash
            - -c
            - |
              echo "Starting cleanup..."
              # Deletar pods completados
              oc delete pods --field-selector=status.phase==Succeeded -A
              # Deletar jobs antigos
              oc get jobs -A -o json | jq -r '.items[] | select(.status.completionTime != null) | "\(.metadata.namespace) \(.metadata.name)"' | while read ns name; do
                oc delete job $name -n $ns
              done
              echo "Cleanup completed"
          restartPolicy: OnFailure
EOF
```

## 📚 Documentação Oficial

Consulte a documentação oficial do OpenShift 4.19 da Red Hat:

- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/nodes" target="_blank">Nodes - Working with jobs and cron jobs</a>
- <a href="https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/building_applications" target="_blank">Building applications</a>

---

## 📖 Navegação

- [← Anterior: Patch e Edit](28-patch-edit.md)
- [→ Próximo: Operators e Operandos](30-operators-operandos.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
