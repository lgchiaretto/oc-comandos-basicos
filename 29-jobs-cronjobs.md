# ⏰ Jobs e CronJobs

Este documento contém comandos para gerenciar Jobs e CronJobs no OpenShift.

---

## 📋 Índice

1. [Jobs](#jobs)
2. [CronJobs](#cronjobs)
3. [Troubleshooting](#troubleshooting)
4. [Exemplos Práticos](#exemplos-práticos)

---

## 🏃 Jobs

### Criar Jobs
```bash
# Job simples
# oc create job <job-name> --image=busybox -- echo "Hello World"
oc create job my-job --image=busybox -- echo "Hello World"
```

```bash ignore-test
# De arquivo
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: my-job
spec:
  template:
    spec:
      containers:
      - name: job
        image: busybox
        command: ["echo", "Hello from Job"]
      restartPolicy: Never
  backoffLimit: 4
EOF
```

```bash ignore-test
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
        image: busybox
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

```bash ignore-test
# Descrever job
oc describe job <job-name>
```

```bash ignore-test
# Ver logs do job
oc logs job/<job-name>
```

```bash ignore-test
# Ver pods do job
oc get pods -l job-name=<job-name>
```

```bash ignore-test
# Deletar job
oc delete job <job-name>
```

```bash ignore-test
# Deletar job e seus pods
oc delete job <job-name> --cascade=foreground
```

```bash
# Manter pods após completar
# (não deletar automaticamente)
```

### Jobs Paralelos
```bash ignore-test
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
        image: busybox
        command: ["sh", "-c", "echo Processing && sleep 5"]
      restartPolicy: Never
EOF
```

```bash
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
        image: busybox
        command: ["echo", "This job will be deleted"]
      restartPolicy: Never
EOF
```

---

## ⏰ CronJobs

### Criar CronJobs
```bash
# CronJob simples
# oc create cronjob <job-name> --image=busybox --schedule="*/5 * * * *" -- echo "Hello every 5 minutes"
oc create cronjob my-cronjob --image=busybox --schedule="*/5 * * * *" -- echo "Hello every 5 minutes"
```

```bash ignore-test
# De arquivo
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: my-cronjob
spec:
  schedule: "0 2 * * *"  # Diariamente às 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: job
            image: busybox
            command: ["sh", "-c", "date; echo Hello from CronJob"]
          restartPolicy: OnFailure
EOF
```

### Schedule Syntax
```bash
# Formato: "minuto hora dia mês dia-da-semana"
# * = qualquer valor
# */N = a cada N
```

```bash
# Exemplos:
"*/5 * * * *"      # A cada 5 minutos
"0 * * * *"        # A cada hora (no minuto 0)
"0 2 * * *"        # Diariamente às 2 AM
"0 */4 * * *"      # A cada 4 horas
"0 0 * * 0"        # Toda semana no domingo à meia-noite
"0 0 1 * *"        # Todo primeiro dia do mês à meia-noite
"30 1 * * 1-5"     # Segunda a Sexta, 1:30 AM
"0 9-17 * * *"     # A cada hora das 9h às 17h
"0 0 1,15 * *"     # Dia 1 e 15 de cada mês
```

### Gerenciar CronJobs
```bash
# Listar cronjobs
oc get cronjobs
oc get cj
```

```bash ignore-test
# Descrever cronjob
oc describe cronjob <name>
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
oc patch cronjob <name> -p '{"spec":{"suspend":true}}'
```

```bash ignore-test
# Reativar
oc patch cronjob <name> -p '{"spec":{"suspend":false}}'
```

```bash ignore-test
# Deletar cronjob
oc delete cronjob <name>
```

```bash ignore-test
# Deletar cronjob e jobs/pods
oc delete cronjob <name> --cascade=foreground
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
oc get job <name> -o yaml
```

```bash ignore-test
# Ver condições
oc get job <name> -o jsonpath='{.status.conditions}'
```

```bash ignore-test
# Ver por que job falhou
oc describe job <name>
```

```bash ignore-test
# Logs do pod do job
POD=$(oc get pods -l job-name=<name> -o jsonpath='{.items[0].metadata.name}')
oc logs $POD
```

```bash
# Logs do pod anterior (se falhou)
oc logs $POD --previous
```

```bash ignore-test
# Ver eventos
oc get events --field-selector involvedObject.name=<job-name>
```

### Debug de CronJobs
```bash ignore-test
# Ver status do cronjob
oc get cronjob <name> -o yaml
```

```bash ignore-test
# Ver último schedule
oc get cronjob <name> -o jsonpath='{.status.lastScheduleTime}'
```

```bash
# Ver próxima execução (estimada)
# Não há campo nativo, calcular baseado em schedule
```

```bash ignore-test
# Criar job manual para testar
oc create job test-job --from=cronjob/<cronjob-name>
```

```bash ignore-test
# Ver histórico de jobs
oc get jobs --sort-by=.metadata.creationTimestamp -l cronjob=<name>
```

```bash ignore-test
# Logs do último job
LAST_JOB=$(oc get jobs --sort-by=.metadata.creationTimestamp -l cronjob=<name> -o name | tail -1)
oc logs $LAST_JOB
```

### Jobs Travados
```bash
# Verificar jobs completados/falhados
oc get jobs --field-selector status.successful=1
oc get jobs --field-selector status.failed=1
```

```bash ignore-test
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

## 💡 Exemplos Práticos

### Backup Diário
```bash
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-backup
spec:
  schedule: "0 2 * * *"
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: backup-sa
          containers:
          - name: backup
            image: registry.redhat.io/rhel8/support-tools
            command:
            - /bin/bash
            - -c
            - |
              BACKUP_DIR="/backups/backup-\$(date +%Y%m%d)"
              mkdir -p \$BACKUP_DIR
              echo "Backing up to \$BACKUP_DIR"
              # Comandos de backup aqui
              tar czf \$BACKUP_DIR/data.tar.gz /data
              echo "Backup completed"
            volumeMounts:
            - name: data
              mountPath: /data
            - name: backups
              mountPath: /backups
          restartPolicy: OnFailure
          volumes:
          - name: data
            persistentVolumeClaim:
              claimName: app-data
          - name: backups
            persistentVolumeClaim:
              claimName: backup-storage
EOF
```

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

### Health Check Periódico
```bash ignore-test
cat <<EOF | oc apply -f -
apiVersion: batch/v1
kind: CronJob
metadata:
  name: health-check
spec:
  schedule: "*/15 * * * *"  # A cada 15 minutos
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: health-check
            image: curlimages/curl:latest
            command:
            - /bin/sh
            - -c
            - |
              URL="https://myapp.example.com/health"
              STATUS=\$(curl -s -o /dev/null -w "%{http_code}" \$URL)
              if [ \$STATUS -eq 200 ]; then
                echo "✅ Health check passed: \$URL returned \$STATUS"
                exit 0
              else
                echo "❌ Health check failed: \$URL returned \$STATUS"
                exit 1
              fi
          restartPolicy: Never
EOF
```

---

## 📖 Navegação

- [← Anterior: Patch e Edit](28-patch-edit.md)
- [→ Próximo: Operators e Operandos](30-operators-operandos.md)
- [↑ Índice Principal](README.md)

---

**Última atualização**: Outubro 2025
