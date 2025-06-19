# 🚀 Despliegue de You-Space.info con Cloudflare

Esta guía te ayudará a desplegar tu aplicación Flask en un servidor Linux y conectarla con tu dominio `you-space.info` a través de Cloudflare.

## 📋 Requisitos Previos

### En tu servidor Linux:
- Ubuntu 20.04+ o Debian 11+
- Python 3.8+
- Nginx
- Acceso SSH con permisos sudo

### En Cloudflare:
- Dominio `you-space.info` configurado
- Panel de Cloudflare activo

## 🔧 Paso 1: Preparación Local (Windows)

1. **Ejecuta la configuración local:**
   ```cmd
   configuracion_windows.bat
   ```

2. **Verifica que todo funcione:**
   ```cmd
   python app.py
   ```

3. **Sube todos los archivos a tu servidor** usando SCP, SFTP o Git.

## 🖥️ Paso 2: Configuración del Servidor

### 2.1 Conectar al servidor
```bash
ssh usuario@tu-servidor.com
```

### 2.2 Instalar dependencias del sistema
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx ufw
```

### 2.3 Ejecutar el script de despliegue
```bash
cd /ruta/a/tu/aplicacion
bash deploy.sh
```

## ☁️ Paso 3: Configuración de Cloudflare

### 3.1 Configurar DNS
1. Ve a tu panel de Cloudflare
2. Selecciona el dominio `you-space.info`
3. Ve a **DNS > Records**
4. Configura estos registros:

| Tipo | Nombre | Contenido | Proxy |
|------|--------|-----------|-------|
| A | @ | [IP de tu servidor] | ✅ Activado |
| A | www | [IP de tu servidor] | ✅ Activado |

### 3.2 Configurar SSL/TLS
1. Ve a **SSL/TLS > Overview**
2. Configura: **Full (strict)**
3. Ve a **SSL/TLS > Edge Certificates**
4. Activa:
   - ✅ Always Use HTTPS
   - ✅ HSTS
   - ✅ Minimum TLS Version: 1.2

### 3.3 Configurar Page Rules (Opcional)
1. Ve a **Page Rules**
2. Crea una regla:
   - URL: `you-space.info/*`
   - Configuración: Always Use HTTPS

## 🔒 Paso 4: Configuración de Seguridad

### 4.1 Firewall
```bash
sudo ufw enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
```

### 4.2 Headers de Seguridad
Los headers ya están configurados en `nginx.conf`:
- X-Frame-Options
- X-XSS-Protection
- X-Content-Type-Options
- Content-Security-Policy

## 📊 Paso 5: Monitoreo y Logs

### 5.1 Ver logs de la aplicación
```bash
sudo journalctl -u you-space -f
```

### 5.2 Ver logs de Nginx
```bash
sudo tail -f /var/log/nginx/you-space.info.error.log
sudo tail -f /var/log/nginx/you-space.info.access.log
```

### 5.3 Verificar estado de servicios
```bash
sudo systemctl status you-space
sudo systemctl status nginx
```

## 🔄 Paso 6: Actualizaciones

### 6.1 Actualizar la aplicación
```bash
cd /var/www/you-space.info
git pull  # si usas Git
sudo systemctl restart you-space
```

### 6.2 Actualizar dependencias
```bash
cd /var/www/you-space.info
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart you-space
```

## 🛠️ Comandos Útiles

### Reiniciar servicios
```bash
sudo systemctl restart you-space
sudo systemctl restart nginx
```

### Ver configuración de Nginx
```bash
sudo nginx -t
```

### Ver puertos en uso
```bash
sudo netstat -tlnp
```

### Verificar conectividad
```bash
curl -I https://you-space.info
```

## 🚨 Solución de Problemas

### Error 502 Bad Gateway
```bash
# Verificar que Gunicorn esté corriendo
sudo systemctl status you-space

# Verificar logs
sudo journalctl -u you-space -f
```

### Error de permisos
```bash
# Corregir permisos
sudo chown -R www-data:www-data /var/www/you-space.info
sudo chmod -R 755 /var/www/you-space.info
```

### Error de SSL
1. Verifica configuración en Cloudflare
2. Asegúrate de que el proxy esté activado
3. Verifica que el certificado SSL esté configurado como "Full (strict)"

### La aplicación no carga
```bash
# Verificar que el puerto 8000 esté abierto
sudo netstat -tlnp | grep 8000

# Verificar configuración de Nginx
sudo nginx -t
```

## 📞 Soporte

Si tienes problemas:

1. **Verifica los logs** usando los comandos de monitoreo
2. **Revisa la configuración** de Cloudflare
3. **Asegúrate** de que la IP del servidor esté correcta en Cloudflare
4. **Verifica** que los puertos 80 y 443 estén abiertos

## 🌐 Resultado Final

Una vez completado el despliegue, tu aplicación estará disponible en:
- **https://you-space.info** (con SSL automático)
- **https://www.you-space.info** (redirección automática)

La aplicación estará protegida por Cloudflare con:
- ✅ SSL/TLS automático
- ✅ Protección DDoS
- ✅ CDN global
- ✅ Headers de seguridad
- ✅ Redirección HTTPS automática 