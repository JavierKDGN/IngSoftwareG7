import os

# Este archivo contiene la configuración de la aplicación. La configuración se almacena en objetos de Python como atributos de clase. Las configuraciones específicas de la aplicación se pueden agregar creando subclases de Config. Por ejemplo, Config y ConfigTest son subclases de Config. La configuración se puede recuperar desde la variable de entorno o se puede usar un valor predeterminado si la variable de entorno no está configurada. La configuración de la aplicación se puede cambiar en tiempo de ejecución, pero solo si la aplicación no se ha iniciado todavía.
#  La configuración de la aplicación se puede acceder desde la variable app.config.

class Config:
    # Clave secreta para protección CSRF
    # La clave secreta se utiliza para proteger las cookies de la aplicación contra la falsificación de solicitudes entre sitios. La clave secreta se utiliza para firmar cookies y otros datos. Si un atacante pudiera obtener la clave secreta, podría falsificar cookies y otros datos firmados. La clave secreta debe ser lo más segura posible y no debe compartirse con nadie.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test_key' # implementar en sprint 2