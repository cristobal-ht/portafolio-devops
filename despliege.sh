#!/bin/bash
set -euo pipefail # Detener ante errores, variables no definidas o fallos en pipes

# --- Configuración de variables ---
NOMBRE_IMAGEN="paginaweb:1.0"
NOMBRE_CLUSTER="mi-pagina-web"
DEPLOYMENT="mi-sitio-deployment"

echo "🚀 Iniciando proceso de despliegue..."

# 1. Construye docker
echo "📦 Paso 1: Construyendo la imagen Docker..."
docker build -t $NOMBRE_IMAGEN .

# 2. Sube la imagen al cluster kind
echo "🚚 Paso 2: Cargando imagen al cluster $NOMBRE_CLUSTER..."
kind load docker-image $NOMBRE_IMAGEN --name $NOMBRE_CLUSTER

# 3. Actualiza el deployment
echo "🔄 Paso 3: Reiniciando Pods en Kubernetes..."
kubectl apply -f deployment.yaml
kubectl rollout restart deployment/$DEPLOYMENT

# Esperar de forma inteligente a que el pod esté listo
echo "⏳ Esperando a que el Deployment esté listo..."
kubectl rollout status deployment/$DEPLOYMENT --timeout=90s

echo "✅ Pods activos:"
kubectl get pods

# 4. Levanta el portforward
echo "🌐 Paso 4: Levantando acceso en http://localhost:9000"
echo "⚠️  ATENCIÓN: Esta terminal quedará bloqueada. Presiona Ctrl+C para detener."
kubectl port-forward service/mi-sitio-service 9000:8080