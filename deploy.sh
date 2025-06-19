#!/bin/bash

# Script de despliegue para You-Space.info
# Configuración para Cloudflare + Nominalia

set -e

echo "🚀 Iniciando despliegue de You-Space.info..."

# Variables
DOMAIN="you-space.info"
APP_DIR="/var/www/$DOMAIN"
SERVICE_NAME="you-space"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si se ejecuta como root
if [[ $EUID -eq 0 ]]; then
   print_error "Este script no debe ejecutarse como root"
   exit 1
fi

# Crear directorio de la aplicación
print_status "Creando directorio de la aplicación..."
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copiar archivos de la aplicación
print_status "Copiando archivos de la aplicación..."
cp -r . $APP_DIR/
cd $APP_DIR

# Crear entorno virtual
print_status "Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
print_status "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Configurar permisos
print_status "Configurando permisos..."
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod -R 775 $APP_DIR/tema/assets/uploads

# Configurar Nginx
print_status "Configurando Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/$DOMAIN
sudo ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Verificar configuración de Nginx
print_status "Verificando configuración de Nginx..."
sudo nginx -t

# Configurar systemd
print_status "Configurando servicio systemd..."
sudo cp $SERVICE_NAME.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

# Iniciar servicios
print_status "Iniciando servicios..."
sudo systemctl start $SERVICE_NAME
sudo systemctl restart nginx

# Verificar estado de los servicios
print_status "Verificando estado de los servicios..."
sudo systemctl status $SERVICE_NAME --no-pager
sudo systemctl status nginx --no-pager

# Configurar firewall
print_status "Configurando firewall..."
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp

# Configurar SSL con Certbot (opcional)
read -p "¿Deseas configurar SSL con Let's Encrypt? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Instalando Certbot..."
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
    
    print_status "Obteniendo certificado SSL..."
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
fi

# Configurar Cloudflare
print_status "Configurando Cloudflare..."
echo ""
echo "📋 CONFIGURACIÓN DE CLOUDFLARE:"
echo "1. Ve a tu panel de Cloudflare"
echo "2. Selecciona el dominio: $DOMAIN"
echo "3. Ve a DNS > Records"
echo "4. Configura los siguientes registros:"
echo ""
echo "   Tipo: A"
echo "   Nombre: @"
echo "   Contenido: [IP de tu servidor]"
echo "   Proxy: Activado (nube naranja)"
echo ""
echo "   Tipo: A"
echo "   Nombre: www"
echo "   Contenido: [IP de tu servidor]"
echo "   Proxy: Activado (nube naranja)"
echo ""
echo "5. Ve a SSL/TLS > Overview"
echo "6. Configura: Full (strict)"
echo "7. Ve a SSL/TLS > Edge Certificates"
echo "8. Activa: Always Use HTTPS"
echo "9. Activa: HSTS"
echo ""

# Verificar conectividad
print_status "Verificando conectividad..."
sleep 5
if curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN | grep -q "200\|301\|302"; then
    print_status "✅ La aplicación está funcionando correctamente!"
else
    print_warning "⚠️  La aplicación podría no estar respondiendo aún. Verifica los logs:"
    echo "   sudo journalctl -u $SERVICE_NAME -f"
    echo "   sudo tail -f /var/log/nginx/error.log"
fi

print_status "🎉 Despliegue completado!"
echo ""
echo "📝 Comandos útiles:"
echo "   Ver logs de la aplicación: sudo journalctl -u $SERVICE_NAME -f"
echo "   Reiniciar aplicación: sudo systemctl restart $SERVICE_NAME"
echo "   Ver estado: sudo systemctl status $SERVICE_NAME"
echo "   Ver logs de Nginx: sudo tail -f /var/log/nginx/$DOMAIN.error.log"
echo ""
echo "🌐 Tu aplicación estará disponible en: https://$DOMAIN" 