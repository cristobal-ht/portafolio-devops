#!/bin/bash

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

# Esperar un momento a que el pod esté listo
echo "Wait: Esperando a que el Pod suba..."
sleep 5
kubectl get pods

# 4. Levanta el portforward
echo "🌐 Paso 4: Levantando acceso en http://localhost:9000"
echo "⚠️  ATENCIÓN: Esta terminal quedará bloqueada. Presiona Ctrl+C para detener."
kubectl port-forward service/mi-sitio-service 9000:8080